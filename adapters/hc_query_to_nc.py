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
        '^',
        '/[a-zA-Z]+/',
        '(',
            'tile/tile/(?P<tile_clause>\d+/\d+/\d+/\d+/\d+)/',
        '|',
            'where/(?P<where_clause>[_a-zA-Z&0-9=]+)/',
        '|',
            'tseries/tseries/(?P<start_date>\d+/\d+/\d+)/(?P<end_date>\d+/\d+/\d+)/?',
        ')*'
        '$'
        ])

    match = re.match(pattern, url)
    if match:
        clauses = match.groupdict()
        tile_clause = clauses["tile_clause"]
        if tile_clause:
            key, x, y, zoom, resolution = map(int, tile_clause.split('/'))

        where = {}
        where_clause = clauses["where_clause"]
        if where_clause:
            for condition in where_clause.split('&'):
                field, value = condition.split('=')
                where[field] = value

        start_date = clauses["start_date"]
        end_date = clauses["end_date"]
        if start_date and end_date:
            t0 = datetime.datetime.strptime(start_date, "%Y/%m/%d")
            t1 = datetime.datetime.strptime(end_date, "%Y/%m/%d")

        print adapter.query_tile_time_url(x, y, t0, t1, zoom, resolution, where=where)
        continue

    raise Exception('unmatched query')

