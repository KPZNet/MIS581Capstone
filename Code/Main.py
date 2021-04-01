import requests
import numpy as np
import statistics
import csv
import os
from datetime import timedelta, date
import calendar
import psycopg2


try:
	# connect to the database
    conn = psycopg2.connect(host="localhost", port = 5432, database="bartridership", user="postgres", password="minden12k")

    cur = conn.cursor()

    cur.execute("""SELECT * FROM hourlyriders where hour = 8 LIMIT 100""")
    query_results = cur.fetchall()
    for q in query_results:
        print(q)

    # Close the cursor and connection to so the server can allocate
    # bandwidth to other requests
    cur.close()
    conn.close()

except (Exception, psycopg2.Error) as e:
    print("Error in running the query: {}".format(str(e)))

finally:
    cur.close()
    conn.close()
    print("Database connection closed")
