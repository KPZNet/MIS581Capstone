import psycopg2
import pandas as pd

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



def GetYearlyAverageDailyRidersToDest(dest, hour, year):
    query = """
                                
        select cast(AVG(riders) as int) as riders, source, dest, hour
        from hourlystationqueue
        where
            extract(ISODOW from date) in (1,2,3,4,5)
        AND
            dest = '{0}'
        AND 
            hour = {1}
        and 
            extract(YEAR from date) = {2}
        group by source, dest, hour
        order by source asc
                
    """.format(dest, hour, year)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    return plotdata


def GetYearlyAverageDailyRidersFromSource(source, hour, year):
    query = """
                                
        select cast(AVG(riders) as int) as riders, source, dest, depart_hour
        from hourlystationqueue
        where
            extract(ISODOW from depart_date) in (1,2,3,4,5)
        AND
            source = '{0}'
        AND 
            depart_hour = {1}
        and 
            extract(YEAR from depart_date) = {2}
        group by source, dest, depart_hour
        order by dest asc
                
    """.format(source, hour, year)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    return plotdata


def GetDailyRidersTo( dest, hour, date):
    query = """
                                
    select riders, source, dest, hour, date
    from hourlystationqueue
    where
        extract(ISODOW from depart_date) in (1)
     and
        hour = {0}
      AND
        dest = '{1}'
      and
        date = '{2}'
      order by source asc 
    """.format(hour, dest, date)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    df = pd.DataFrame(dat, columns = ['riders','source','dest','depart_hour','depart_date'])
    return plotdata, df

def GetDailyRidersFrom( origin, hour, date):
    query = """
                                
    select riders, source, dest, depart_hour, depart_date
    from hourlystationqueue
    where
        extract(ISODOW from depart_date) in (1)
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
    df = pd.DataFrame(dat, columns = ['riders','source','dest','depart_hour','depart_date'])
    return plotdata, df


def GetSumYearRidersPerHour(origin, year):
    query = """
                                
    select cast(sum(riders) as int) as riders, depart_hour
    from hourlystationqueue
    where
          extract(ISODOW from depart_date) in (1,2,3,4,5)
      AND
          source = '{0}'
      and
          extract(YEAR from depart_date) = {1}
    
    group by source, depart_hour
    order by depart_hour asc
                
    """.format(origin,year)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    return plotdata


def GetAveragedWeekdayRidersToDest(dest, hour, years) :
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
            extract(MONTH from depart_date) in (4,5,6,7,8,9,10,11)
        and
            extract(YEAR from depart_date) in {2}
        group by dest,  extract(WEEK from depart_date), extract(DOW from depart_date)

    """.format ( dest, hour, years )
    dat = PGBartLocal ( query )
    plotdata = list ( map ( lambda x : x[0], dat ) )
    return plotdata

def GetAveragedWeekdayRidersFromSource(source, hour, years) :
    query = """

        select sum(cast(riders as double precision)), source, 
            extract(DOW from depart_date) as dow,
            extract(WEEK from depart_date) as week
        from hourlystationqueue
        where
            extract(ISODOW from depart_date) in (1,2,3,4,5)
        AND
            source = '{0}'
        and
            depart_hour = {1}
        and 
            extract(MONTH from depart_date) in (1,2,3,4,5,6,7,8,9,10,11,12)
        and
            extract(YEAR from depart_date) = {2}
        group by source,  extract(WEEK from depart_date), extract(DOW from depart_date)

    """.format ( source, hour, years )
    dat = PGBartLocal ( query )
    plotdata = list ( map ( lambda x : x[0], dat ) )
    return plotdata


def GetWeekdayRidersFrom(origin, hour, years) :
    query = """

        select sum(cast(riders as double precision))
        from hourlystationqueue
        where
            extract(ISODOW from depart_date) in (1)
        AND
            source = '{0}'
        and
            depart_hour = {1}
        and 
            extract(MONTH from depart_date) in (2,3,4,5,6,7,8,9,10,11)
        and
            extract(YEAR from depart_date) in {2}
        group by source, 
        
    """.format ( origin, hour, years )
    dat = PGBartLocal ( query )
    plotdata = list ( map ( lambda x : x[0], dat ) )
    return plotdata


def GetAverageWeeklyRiderForHour2(dest, hour, year):
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


def GetTotalRidersInNetworkByHourFrom(hour, year):
    query = """

     select cast(sum(riders) as int) as riders,source,
             cast(gtfslat as decimal ), cast(gtfslong as decimal)
        from hourlystationqueue, bartstations
        where depart_hour = {0}
          and
              extract(YEAR from depart_date) = {1}
        and
              hourlystationqueue.source = bartstations.abbr
        group by source,  
                 gtfslat, gtfslong
        order by riders asc

    """.format(hour, year)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    df = pd.DataFrame(dat, columns = ['riders','source','lat','long'])
    return plotdata, df

def GetTotalRidersInNetworkByHourTo(hour, year):
    query = """

     select cast(sum(riders) as int) as riders,dest,
             cast(gtfslat as decimal ), cast(gtfslong as decimal)
        from hourlystationqueue, bartstations
        where hour = {0}
          and
              extract(YEAR from date) = {1}
        and
              hourlystationqueue.source = bartstations.abbr
        group by dest,  
                 gtfslat, gtfslong
        order by riders desc

    """.format(hour, year)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    df = pd.DataFrame(dat, columns = ['riders','source','lat','long'])
    return plotdata, df


def GetTotalRidersInNetwork(year):
    query = """

    select cast(sum(riders) as int) as riders,source,
           cast(gtfslat as decimal ), cast(gtfslong as decimal)
    from hourlystationqueue, bartstations
        where
        extract(ISODOW from depart_date) in (1,2,3,4,5)
              and
                  extract(YEAR from depart_date) = {0}
            and
                  hourlystationqueue.source = bartstations.abbr
    group by source, gtfslat, gtfslong
    order by riders desc

    """.format(year)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    df = pd.DataFrame(dat, columns = ['riders','source','lat','long'])
    return plotdata, df


def GetTotalRidersPerHour(year):
    query = """
                                
    select sum(riders) as riders, depart_hour
    from hourlystationqueue
    where
      extract(ISODOW from depart_date) in (1,2,3,4,5)
    and
      extract(YEAR from depart_date) = {0}
    
    group by depart_hour
    order by riders desc
                
    """.format(year)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    df = pd.DataFrame(dat, columns = ['riders','hour'])
    return plotdata, df

def GetTotalRidersPerHourForStation(source, year):
    query = """
                                
    select sum(riders) as riders, depart_hour
    from hourlystationqueue
    where
      extract(ISODOW from depart_date) in (1,2,3,4,5)
    and
      source = '{0}'
    and
      extract(YEAR from depart_date) = {1}
    
    group by depart_hour
    order by riders desc
                
    """.format(source, year)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    df = pd.DataFrame(dat, columns = ['riders','hour'])
    return plotdata, df

def GetTotalRidersPerHourPerDayForStation(source, year):
    query = """
                                
    select SUM(riders) as riders, depart_hour, extract(DOY from depart_date) as DOY
    from hourlystationqueue
    where
            extract(ISODOW from depart_date) in (1,2,3,4,5)
      and
            source = '{0}'
      and
            extract(YEAR from depart_date) = {1}
        group by depart_hour, extract(DOY from depart_date)
    order by DOY, depart_hour
                
    """.format(source, year)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    df = pd.DataFrame(dat, columns = ['riders','depart_hour', 'doy'])
    return plotdata, df

def GetTotalRidersPerHourPerDOWForStation(source, year):
    query = """
                                
    select sum(riders) as riders, depart_hour, extract(ISODOW from depart_date) as isodow, depart_date
    from hourlystationqueue
    where
            extract(ISODOW from depart_date) in (1,2,3,4,5)
    and
            depart_hour in (4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20)
      and
            source = '{0}'
      and
            extract(YEAR from depart_date) = {1}
        group by depart_hour, extract(ISODOW from depart_date), depart_date
    order by depart_date, isodow, depart_hour
                
    """.format(source, year)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    df = pd.DataFrame(dat, columns = ['riders','hour', 'isodow', 'depart_date'])
    return plotdata, df

def GetTotalRidersPerHourPerDOWForStationTEXT(source, year):
    query = """
                                
    select sum(riders) as riders, cast(depart_hour as TEXT),
           cast(extract(ISODOW from depart_date) as TEXT) as isodow,
           depart_date
    from hourlystationqueue
    where
            extract(ISODOW from depart_date) in (1,2,3,4,5)
      and
            depart_hour in (5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20)
      and
            source = '{0}'
      and
            extract(YEAR from depart_date) = {1}
    group by depart_hour, extract(ISODOW from depart_date), depart_date
    order by depart_date, isodow, depart_hour
                
    """.format(source, year)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    df = pd.DataFrame(dat, columns = ['riders','hour', 'isodow', 'date'])
    return plotdata, df

def GetTotalRidersPerDOWForStation(source, year):
    query = """
                                
    select sum(riders) as riders, extract(ISODOW from depart_date) as isodow, depart_date
    from hourlystationqueue
    where
            extract(ISODOW from depart_date) in (1,2,3,4,5)
      and
            source = '{0}'
      and
            extract(YEAR from depart_date) = {1}
        group by  extract(ISODOW from depart_date), depart_date
    order by depart_date, isodow
                
    """.format(source, year)

    dat = PGBartLocal(query)
    plotdata = list(map(lambda x: x, dat))
    df = pd.DataFrame(dat, columns = ['riders','isodow', 'depart_date'])
    return plotdata, df


def GetTotalRidersPerMonth() :
    query = """
    select sum(cast(riders as double precision)),
           extract(MONTH from date) as month,
           extract(YEAR from date) as year,
           row_number() over()
    from hourlystationqueue
    group by month,  year
    order by year asc , month asc

    """.format ()
    dat = PGBartLocal ( query )
    plotdata = list ( map ( lambda x : x, dat ) )
    df = pd.DataFrame(dat, columns = ['riders','month', 'year','rMonth'])
    return plotdata,df