import requests
import numpy as np
import statistics
import csv
import os
from datetime import timedelta, date
import datetime as dt
import calendar
import bart


file_name = "all_stations.csv"

bart.DeleteFile(file_name)

try:
    with open(file_name, mode='w', newline='') as routetimes_file:
        route_writer = csv.writer(routetimes_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        route_writer.writerow(['name', 'abbr', 'gtfslat', 'gtfslong', 'city', 'id'])
        stations = bart.GetStationList()
        i = 1
        for r in stations:
            lineRow = [r['name'], r['abbr'],r['gtfs_latitude'],r['gtfs_longitude'],r['city'],i]
            route_writer.writerow(lineRow)
            i = i + 1
except (Exception) as e:
    print(e)
finally:
    print("Completed")