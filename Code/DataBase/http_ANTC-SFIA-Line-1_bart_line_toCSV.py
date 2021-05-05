#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Adds Antioch SFIA line to Postgres tables
"""
import csv
import os

import bart

lines_file_name = "K:\\OneDrive\\CSUGlobal\\MIS581\\PortfolioProject\\Data\\bart_line_1.csv"
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
    print("Number of Stations in Line :", len(routeLines))
    print("Completed")