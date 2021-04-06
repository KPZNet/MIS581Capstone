import requests
import numpy as np
import statistics
import csv
import os
from datetime import timedelta, date
import calendar
import psycopg2
import pandas as pd
import scipy
from scipy import signal
import matplotlib.pyplot as plt
import bart


def smoothTriangle(data, degree):
    triangle=np.concatenate((np.arange(degree + 1), np.arange(degree)[::-1])) # up then down
    smoothed=[]

    for i in range(degree, len(data) - degree * 2):
        point=data[i:i + len(triangle)] * triangle
        smoothed.append(np.sum(point)/np.sum(triangle))
    # Handle boundaries
    smoothed=[smoothed[0]]*int(degree + degree/2) + smoothed
    while len(smoothed) < len(data):
        smoothed.append(smoothed[-1])
    return smoothed

def Smooth_1StandardDeviation(dataSet):
    returnData = []
    sdv = statistics.stdev(dataSet)
    mn = statistics.mean(dataSet)
    Maxthreshold = mn + (2.0 * sdv)
    Minthreshold = mn - (2.0 * sdv)
    for d in range(0, len(dataSet)):
        if (dataSet[d] > Maxthreshold ):
            print(d, ' : ' ,dataSet[d], mn+sdv)
            returnData.append(mn + sdv)
        elif (dataSet[d] < Minthreshold ):
            print(d, ' : ' ,dataSet[d], mn-sdv)
            returnData.append(mn - sdv)
        else:
            returnData.append(dataSet[d])
    return returnData





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
        smoothData = Smooth_1StandardDeviation(plotdata)
        #smoothDataTr = smoothTriangle(plotdata, 10)
        #
        #    smoothDataT = signal.savgol_filter(plotdata,
        #                                   53, # window size used for filtering
        #                                   3), # order of fitted polynomial
        #

        datasize = len(smoothData)
        x = list( range( datasize ) )
        fig, ax1 = plt.subplots(figsize = (20,5))
        p1, =ax1.plot(x, plotdata,
              color='blue',
              linewidth= 2
              )
        ax2 = ax1.twinx()
        #add data to the new Y axis
        p4, = ax2.plot(x, smoothData,
                      color='purple',
                      linewidth=2
                      )
        ax1.set_ylim(0,6000)
        ax2.set_ylim(0,6000)

        sdv = statistics.stdev(plotdata)
        mn = statistics.mean(plotdata)
        Maxthreshold = mn + (2.0 * sdv)
        Minthreshold = mn - (2.0 * sdv)
        plt.hlines(Maxthreshold,0,datasize,colors="red")
        plt.hlines(Minthreshold,0,datasize,colors="red")


        plt.show()
except(Exception) as e:
        print(e)
finally:
        print("Completed")


