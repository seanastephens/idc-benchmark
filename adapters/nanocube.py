from utils import GET_json_as_obj, coords_to_path
from datetime import datetime, timedelta
from adapter import Adapter
import urllib2


class NanocubeAdapter(Adapter):

    def __init__(self, url, port, dataset):
        self.name = 'nanocube ({})'.format(dataset)
        self.base_url = '{}:{}/'.format(url, port)
        (self.base_url + '/schema')
        self.schema = GET_json_as_obj(self.base_url + '/schema')

        metadata = self.schema['metadata']
        time_data = next(x for x in metadata if x['key'] == 'tbin')
        start_date, start_time, bin_size = time_data['value'].split('_')
        start = start_date + ' ' + start_time

        self.start_time = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        
        if bin_size[-1] == 's':
            self.bin_size = timedelta(seconds=int(bin_size[:-1]))
        else:
            raise ValueError('bin_size unrecognized: {}'.format(bin_size))

        total = int(GET_json_as_obj(self.base_url + 'count')['root']['val'])
        start = self.start_time
        steps = reversed([timedelta(hours=2**i) for i in range(0, 13)])
        end = start

        for step in steps:
            while self.query_tile_time(0, 0, start, end, 0, 1) < total:
                end += step
            end -= step
        end += step

        self.end_time = end


    def datetime_to_nanocube_bin(self, time):
        diff = time - self.start_time
        return max(0, int(diff.total_seconds() / self.bin_size.total_seconds()))

    def query_tile_time_url(self, x, y, starttime, endtime, zoom, res, where={}):
        time0 = self.datetime_to_nanocube_bin(starttime)
        time1 = self.datetime_to_nanocube_bin(endtime)

        query_url = 'count.r("time",interval({},{})).a("location",dive({},{}))'
        whole_url = self.base_url + query_url
        url = whole_url.format(time0, time1, coords_to_path(x, y, zoom), res)
        for field, value in where.items():
            url += '.r("{}",set({}))'.format(field, value)
        return url.replace(' ', '')

    def query_tile_time(self, x, y, starttime, endtime, zoom, res, where={}):
        url = self.query_tile_time_url(x, y, starttime, endtime, zoom, res, where=where)

        results = GET_json_as_obj(url)["root"]

        if "children" in results:
            return sum(int(x['val']) for x in results["children"])
        return 0

    def query_region_time(self, lat0, lon0, lat1, lon1, zoom, starttime, endtime):
        time0 = self.datetime_to_nanocube_bin(starttime)
        time1 = self.datetime_to_nanocube_bin(endtime)

        step = 24 * 7 # hard coded to match hc
        num_bins = int(((time1 - time0) / step) + 0.5)

        point_seq = [lon0,lat0,lon0,lat1,lon1,lat1,lon1,lat0]

        query_url1 = 'count.r("location",mercator_mask("{}",{}))'
        query_url2 = '.r("time",mt_interval_sequence({},{},{}))'
        query_url1 = query_url1.format(','.join([str(float(x)) for x in point_seq]), 10) # no idea about this last param
        query_url2 = query_url2.format(time0, step, num_bins)

        url = self.base_url + query_url1 + query_url2

        results = GET_json_as_obj(url)["root"]

        if "children" in results:
            return sum(int(x['val']) for x in results["children"])

        return 0
