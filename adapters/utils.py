from datetime import datetime, timedelta
import json
import sys
import urllib2
import functools

def coords_to_path(x, y, zoom):
    ''' List of quadtree steps in {0,1,2,3} from tile x, y, zoom '''

    path = []
    while zoom > 0:
        path.append((x % 2) * 2 + (y % 2))
        x /= 2
        y /= 2
        zoom -= 1
    path.reverse()
    return path


def generic_range(start, end, step):
    now = start
    while now < end:
        yield now
        now += step


def GET_json_as_obj(url):
    url = url.replace(' ', '')
    return json.loads(''.join(urllib2.urlopen(url).readlines()))


def timed(f):
    @functools.wraps(f)
    def timed_f(*args, **kwargs):
        start = datetime.now()
        ret_val = f(*args, **kwargs)
        return (datetime.now() - start, ret_val)

    return timed_f
