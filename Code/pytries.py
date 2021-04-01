import requests
import numpy as np
import statistics
import csv
import os
from datetime import timedelta, date
import calendar



route_file_name = "route_trip_times.csv"
k_lic = "ZUKP-YX9M-Q5DQ-8UTV"
gen_lic = 'MW9S-E7SL-26DU-VV8V'
url = 'http://api.bart.gov/api/sched.aspx'
stationsURL = "https://api.bart.gov/api/stn.aspx"

class routeTime:
    origin = 'XXX'
    destination = 'XXX'
    tripTime = 0
    tripTimeString = '0'
    hour = 0
    origTimeMin = ''
    destTimeMin = ''
    origTimeDate = ''
    destTimeDate = ''
    fare = 0.0

routeTimeList = []

weekDays = {0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday",5:"Saturday",6:"Sunday"}
isoweekDays = {1:"Monday",2:"Tuesday",3:"Wednesday",4:"Thursday",5:"Friday",6:"Saturday",7:"Sunday"}

weekDaysTest = {0:"Monday"}


def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def daterange2(date1, date2):
    r = []
    for n in range(int ((date2 - date1).days)+1):
        r.append( date1 + timedelta(n) )
    return r

start_dt = date(2021, 3, 29)
end_dt = date(2021, 4, 4)
drange = daterange2(start_dt, end_dt)

for dd in drange:
    print(  calendar.day_name[dd.weekday()] )
    print ( dd.weekday() )
    print(dd.strftime("%m/%d/%y"))
    
for dt in daterange(start_dt, end_dt):
    print(dt.strftime("%Y-%m-%d"))
	