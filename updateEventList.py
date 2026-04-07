import os
from datetime import datetime, timedelta, timezone
from ligo.gracedb.rest import GraceDb

client = GraceDb()

# O4a
# UTC time: 2023/05/24 15:00:00 => GPS = 1368975618
#gpstime_start = 1368975618
#file_evelist  = "dataO4a.txt"

# O4b
# UTC time: 2024/04/10 15:00:00 => GPS = 1396796418
#gpstime_start = 1396796418
#file_evelist  = "dataO4b.txt"

# O4c
# UTC time: 2025/01/28 17:00:00 => GPS = 1422118818
gpstime_start = 1422118818
file_evelist  = "dataO4c.txt"

# Should be much later than the actual end of O4(b) but a while before O5(a)...
# UTC time: 2026/01/01 00:00:00 => GPS = 1451260818
gpstime_end = 1451260818

# Get event data with ADVOK label.
superevent_iterator = client.superevents('label: ADVOK gpstime: {} .. {}'.format(gpstime_start, gpstime_end))

# Export to a file
with open(file_evelist, 'w') as file:
    for superevent in superevent_iterator:
        file.write(superevent['superevent_id'] + '\n')
