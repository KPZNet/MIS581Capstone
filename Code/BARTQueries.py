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
    global smoothData, scal
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


def GetAverageDailyDestFrom(source, hour, year):
    global smoothData, scal
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