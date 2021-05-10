#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Helper function to execute Python code needed for quering BART API
    and Postgres input-outputs
"""
import os

import psycopg2
import requests

gen_lic = 'MW9S-E7SL-26DU-VV8V'
bart_lic = gen_lic
url = 'http://api.bart.gov/api/route.aspx?'


def checkkey(dic, key):
    """
    Check if key exist in dictionary
    :param dic: dictionary to check
    :param key: key to check in dictionary
    :return: True or False if key exists in dict
    """
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
    """
    Query BART API for stations in line
    :param bartLine: BART line to get station list for
    :return: list of BART stations
    """
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
            if checkkey(rj, ['root', 'routes', 'route', 'config', 'station']) == True:
                routeSummary = route.json()['root']['routes']['route']
                routeDetails = route.json()['root']['routes']['route']['config']['station']
                for r in routeDetails:
                    rline = {'abbr': routeSummary['abbr'], 'routeID': routeSummary['routeID'],
                             'origin': routeSummary['origin'], 'dest': routeSummary['destination'],
                             'number': routeSummary['number'], 'station': r}
                    lineReturn.append(rline)
    except (Exception) as e:
        print("Error getting line: {}".format(str(e)))
    finally:
        return lineReturn


def GetBARTLines():
    """
    Query BART API For all stations in all lines
    :return: List of lines and station in lines
    """
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
    except (Exception) as e:
        print("Error geting all lines: {}".format(str(e)))
    finally:
        return routeLinesReturn, routeFailures


def DeleteFile(f):
    """
    Delete a local file
    :param f: file name fully qualified
    """
    if os.path.exists(f):
        os.remove(f)


def GetStationList():
    """
    Query BART API for list of all stations and details
    :return: List of all BART stations
    """
    stationsURL = "https://api.bart.gov/api/stn.aspx"
    paramsStation = dict(
        cmd='stns',
        key=bart_lic,
        json='y'
    )
    bartStationList = requests.get(url=stationsURL, params=paramsStation).json()['root']['stations']['station']
    return bartStationList


def PGBart(query):
    """
    Postgres query helper function for remote PG server
    :param query: query string
    :return: Postgres query results in list
    """
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


def PGBartLocal(query):
    """
    Postgres query helper function for local PG installation
    :param query: query string
    :return: Postgres query results in list
    """
    try:
        query_results = []
        conn = psycopg2.connect(host="localhost", port=5432, database="bartridership", user="postgres",
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
