import requests
import numpy as np
import statistics
import csv
import os
from datetime import timedelta, date
import datetime as dt
import calendar
import bart


lines_file_name = "bart_line_1.csv"
line_number = '1'

if os.path.exists(lines_file_name):
    os.remove(lines_file_name)

try:
    with open(lines_file_name, mode='w', newline='') as routetimes_file:
        route_writer = csv.writer(routetimes_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        route_writer.writerow(['number', 'station'])
        routeLines = bart.GetBARTLine(line_number)
        for r in routeLines:
            lineRow = [r['number'], r['station']]
            route_writer.writerow( lineRow )
except (Exception) as e:
    print(e)
finally:
    print("Completed")