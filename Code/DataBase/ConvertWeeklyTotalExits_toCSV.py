#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Converts weekly total BART Exits into Postgres relational database
"""

import csv
import os

from csv import reader


def DeleteFile(f):
    """
    Delete local file
    :param f: file fully qualified
    """
    if os.path.exists(f):
        os.remove(f)


# AVG_WEEK_EXITS_BART = 'K:\\OneDrive\\CSUGlobal\\MIS581\\PortfolioProject\\Data\\AVERAGE_WEEKDAY_EXITS.csv'
# averageweeklyexits = 'K:\\OneDrive\\CSUGlobal\\MIS581\\PortfolioProject\\Data\\AverageWeekdayExits.csv'


AVG_WEEK_EXITS_BART = '/Users/KenCeglia/OneDrive/CSUGlobal/MIS581/PortfolioProject/Data/AVERAGE_WEEKDAY_EXITS.csv'
averageweeklyexits = '/Users/KenCeglia/OneDrive/CSUGlobal/MIS581/PortfolioProject/Data/AverageWeekdayExits.csv'

with open(AVG_WEEK_EXITS_BART, 'r') as csv_file:
    csv_reader = reader(csv_file)
    # Passing the cav_reader object to list() to get a list of lists
    list_of_rows = list(csv_reader)
    for l in list_of_rows:
        print(l)

DeleteFile(averageweeklyexits)

with open(averageweeklyexits, mode='w', newline='') as aveweekexits:
    route_writer = csv.writer(aveweekexits, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    route_writer.writerow(['station', 'abbr', 'year', 'number'])
    for r in range(1, len(list_of_rows)):
        for y in range(2, len(list_of_rows[0])):
            lineRow = [list_of_rows[r][0], list_of_rows[r][1], list_of_rows[0][y], list_of_rows[r][y]]
            print(lineRow)
            route_writer.writerow([list_of_rows[r][0], list_of_rows[r][1], list_of_rows[0][y], list_of_rows[r][y]])
