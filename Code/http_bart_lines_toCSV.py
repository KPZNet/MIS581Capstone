import requests
import numpy as np
import statistics
import csv
import os
from datetime import timedelta, date
import datetime as dt
import calendar


lines_file_name = "bart_lines.csv"
k_lic = "ZUKP-YX9M-Q5DQ-8UTV"
gen_lic = 'MW9S-E7SL-26DU-VV8V'
url = 'http://api.bart.gov/api/route.aspx?'

params = dict(
    cmd='routes',
    key=gen_lic,
    json='y'
)

if os.path.exists(lines_file_name):
    os.remove(lines_file_name)

try:
    lines = requests.get(url=url, params=params)
    statusCode =  lines.status_code
    if statusCode == 200:
        lineDetails = lines.json()['root']['routes']['route']
        with open(lines_file_name, mode='w', newline='') as routetimes_file:
            route_writer = csv.writer(routetimes_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            route_writer.writerow(['name', 'abbr', 'routeID', 'number', 'hexcolor', 'color', 'direction'])
            for bline in lineDetails:
                route_writer.writerow([bline['name'], bline['abbr'], bline['routeID'], bline['number'], bline['hexcolor'], bline['color'], bline['direction']])

except (Exception) as e:
    print(e)

finally:
    print("complete")