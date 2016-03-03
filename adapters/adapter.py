from datetime import datetime, timedelta

class Adapter:

    def _interpolate_time(self, t0, t1):
        total_seconds = (self.end_time - self.start_time).total_seconds()
        t0_seconds = total_seconds * t0
        t1_seconds = total_seconds * t1
        start = self.start_time + timedelta(seconds=t0_seconds)
        end = self.start_time + timedelta(seconds=t1_seconds)
        return (start, end)

    def query_tile_time_percent(self, x, y, zoom, res, t0, t1):
        start, end = self._interpolate_time(t0, t1)
        return self.query_tile_time(x, y, start, end, zoom, res)

    def query_region_latlon_time_percent(self, lat0, lon0, lat1, lon1, zoom, t0, t1):
        start, end = self._interpolate_time(t0, t1)
        return self.query_region_time(lat0, lon0, lat1, lon1, zoom, start, end)
