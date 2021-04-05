import requests
import numpy as np
import statistics
import csv
import os
from datetime import timedelta, date
import calendar
import psycopg2

k_lic = "ZUKP-YX9M-Q5DQ-8UTV"
gen_lic = 'MW9S-E7SL-26DU-VV8V'
bart_lic = k_lic
url = 'http://api.bart.gov/api/route.aspx?'


def checkkey(dic, key):
    r = False
    try:
        if type(key is list):
            checkDict = dic
            for k in key:
                if k in checkDict:
                    r = True
                    checkDict = checkDict[k]
                else:
                    r = False
    except(Exception) as e:
        r = False
    finally:
        return r


def GetBARTLine(bartLine):
    try:
        lineReturn = []
        urlRoute = 'https://api.bart.gov/api/route.aspx?'
        paramsRoute = dict(
            cmd='routeinfo',
            route=bartLine,
            key=bart_lic,
            json='y'
        )
        route = requests.get(url=urlRoute, params=paramsRoute)
        statusCode = route.status_code
        if statusCode == 200:
            rj = route.json()
            if checkkey(rj, ['root','routes','route','config','station']) == True:
                routeSummary = route.json()['root']['routes']['route']
                routeDetails = route.json()['root']['routes']['route']['config']['station']
                for r in routeDetails:
                    rline = { 'abbr': routeSummary['abbr'], 'routeID':routeSummary['routeID'],
                              'origin':routeSummary['origin'], 'dest':routeSummary['destination'],
                              'number':routeSummary['number'], 'station': r }
                    lineReturn.append(rline)
    except (Exception) as e:
        print("Error getting line: {}".format(str(e)))
    finally:
        return lineReturn


def GetBARTLines():
    try:
        routeLinesReturn = []
        routeFailures = []
        url = 'http://api.bart.gov/api/route.aspx?'
        urlRoute = 'https://api.bart.gov/api/route.aspx?'
        params = dict(
            cmd='routes',
            key=bart_lic,
            json='y'
        )
        lines = requests.get(url=url, params=params)
        statusCode = lines.status_code
        if statusCode == 200:
            lineDetails = lines.json()['root']['routes']['route']
            for line in lineDetails:
                routeSummary = GetBARTLine(line['number'])
                if len(routeSummary) > 0:
                    routeLinesReturn.extend(routeSummary)
                else:
                    routeFailures.append(line)
            else:
                routeFailures.append(line)
    except (Exception) as e:
        print("Error geting all lines: {}".format(str(e)))
    finally:
        return routeLinesReturn, routeFailures


def DeleteFile(f):
    if os.path.exists(f):
        os.remove(f)


def PGBart(query):
    try:
        query_results = []
        conn = psycopg2.connect(host="10.0.0.206", port=5432, database="bartridership", user="postgres",
                                password="minden12k")
        cur = conn.cursor()
        cur.execute(query)
        query_results = cur.fetchall()
        # Close the cursor and connection to so the server can allocate
        # bandwidth to other requests
        cur.close()
        conn.close()
    except (Exception, psycopg2.Error) as e:
        print("Error in running the query: {}".format(str(e)))
    finally:
        return query_results
