# -*- coding: utf-8 -*-
""":mod:`noomlib`
~~~~~~~~~~~~~~~~~

"""
import requests
try:
    import simplejson as json
except ImportError:
    import json
import gpxpy
from datetime import datetime

__all__ = 'Noom', 'Track', 'exercise_types', 'exercise_type_strings'

NOOM_URL = 'http://www.noom.com/cardiotrainer/tracks.php'
NOOM_EXPORT_URL = 'http://www.noom.com/cardiotrainer/exporter/export_gpx.php'
NOOM_DATE_FORMAT = '%A<br/>%b.%d, %Y<br/>%I:%M %p'


class Noom(object):
    """Noom data reader
    
    >>> noom = Noom()
    >>> noom.auth('access', 'code')
    >>> for track in noom.tracks:
            pass
    """

    def __init__(self):
        self.session = requests.Session()

    def auth(self, access, code):
        """Authroize Noom data page

        :param access:
        :type acceess: :class:`basestring`
        :param code:
        :type code: :class:`basestring`

        """
        data = dict(access=access, code=code)
        self.session.post(NOOM_URL, data=data)

    @property
    def tracks(self):
        """Get all stored noom track datas

        :returns: Wrapped :class:`Track` datas
        :trype: :class:`generator`

        """
        offset = 0
        while True:
            resp = self.session.get(NOOM_URL, params=dict(offset=offset))
            html = resp.text
            data = html.split('var trackData = ')[1]
            data = data.split('; </script>')[0]
            data = dict(json.loads(data))
            length = len(data.keys())
            if not length:
                break
            # TODO: data sort
            strptime = datetime.strptime
            items = sorted(data.iteritems(), cmp=cmp_time, reverse=True)
            for track_id, track_data in items:
                signature = track_data['trackIdSignature']
                params = dict(trackId=track_id, signature=signature)
                gpx = self.session.get(NOOM_EXPORT_URL, params=params).text
                yield Track(track_data=track_data, gpx=gpx)
            offset += length


def cmp_time(x, y):
    delta = datetime.strptime(x[1]['date'], NOOM_DATE_FORMAT) - \
            datetime.strptime(y[1]['date'], NOOM_DATE_FORMAT)
    sec = delta.total_seconds()
    if sec < 0:
        return -1
    elif sec > 0:
        return 1
    return 0

exercise_types = [
    'exercise_type_unspecified',
    'exercise_type_running',
    'exercise_type_biking',
    'exercise_type_walking',
    'exercise_type_skiing',
    'exercise_type_driving',
    'exercise_type_horseback_riding',
    'exercise_type_kayaking',
    'exercise_type_skating',
    'skating_indoor',
    'exercise_type_rollerblading',
    'rollerblading_indoor',
    'exercise_type_snowboarding',
    'exercise_type_hiking',
    'exercise_type_team_sports',
    'team_sports_indoor',
    'exercise_type_aerobics',
    'exercise_type_swimming',
    'swimming_indoor',
    'exercise_type_dancing',
    'exercise_type_pilates',
    'exercise_type_weight_lifting',
    'exercise_type_yoga',
    'exercise_type_elliptical',
    'running_treadmill',
    'walking_treadmill',
    'biking_stationary',
    'exercise_type_boxing',
    'skiing_cross_country',
    'biking_mountain_bike',
    'exercise_type_stairs',
    'stairs_stepper',
    'exercise_type_jumprope',
    'exercise_type_rowing',
    'rowing_machine',
    'biking_spinning',
    'exercise_type_nordic_walking',
    'racquet_ball',
    'racquet_squash',
    'racquet_tennis',
    'exercise_type_custom',
]

exercise_type_strings = {
    0: 'UNSPECIFIED',
    1: 'Running',
    2: 'Biking',
    3: 'Walking',
    4: 'Skiing',
    5: 'Driving',
    6: 'Horseback riding',
    7: 'Kayaking',
    8: 'Skating',
    9: 'Skating, indoor',
    10: 'Rollerblading',
    11: 'Rollerblading, indoor',
    12: 'Snowboarding',
    13: 'Hiking',
    14: 'Team sports',
    15: 'Team sports, indoor',
    16: 'Aerobics',
    17: 'Swimming',
    18: 'Swimming, indoor',
    19: 'Dancing',
    20: 'Pilates',
    21: 'Weight lifting',
    22: 'Yoga',
    23: 'Elliptical',
    24: 'Running, treadmill',
    25: 'Walking, treadmill',
    26: 'Biking, stationary',
    27: 'Boxing',
    28: 'Skiing, cross contry',
    29: 'Biking, mountain bike',
    30: 'Stairs',
    31: 'Stairs, stepper',
    32: 'Jumprope',
    33: 'Rowing',
    34: 'Rowing, machine',
    35: 'Biking, spinning',
    36: 'Nordic walking',
    37: 'Racquet, ball',
    38: 'Racquet, squash',
    39: 'Racquet, tennis',
    40: 'Custom',
}


class Track(object):
    """Noom track data
    
    """

    def __init__(self, track_data, gpx):
        self.track_data = track_data
        self.raw_gpx = gpx
        self._gpx = None

    @property
    def gpx(self):
        self._gpx = self._gpx or gpxpy.parse(self.raw_gpx)
        return self._gpx

    @property
    def raw_exercise_type(self):
        return self.track_data.get('exercise_type',
                                   'exercise_type_unspecified')

    @property
    def exercise_type(self):
        return exercise_types.index(self.raw_exercise_type)

    @property
    def exercise(self):
        return exercise_type_strings[self.exercise_type] 

    @property
    def distance(self):
        return self.track_data.get('distance', 0)

    @property
    def max_speed(self):
        return self.track_data.get('maxSpeed', 0)

    @property
    def avg_speed(self):
        return self.track_data.get('avgSpeed', 0)

    @property
    def calories(self):
        return self.track_data.get('calories', 0)

    @property
    def duration(self):
        ftr = 3600, 60, 1
        times = self.track_data.get('duration', '00:00:00')
        times = (int(x) for x in times.split(':'))
        return sum((x * y) for x, y in zip(ftr, times))

    @property
    def climb(self):
        return self.track_data.get('climb', 0)

    @property
    def date(self):
        return self.gpx.time


if __name__ == '__main__':
    import os

    access_code = os.environ.get('NOOM_ACCESS_CODE')
    if not access_code:
        raise TypeError('Not set environment variable `NOOM_ACCESS_CODE`')
    access, code = access_code.split('-')
    noom = Noom()
    noom.auth(access, code)
    for i, t in enumerate(noom.tracks):
        print "%4d. %s" % (i + 1, t.gpx.description)
        print '\tdate:', t.date
        print '\texercise type:', t.exercise
        print '\tduration:', t.duration
        print '\tsppeds (max/avg/climb):', t.max_speed, t.avg_speed, \
              t.distance, t.climb
        print '\tcalories:', t.calories
        for tr in t.gpx.tracks:
            for s in tr.segments:
                for p in s.points:
                    print '\t', p.latitude, '\t', p.longitude,
                    print '\t', p.elevation
        print
        raw_input('\tpause. ')
