import psycopg2

def PGBart(query):
    try:
        query_results = []
        conn = psycopg2.connect(host="10.0.0.206", port=5432,
                                database="bartridership",
                                user="postgres",
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
        conn = psycopg2.connect(host="localhost", port=5432,
                                database="bartridership",
                                user="postgres",
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


def GetAveragedWeekdayRidersToDest(dest, hour, years):
    query = """
                
        select avg(cast(riders as double precision)), dest, 
            extract(DOW from depart_date) as dow,
            extract(WEEK from depart_date) as week
        from hourlystationqueue
        where
            extract(ISODOW from depart_date) in (1,2,3,4,5)
        AND
            dest = '{0}'
        and
            depart_hour = {1}
        and 
            extract(MONTH from depart_date) in (1,2,3,4,5,6,7,8,9,10,11,12)
        and
            extract(YEAR from depart_date) in {2}
        group by dest,  extract(WEEK from depart_date), extract(DOW from depart_date)
                
    """.format(dest, hour, years)
    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x[0], dat))
    return plotdata


def GetAverageDailyRidersFromSource(source, hour, year):
    query = """
                                
        select AVG(riders) as riders, source, dest
        from hourlystationqueue
        where
            extract(ISODOW from depart_date) in (1,2,3,4,5)
        AND
            source = '{0}'
        AND 
            depart_hour = {1}
        and 
            extract(YEAR from depart_date) = {2}
        group by source, dest
                
    """.format(source, hour, year)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    return plotdata

def GetAverageDailySourceByHour(source):
    query = """
                                
    select AVG(riders) as riders, source, depart_hour
    from hourlystationqueue
    where
            extract(ISODOW from depart_date) in (1,2,3,4,5)
      AND
            source = '{0}'
      and
        extract(YEAR from depart_date) in (2014,2015,2016,2017,2018)
    group by source, depart_hour
                
    """.format(source)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    return plotdata


def GetDailyRidersFrom( origin, hour, date):
    query = """
                                
    select riders, source, dest, depart_hour
    from hourlystationqueue
    where
        extract(ISODOW from depart_date) in (1,2,3,4,5)
     and
        depart_hour = {0}
      AND
        source = '{1}'
      and
        depart_date = '{2}'
      order by dest asc 
    """.format(hour, origin, date)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    return plotdata


def GetDailyRidersTo( dest, hour, date):
    query = """
                                
    select riders, source, dest, depart_hour
    from hourlystationqueue
    where
        extract(ISODOW from depart_date) in (1,2,3,4,5)
     and
        hour = {0}
      AND
        dest = '{1}'
      and
        date = '{2}'
      order by dest asc 
    """.format(hour, dest, date)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    return plotdata

def GetDailyRidersFrom( source, hour, date):
    query = """
                                
    select riders, source, dest, depart_hour
    from hourlystationqueue
    where
        extract(ISODOW from depart_date) in (1,2,3,4,5)
     and
        depart_hour = {0}
      AND
        source = '{1}'
      and
        depart_date = '{2}'
      order by dest asc 
    """.format(hour, source, date)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    return plotdata


def GetDailyRidersAveByMonth(hour, source, isodow, month, year):
    query = """
                                
    select avg(riders) as riders, source, dest, depart_hour,
           extract(ISODOW from depart_date) as ISODOW
    from hourlystationqueue
    where
            depart_hour = {0}
      AND
        source = '{1}'
      and
        extract(ISODOW from depart_date) = {2}
      and
        extract(MONTH from depart_date) = {3}
      and
        extract(YEAR from depart_date) = {4}
    group by source, dest, depart_hour, extract(ISODOW from depart_date)
                
    """.format(hour, source, isodow, month, year)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    return plotdata


def GetAverageDayRider(source, hour, isodow, year):
    query = """
                                
    select AVG(riders) as riders, source, dest, depart_hour
    from hourlystationqueue
    where
        extract(ISODOW from depart_date) = {2}
    AND
        source = '{0}'
    AND
        depart_hour = {1}
    AND
        extract(YEAR from depart_date) = {3}
    group by source, dest, depart_hour
                
    """.format(source, hour, isodow, year)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    return plotdata


def GetAverageDailyRidersFrom(source, hour, year):
    query = """
                                
    select cast(avg(riders) as int) as riders, source, dest, depart_hour
    from hourlystationqueue
    where
    extract(ISODOW from depart_date) in (1,2,3,4,5)
    and
    source = '{0}'
    AND
    depart_hour = {1}
    AND
    extract(YEAR from depart_date) = {2}
    group by source, dest, depart_hour
    order by dest
                
    """.format(source, hour, year)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    return plotdata


def GetTotalDayRiderByWeek(source, hour, week, year):
    query = """
                                
    select avg(riders) as riders, source, dest, depart_hour
    from hourlystationqueue
    where
        extract(ISODOW from depart_date) in (1,2,3,4,5)
    and
        extract(WEEK from depart_date) = {2}
    AND
        source = '{0}'
    AND
        depart_hour = {1}
    AND
        extract(YEAR from depart_date) = {3}
    group by source, dest, depart_hour
    order by dest
                
    """.format(source, hour, week, year)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    return plotdata

def GetAverageDayRiderByMonth(source, hour, isodow, month, year):
    query = """
                                
    select sum(riders) as riders, source, dest, depart_hour
    from hourlystationqueue
    where
        extract(ISODOW from depart_date) in ({2})
    AND
        source = '{0}'
    AND
        depart_hour = {1}
    AND
        extract(MONTH from depart_date) = {3}
    AND
        extract(YEAR from depart_date) = {4}
    group by source, dest, depart_hour
    order by dest
                
    """.format(source, hour, isodow, month, year)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    return plotdata




def GetAverageWeeklyRiderForHour(dest, hour, year):
    query = """
                                
        select avg(cast(riders as double precision)), dest, 
        extract(WEEK from depart_date) as week
        from hourlystationqueue
        where
            extract(ISODOW from depart_date) in (1,2,3,4,5)
        AND
            dest = '{0}'
        and
            depart_hour = {1}
        and 
            extract(MONTH from depart_date) in (1,2,3,4,5,6,7,8,9,10,11,12)
        and
            extract(YEAR from depart_date) in {2}
        group by dest,  extract(WEEK from depart_date)
                
    """.format(dest, hour, year)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    return plotdata