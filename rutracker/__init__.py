from .main import rutracker

def autoload():
  return rutracker()

config = [{
  'name': 'rutracker',
  'groups': [
    {
      'tab': 'searcher',
      'list': 'torrent_providers',
      'name': 'rutracker',
      'description': '<a href="https://rutracker.org">rutracker.org</a>',
      'wizard': True,
      'icon': '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',
      'options': [
        {
          'name': 'enabled',
          'type': 'enabler',
          'default': False,
        },
        {
          'name': 'username',
          'default': '',
        },
        {
          'name': 'password',
          'default': '',
          'type': 'password',
        },
        {
          'name': 'seed_ratio',
          'label': 'Seed ratio',
          'type': 'float',
          'default': 1,
          'description': 'Will not be (re)moved until this seed ratio is met.',
        },
        {
          'name': 'seed_time',
          'label': 'Seed time',
          'type': 'int',
          'default': 48,
          'description': 'Will not be (re)moved until this seed time (in hours) is met.',
        },
        {
          'name': 'extra_score',
          'advanced': True,
          'label': 'Extra Score',
          'type': 'int',
          'default': 0,
          'description': 'Starting score for each release found via this provider.',
        }
      ],
    },
  ],
}]
