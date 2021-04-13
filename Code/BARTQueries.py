import requests
import numpy as np
import statistics
import csv
import os
from datetime import timedelta, date
import calendar
import psycopg2


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

def PGBartLocal(query):
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


def GetWeeklyRidersToEMBRAtHour():
    global smoothData, scal
    query = """
                
        select avg(cast(riders as double precision)), dest, 
            extract(DOW from depart_date) as dow,
            extract(WEEK from depart_date) as week
        from hourlystationqueue
        where
                extract(ISODOW from depart_date) in (1,2,3,4,5)
          AND
                dest = 'EMBR'
          and
                depart_hour = 7
        
          and
                extract(YEAR from depart_date) in (2013,2014,2015,2017,2018)
        group by dest,  extract(WEEK from depart_date), 
                        extract(DOW from depart_date)
                
    """
    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x[0], dat))
    return plotdata

def GetYearlyRiderDistFromPITT2014():
    global smoothData, scal
    query = """
                
    select SUM(riders) as riders, source, dest
    from hourlystationqueue
    where
            extract(ISODOW from depart_date) in (1,2,3,4,5)
      AND
            source = 'PITT'
      AND depart_hour = 7
      and extract(YEAR from depart_date) = 2014
    group by source, dest
                
    """

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    return plotdata

def GetYearlyRiderDistFromPITT2015():
    global smoothData, scal
    query = """
                                
    select SUM(riders) as riders, source, dest
    from hourlystationqueue
    where
            extract(ISODOW from depart_date) in (1,2,3,4,5)
      AND
            source = 'PITT'
      AND depart_hour = 7
      and extract(YEAR from depart_date) = 2015
    group by source, dest
                
    """

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    return plotdata


def GetYearlyRiderDistFromPITT2015_AVG():
    global smoothData, scal
    query = """
                                
    select AVG(riders) as riders, source, dest
    from hourlystationqueue
    where
            extract(ISODOW from depart_date) in (1,2,3,4,5)
      AND
            source = 'PITT'
      AND depart_hour = 7
      and extract(YEAR from depart_date) = 2015
    group by source, dest
                
    """

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    return plotdata

def GetAverageDailyFromPITT14():
    global smoothData, scal
    query = """
                                
    select AVG(riders) as riders, source, dest
    from hourlystationqueue
    where
            extract(ISODOW from depart_date) in (1,2,3,4,5)
      AND
            source = 'PITT'
      AND depart_hour = 7
      and extract(YEAR from depart_date) = 2014
    group by source, dest
                
    """

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    return plotdata

def GetAverageDailyFromPITT15():
    global smoothData, scal
    query = """
                                
    select AVG(riders) as riders, source, dest
    from hourlystationqueue
    where
            extract(ISODOW from depart_date) in (1,2,3,4,5)
      AND
            source = 'PITT'
      AND depart_hour = 7
      and extract(YEAR from depart_date) = 2015
    group by source, dest
                
    """

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    return plotdata