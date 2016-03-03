from utils import GET_json_as_obj
from datetime import datetime
from adapter import Adapter
import sys

debug = False

class HashedcubeAdapter(Adapter):

    def __init__(self, url, port, dataset):
        self.name = 'hashedcube ({})'.format(dataset)
        self.base_url = '{}:{}/'.format(url, port)
        self.dataset = dataset
        self.schema = GET_json_as_obj(self.base_url + '/rest/schema/' +
                                      dataset)

        self.start_time = datetime.strptime(self.schema['mindate'], "%Y-%m-%d")
        self.end_time = datetime.strptime(self.schema['maxdate'], "%Y-%m-%d")

    def query_tile_time(self, x, y, starttime, endtime, zoom, res):
        time0 = starttime.strftime("%Y/%m/%d")
        time1 = endtime.strftime("%Y/%m/%d")

        query_url = 'rest/query/brightkite/tile/0/{}/{}/{}/{}/tseries/tseries/{}/{}'
        whole_url = self.base_url + query_url
        url = whole_url.format(x, y, zoom, res, time0, time1)
        if debug: sys.stderr.write(url + '\n')
        try:
            results = GET_json_as_obj(url)
            return sum(int(x[3]) for x in results)
        except Exception, e:
            print url
            raise e

    def query_region_time(self, lat0, lon0, lat1, lon1, zoom, starttime, endtime):
        time0 = starttime.strftime("%Y/%m/%d")
        time1 = endtime.strftime("%Y/%m/%d")

        query_url = 'rest/query/brightkite/time/tseries/tseries/{}/{}/region/{}/0/{}/{}/{}/{}'
        whole_url = self.base_url + query_url
        url = whole_url.format(time0, time1, zoom, lat0, lon0, lat1, lon1)
        if debug: sys.stderr.write(url + '\n')
        try:
            results = GET_json_as_obj(url)
            return sum(int(x['k']) for x in results)
        except Exception, e:
            print url
            raise e

