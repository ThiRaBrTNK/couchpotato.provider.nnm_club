# -*- coding: utf8 -*-
import traceback

from couchpotato.core.helpers.encoding import tryUrlencode
from couchpotato.core.helpers.variable import tryInt
from couchpotato.core.logger import CPLog
from couchpotato.core.media._base.providers.torrent.base import TorrentProvider
from couchpotato.core.media.movie.providers.base import MovieProvider
from bs4 import BeautifulSoup
from datetime import datetime

import re


log = CPLog(__name__)


class rutracker(TorrentProvider, MovieProvider):

    baseurl = 'https://rutracker.org/forum/'
    urls = {
        'test' : 'https://rutracker.org',
        'login' : baseurl + 'login.php',
        'login_check': baseurl + 'privmsg.php',
        'detail' : baseurl + 'viewtopic.php?t=%s',
        'search' : baseurl + 'tracker.php?nm=%s&o=7&c=14&f=313',
        'download' : baseurl + 'dl.php?t=%s',
    }

    months = (u'Янв', u'Фев', u'Мар', u'Апр', u'Май', u'Июн', u'Июл', u'Авг', u'Сен', u'Окт', u'Ноя', u'Дек')

    http_time_between_calls = 1 #seconds
    cat_backup_id = None

    def _searchOnTitle(self, title, movie, quality, results):
        if len(title) == 0:
            log.debug('Skipping. Reason: Title is empty')
            return
            
        log.debug('Searching rutracker for %s' % (title))

        if len(title) < 2:
            log.debug('Skipping. Reason: Title is too short for search')
            return

        url = self.urls['search'] % title.replace(':', ' ')
        data = self.getHTMLData(url).decode('cp1251')

        log.debug('Received data from rutracker')
        if data:
            log.debug('Data is valid from rutracker')
            html = BeautifulSoup(data)

            try:
                result_table = html.find(id='tor-tbl')
                if not result_table:
                    log.debug('No table results from rutracker')
                    return

                table_head = result_table.find('thead')
                header_cells = table_head.find_all('th')

                # Cells idx
                title_cell_idx = header_cells.index(table_head.find('th', text=u'Тема'))
                size_idx = header_cells.index(table_head.find('th', text=u'Размер'))
                seed_idx = header_cells.index(table_head.find('th', text='S'))
                leech_idx = header_cells.index(table_head.find('th', text='L'))
                date_added_idx = header_cells.index(table_head.find('th', text=u'Добавлен'))

                torrents = result_table.find_all('tr', attrs = {'class' : 'hl-tr'})
                log.debug('Found %s results from rutracker', len(torrents))
                for result in torrents:
                    all_cells = result.find_all('td')

                    # Cells
                    title_cell = all_cells[title_cell_idx].find('a')
                    dl_cell = all_cells[size_idx].find('a')
                    size_cell = all_cells[size_idx].find('a')
                    seed_cell = all_cells[seed_idx]
                    leech_cell = all_cells[leech_idx]
                    date_added_cell = all_cells[date_added_idx].find('p')

                    # Torrent data
                    topic_id = title_cell['href']
                    topic_id = topic_id.replace('viewtopic.php?t=', '')
                    torrent_id = dl_cell['href']
                    torrent_id = torrent_id.replace('dl.php?t=', '')

                    torrent_name = self.formatTitle(title_cell.getText())
                    torrent_size = self.parseSize(size_cell.text.strip()[:-2])
                    torrent_seeders = tryInt(seed_cell.getText())
                    torrent_leechers = tryInt(leech_cell.getText())
                    torrent_age = date_added_cell.text.strip()
                    torrent_age_day, torrent_age_month, torrent_age_year = torrent_age.split('-')
                    torrent_age_year = int(torrent_age_year)
                    torrent_age_year = (2000 if torrent_age_year < 50 else 1900) + torrent_age_year
                    month_numeric = self.months.index(torrent_age_month) + 1
                    torrent_age = u'{0}-{1}-{2}'.format(torrent_age_day, format(month_numeric, '02'), torrent_age_year).encode('ascii')
                    torrent_age = self.calculateAge(torrent_age)
                    torrent_detail_url = self.urls['detail'] % topic_id
                    torrent_url = self.urls['download'] % torrent_id

                    log.debug('Id: %s' % torrent_id)
                    log.debug('Title: %s' % torrent_name)
                    log.debug('Size: %s' % torrent_size)
                    log.debug('Forum: %s' % torrent_detail_url)
                    log.debug('Dl: %s' % torrent_url)
                    log.debug('Seed: %d' % torrent_seeders)
                    log.debug('Leech: %d' % torrent_leechers)
                    log.debug('Age: %s' % torrent_age)
                    
                    results.append({
                        'id': torrent_id,
                        'name': torrent_name,
                        'size': torrent_size,
                        'seeders': torrent_seeders,
                        'leechers': torrent_leechers,
                        'url': torrent_url,
                        'detail_url': torrent_detail_url,
                        'age': torrent_age,
                    })

            except:
                log.error('Failed to parse rutracker: %s' % (traceback.format_exc()))

    def getLoginParams(self):
        log.debug('Getting login params for rutracker')
        return {
            'login_username': self.conf('username'),
            'login_password': self.conf('password'),
            'login': '%E2%F5%EE%E4',
        }

    def loginSuccess(self, output):
        isLoginSuccessful = "post2url('login.php', {logout: 1});" in output.lower()
        log.debug('Checking login success for rutracker: %s' % isLoginSuccessful)
        return True

    loginCheckSuccess = loginSuccess
    
    # Input format: Translated Title / Original Title (year) rest/of[the]name
    # Output format: Original.Title.(year).[resolution].rest.of.the.name
    def formatTitle(self, raw_title):
        log.debug('Raw Title: %s' % raw_title)

        # Workaround for filtering 1080p and 720p by CouchPotato: BDRip is a source, not a video quality!
        title = raw_title.replace('BDRip', '')

        title_re = re.compile('(?:.*\/(.*)) \(.*\).*?\[((?:\d{4}\, ?)+)(\d{4})?(.*?)([0-9]{3,4}[pi])\](.*)')
        title_match = title_re.findall(title)
        if not title_match:
            return title
        name, years, year, additional1, resolution, additional2 = title_match[0]
        name = re.sub('[ \:]', '.', name)
        additional1 = re.sub('[ \:\,\+]', '.', additional1)
        additional2 = re.sub('[ \:\,\+]', '.', additional2)
        years = re.sub(' |, ?$', '', years).split(',')
        if year:
            years = years.append('year')
        log.debug('Found years: %s', years)
        if len(years) != 1:
            return title

        title = u'{0}.({1}).[{2}].{3}.{4}'.format(name, years[0], resolution, additional1, additional2)

        # Year search (should be always in '(' ')' )
        # p = re.compile('\[[0-9]{4}\,\]')
        # m = p.search(title)
        # if not m:
        #     # Can't format properly without a year anyway
        #     log.debug('Year not found in title')
        #     return title

        # year = m.group()

        # title_split = title.split(year)
                  
        # # Keep only last title name (nnm uses '/' to delimit title names in different languages)
        # title_only = title_split[0].split('/')[-1].strip()
        # title_only = re.sub('[ \:]', '.', title_only)
        
        # rest = re.sub('[^0-9a-zA-Z]+', '.', title_split[1])

        # # Resolution (1080p, 720p and etc)
        # p = re.compile('\.[0-9]{3,4}p(\.)?')
        # m = p.search(rest)
        # resolution = ''
        # if m:
        #     resolution = m.group().replace('.','')
        #     rest = rest.replace(resolution, '')
        #     resolution = '[' + resolution + ']'
            
        # title = title_only + '.' + year + '.' + resolution + '.' + rest

        title = re.sub('\.\.+', '.', title)
        title = re.sub('(^\.)|(\.$)', '', title)

        return title
    
    def calculateAge(self, date_str):
        return (datetime.today() - datetime.strptime(date_str, '%d-%m-%Y')).days
