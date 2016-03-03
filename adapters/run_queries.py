import sys
import urllib2
import datetime
import time

# Time every query on stdin. 


next(sys.stdin) # skip header

for line in sys.stdin:
    url = line.strip()

    sys.stderr.write(url + '\n')

    start = datetime.datetime.now()

    try:
        urllib2.urlopen(url).readlines()
    except Exception, e:
        print url
        raise e

    end = datetime.datetime.now()

    ms = (end - start).microseconds / 1000
    print '{},{}'.format(ms, url)

    # Running queries too fast kills the socket. Not sure why.
    # The queries are mostly on the order of 0.001 sec, so this is a bottleneck
    # right now
    time.sleep(0.005)
