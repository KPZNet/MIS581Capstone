import requests
import numpy as np
import statistics
import csv
import os
from datetime import timedelta, date
import datetime as dt
import calendar
import bart


all_lines_file_name = "K:\\OneDrive\\CSUGlobal\\MIS581\\PortfolioProject\\Data\\all_bart_lines.csv"

bart.DeleteFile(all_lines_file_name)

try:
    with open(all_lines_file_name, mode='w', newline='') as routetimes_file:
        route_writer = csv.writer(routetimes_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        route_writer.writerow(['abbr', 'routeID','origin', 'dest','number', 'station'])
        routeLines, routeFailures = bart.GetBARTLines()
        for r in routeLines:
            lineRow = [r['abbr'], r['routeID'],r['origin'], r['dest'], r['number'], r['station']]
            route_writer.writerow(lineRow)
except (Exception) as e:
    print(e)
finally:
    print("Total Lines  ", len(routeLines))
    print("Total Failures  ", len(routeFailures))
    print(routeFailures)
    print("Completed")