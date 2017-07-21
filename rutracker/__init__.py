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
      'icon': 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAABGlBMVEUAAADV1dXp6enr6+v///+/v7/i4uLu7u7d3d31lKnvWHje3t7j4+Pg4ODt7e329vbrM1rpEkDrJ1F+fn7+/v7IyMjQXXb5ucdJSUqYmJhf1DfnIUz0iqG8vLzY2Nil54+V4nuA3WE/yxCmpqbQN1j0tcP2oLPf39+xsbHDw8OI32uZmZ49PT5kZWXS0tLh4eH8/PxBzBOi5oxsbGwMEVYcJJlTWr1scrvU1NSioqJo1kOh5oorLEYLFZMRHs0SIOGztuvPz8+kpKTx8fGurq7Z9c9paWkSIelXV1fMzM6goKCampqUlJSCgoLz8/MZJ+kqOOpcZ/Cbofbc3NyIiIhATe3d3/zb29tOTk5ycnJ8fHyKiorq6urLy8vuTXI1AAAAAXRSTlMAQObYZgAAAAFiS0dEBI9o2VEAAAAHdElNRQfYAx8VHw86a3tvAAAAx0lEQVQY02NggAJGJgZkwMzCwsrGjiTAwcnFwsLCzQPl8vLxCwgKCrEIc0D4PCKiYoKCguISkjANUnyS0oJCMpKyII6cvIKiEouyiiqLmroGSECTRQkItFi0dXT1lHmBAvoGhkpKRizGJqZm5haWIBtYrKyVWHRsbO3sHRydQE5yVnZxZXEzs3d3Z/HwBApYeHn7+PpJsPkHBAbxOAIF+IJ5g5U1Q3hCw4BOlYU5hDtcjz/CLTJKFuEZx2ivcB71GIQAbyzUHwBnIRen+TqAhgAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAxNy0wNy0yMlQwMDowMDo1MyswMjowMNUDgxIAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMDgtMDMtMzFUMjE6MzE6MTUrMDI6MDAJ85C+AAAAAElFTkSuQmCC',
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
