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
url = 'http://api.bart.gov/api/route.aspx?'


def GetBARTLine(bartLine):
    try:
        lineReturn = []
        urlRoute = 'https://api.bart.gov/api/route.aspx?'
        paramsRoute = dict(
            cmd='routeinfo',
            route = '1',
            key=k_lic,
            json='y'
        )
        paramsRoute['route'] = bartLine
        route = requests.get(url=urlRoute, params=paramsRoute)
        statusCode = route.status_code
        if statusCode == 200:
            rj = route.json()
            routeSummary = route.json()['root']['routes']['route']
            routeDetails = route.json()['root']['routes']['route']['config']['station']
            for r in routeDetails:
                if routeDetails[0] != r:
                    rline = [ routeSummary['abbr'], routeSummary['number'], routeDetails[0], r]
                    lineReturn.append( rline )
    except (Exception) as e:
        print("Error in running the query: {}".format(str(e)))
    finally:
        return lineReturn

def GetBARTLines():
    try:
        routeLinesReturn = []
        url = 'http://api.bart.gov/api/route.aspx?'
        urlRoute = 'https://api.bart.gov/api/route.aspx?'
        params = dict(
            cmd='routes',
            key=k_lic,
            json='y'
        )
        paramsRoute = dict(
            cmd='routeinfo',
            route = '1',
            key=k_lic,
            json='y'
        )
        lines = requests.get(url=url, params=params)
        statusCode =  lines.status_code
        if statusCode == 200:
            lineDetails = lines.json()['root']['routes']['route']
            for line in lineDetails:
                paramsRoute['route'] = line['number']
                route = requests.get(url=urlRoute, params=paramsRoute)
                statusCode = route.status_code
                if statusCode == 200:
                    rj = route.json()
                    routeDetails = route.json()['root']['routes']['route']['config']['station']
                    for r in routeDetails:
                        if routeDetails[0] != r:
                            rline = [ line['abbr'], line['number'], routeDetails[0], r]
                            routeLinesReturn.append( rline )
    except (Exception) as e:
        print("Error in running the query: {}".format(str(e)))
    finally:
        return routeLinesReturn


def DeleteFile(f):
    if os.path.exists(f):
        os.remove(f)

def PGBart(query):
    try:
        query_results = []
        conn = psycopg2.connect(host="10.0.0.206", port = 5432, database="bartridership", user="postgres", password="minden12k")
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