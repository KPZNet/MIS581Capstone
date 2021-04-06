import requests
import numpy as np
import statistics
import csv
import os
from datetime import timedelta, date
import calendar
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import bart


try:
        query = """
                select sum(riders), source, depart_date
                from hourlystationqueue
                where
                        extract(ISODOW from depart_date) in (1)
                  AND
                        source = 'PITT'
                  and
                        depart_hour = 7
                  and
                        extract(YEAR from depart_date) in (2015)
                group by source, depart_date
                
        """

        dat = bart.PGBart(query)

        plotdata = list(map(lambda x: x[0], dat ) )
        datasize = len(plotdata)
        x = list( range( datasize ) )
        fig, ax1 = plt.subplots(figsize = (20,5))
        p1, =ax1.plot(x, plotdata,
              color='blue',
              linewidth=1
              )

        plt.show()
except(Exception) as e:
        print(e)
finally:
        print("Completed")


