from typing import List, Any

import requests
import numpy as np
import statistics
import csv
import os
from datetime import datetime
from datetime import timedelta, date
import datetime as dt
import calendar
import bart


route_file_name = "route_trip_times.csv"
k_lic = "ZUKP-YX9M-Q5DQ-8UTV"
gen_lic = 'MW9S-E7SL-26DU-VV8V'
bart_lic = k_lic
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

def PrintTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

def DateRangeList(date1, date2):
    r = []
    for n in range(int ((date2 - date1).days)+1):
        r.append( date1 + timedelta(n) )
    return r

start_dt = date(2021, 3, 28)
end_dt = start_dt + timedelta(1) # date(2021, 4, 4)
weekDayList = DateRangeList(start_dt, end_dt)

hours = {i : dt.time(i).strftime('%I:00 %p') for i in range(24)}

def FillRouteTime(t, hour):
    ro = routeTime()
    ro.origin = t['@origin']
    ro.destination = t['@destination']
    ro.tripTime = int( t['@tripTime'] )
    ro.tripTimeString = t['@tripTime']
    ro.hour = hour
    ro.origTimeMin = t['@origTimeMin']
    ro.origTimeDate = t['@origTimeDate']
    ro.destTimeMin = t['@destTimeMin']
    ro.destTimeDate = t['@destTimeDate']
    ro.fare = t['@fare']
    return ro

def GetMeanTime(timeList):
    tot = 0
    sz = len(timeList)
    if sz > 0:
        for t in timeList:
            minutes = t['@tripTime']
            tot = tot + int(minutes)
    else:
        sz = 1
    return tot/sz

def GetTime(t):
    time = int(t['@tripTime'])
    return time
      

paramsStation = dict(
    cmd='stns',
    key=bart_lic,
    json='y'
)

bartStationList = requests.get(url=stationsURL, params=paramsStation).json()['root']['stations']['station']

stList_dest = list(map(lambda x: x['abbr'], bartStationList ) )
stList_orig = list(map(lambda x: x['station'], bart.GetBARTLine('1') ) )

#stList_orig = ['PITT']

if os.path.exists(route_file_name):
    os.remove(route_file_name)

PrintTime()

with open(route_file_name, mode='w', newline='') as routetimes_file:
    route_writer = csv.writer(routetimes_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    route_writer.writerow(['origin', 'destination', 'tripTime', 'hour', 
        'origTimeMin', 'origTimeDate', 'destTimeMin', 'destTimeDate', 'dow', 'day', 'fare'])

    for day in weekDayList:
        for hour in hours:
            for origin in stList_orig:
                for dest in stList_dest:
                    if origin != dest:
                        dow = day.weekday()
                        dayString = calendar.day_name[day.weekday()]
                        dateString = day.strftime("%m/%d/%y")
                        print('Acquiring: ', origin, ":", dest, ":", " day: ", dow, " wd: ", dayString, "Hour: ", hour)
                        paramsRoute = dict(
                            cmd='arrive',
                            orig=origin,
                            dest=dest,
                            time=hours[hour],
                            date=dateString,
                            key=gen_lic,
                            b='0',
                            a='0',
                            json='y'
                        )
                        retRoute = requests.get(url=url, params=paramsRoute)
                        statusCode =  retRoute.status_code
                        if statusCode == 200:
                            routeDetails = retRoute.json()['root']['schedule']['request']['trip']
                            if type(routeDetails) is dict:
                                rc = FillRouteTime(routeDetails, hour)
                                routeTimeList.append(rc)
                                print('\t', 'Trip time: ', rc.tripTime, " : Dest Time :  ", rc.destTimeMin)
                                route_writer.writerow([rc.origin, rc.destination, rc.tripTime, 
                                hour, rc.origTimeMin, rc.origTimeDate, rc.destTimeMin, rc.destTimeDate, 
                                dow, dayString,rc.fare])

PrintTime()

