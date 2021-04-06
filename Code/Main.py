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

def SmoothData_Filter_A(dataSet):
    sdv = statistics.stdev(dataSet)
    mn = statistics.mean(dataSet)
    Maxthreshold = mn + (2.0 * sdv)
    Minthreshold = mn - (2.0 * sdv)
    for d in range(0, len(dataSet)):
        if (dataSet[d] > Maxthreshold ):
            print(d)
            dataSet[d] = mn + sdv
        if (dataSet[d] < Minthreshold ):
            print(d)
            dataSet[d] = mn - sdv




try:
        query = """
                select sum(riders), dest, depart_date
                from hourlystationqueue
                where
                        extract(ISODOW from depart_date) in (1,2,3,4,5)
                  AND
                        dest = 'EMBR'
                  and
                        depart_hour = 7
                  and   depart_date < '11-01-2015'
                  and
                        extract(YEAR from depart_date) in (2015)
                group by dest, depart_date
                
        """

        dat = bart.PGBart(query)

        plotdata = list(map(lambda x: x[0], dat ) )
        SmoothData_Filter_A(plotdata)

        datasize = len(plotdata)
        x = list( range( datasize ) )
        fig, ax1 = plt.subplots(figsize = (20,5))
        p1, =ax1.plot(x, plotdata,
              color='blue',
              linewidth= 2
              )

        plt.show()
except(Exception) as e:
        print(e)
finally:
        print("Completed")


