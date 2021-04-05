import requests
import numpy as np
import statistics
import csv
import os
from datetime import timedelta, date
import calendar
import psycopg2
import bart

try:
    query_results = bart.PGBart("""SELECT * FROM hourlystationqueue where hour = 8 LIMIT 100""")
    print(type(query_results))
    for q in query_results:
        print(q)

except (Exception, psycopg2.Error) as e:
    print("Error in running the query: {}".format(str(e)))

finally:
    print("Database connection closed")
