import requests
import numpy as np
import statistics
import csv
import os
from datetime import timedelta, date
import datetime as dt
import calendar
import bart


lines_file_name = "all_bart_lines.csv"

if os.path.exists(lines_file_name):
    os.remove(lines_file_name)

try:
    with open(lines_file_name, mode='w', newline='') as routetimes_file:
        route_writer = csv.writer(routetimes_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        route_writer.writerow(['name', 'number', 'orig', 'dest'])
        routeLines = bart.GetBARTLines()
        for r in routeLines:
            if routeLines[0] != r:
                route_writer.writerow(r)
except (Exception) as e:
    print(e)
finally:
    print("Completed")