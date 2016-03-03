import sys
import datetime

# sort by date in csv field 1. Only tested on brightkite.

data = []
for line in sys.stdin:

    line = line.strip()
    fields = line.split(',')

    # Just bail if things don't look right.
    try:
        date = datetime.datetime.strptime(fields[1], '%Y-%m-%dT%H:%M:%SZ')
        data.append((date, line))
    except:
        pass

data.sort()

for _, line in data:
    print line

