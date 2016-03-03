import sys
import re
import nanocube
import datetime
import time

NC_PORT = 29513

adapter = nanocube.NanocubeAdapter('http://localhost', NC_PORT, 'brightkite')

next(sys.stdin) # skip header

for line in sys.stdin:

    url = line.strip()

    pattern = ''.join([
        '/[a-zA-Z]+/tile/tile/',
        '(?P<key>\d+)/',
        '(?P<x>\d+)/',
        '(?P<y>\d+)/',
        '(?P<zoom>\d+)/',
        '(?P<resolution>\d+)/',
        '(where/(?P<categoricals>[_a-zA-Z&0-9=]+)/)?',
        'tseries/tseries/',
        '(?P<start_date>\d+/\d+/\d+)/',
        '(?P<end_date>\d+/\d+/\d+)',
        ])

    match = re.match(pattern, url)
    if match:
        x = int(match.group('x'))
        y = int(match.group('y'))
        zoom = int(match.group('zoom'))
        resolution = int(match.group('resolution'))

        categoricals = {}
        if match.groupdict()['categoricals']:
            for condition in match.group('categoricals').split('&'):
                field, value = condition.split('=')
                categoricals[field] = value

        t0 = datetime.datetime.strptime(match.group("start_date"), "%Y/%m/%d")
        t1 = datetime.datetime.strptime(match.group("end_date"), "%Y/%m/%d")

        print adapter.query_tile_time_url(x, y, t0, t1, zoom, resolution, where=categoricals)
        continue

    raise Exception('unmatched query')

