from utils import timed
from hashedcube import HashedcubeAdapter
from nanocube import NanocubeAdapter
import random
import itertools
import time
import sys
import functools
from collections import defaultdict

# adapter = HashedcubeAdapter(url='http://localhost', port=8000, dataset='brightkite')
adapter = NanocubeAdapter(url='http://localhost', port=29513, dataset='brightkite')
DELAY = 0.005

def tile_time_resolution(adapter, time_steps=5, zoom=4, tile_samples=20, resolution=8):

    random.seed(1)
    all_coords = list(itertools.product(range(0, 2**zoom), range(0, 2**zoom)))
    coords = random.sample(all_coords, tile_samples)

    starts = ends = [float(x) / time_steps for x in range(time_steps)]

    query = timed(adapter.query_tile_time_percent)

    count = 0
    time_sum = 0
    for start, end, (x, y) in itertools.product(starts, ends, coords):
        if start >= end: continue
    
        time_v, count_v = query(x, y, zoom, resolution, start, end)
        count += 1
        time_sum += time_v.microseconds

        time.sleep(DELAY)
    
    average = time_sum / count / 1.e6
    print 'At resolution {} average time {}'.format(resolution, average)

def region_time(adapter, latlon_mag=160, latlon_step=160, time_steps=5, zoom=4):
    
    lat0s = lat1s = lon0s = lon1s = [float(x) / 180. for x in range(-latlon_mag, latlon_mag + latlon_step, latlon_step)]
    starts = ends = [float(x) / time_steps for x in range(time_steps)]
    
    query = timed(adapter.query_region_latlon_time_percent)
    
    count = 0
    time_sum = 0.
    for lat0, lat1, lon0, lon1, start, end in itertools.product(lat0s, lat1s, lon0s, lon1s, starts, ends):
        if lat0 >= lat1 or lon0 >= lon1 or start >= end: continue
                    
        time_v, count_v = query(lat0, lon0, lat1, lon1, zoom, start, end)
        count += 1
        time_sum += time_v.microseconds
    
        time.sleep(DELAY)

    print 'For regions, average time {}'.format(time_sum / count / 1.e6)

def user_tiles(adapter, count=5000):

    query = timed(adapter.query_tile_time_percent)

    time_sum = 0
    with open('./tiles.txt') as f:
        queries = (tuple(int(x) for x in line.split('/')[1:5]) for line in f)
        for zoom, resolution, x, y in itertools.islice(queries, count):
        
            time_v, count_v = query(x, y, zoom, resolution, 0.0, 1.0)
            time_sum += time_v.microseconds

            time.sleep(DELAY)
        
        average = time_sum / count / 1.e6
        print 'User queries: average time {}'.format(average)


for benchmark in [tile_time_resolution, region_time, user_tiles]:
    benchmark(adapter)
