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


def SumSquares(ft):
  r =  np.sqrt(  np.square(ft.real) + np.square(ft.imag)  )
  return r


try:
        query = """
                
select sum(riders), dest, extract(DOW from depart_date) as dow,extract(WEEK from depart_date) as week
from hourlystationqueue
where
        extract(ISODOW from depart_date) in (1,2,3,4,5)
  AND
        dest = 'EMBR'
  and
        depart_hour = 7

  and
        extract(YEAR from depart_date) in (2014,2015, 2016, 2017, 2018)
group by dest,  extract(WEEK from depart_date), extract(DOW from depart_date)
                
        """

        dat = bart.PGBart(query)

        plotdata = list(map(lambda x: x[0], dat ) )
        smoothData = Smooth_1StandardDeviation(plotdata)
        datasize = len(smoothData)
        x = list( range( datasize ) )
        fig, ax1 = plt.subplots(figsize = (20,5))
        p1, =ax1.plot(x, smoothData,
              color='blue',
              linewidth= 1
              )

        sdv = statistics.stdev(plotdata)
        mn = statistics.mean(plotdata)
        Maxthreshold = mn + (2.0 * sdv)
        Minthreshold = mn - (2.0 * sdv)
        plt.hlines(Maxthreshold,0,datasize,colors="red")
        plt.hlines(Minthreshold,0,datasize,colors="red")

        plt.show()

        smoothData = smoothData[:256]
        smoothData = list(map(lambda x: x-statistics.mean(smoothData), smoothData ) )
        print(statistics.mean(smoothData))

        ft = np.fft.fft(smoothData)
        rt = []

        rt = list(map(lambda x: SumSquares(x) , ft ) )
        le = len(rt)
        scal = 1/(2*(np.sqrt(le)))
        rt = list(map(lambda x: scal * x , rt ) )

        plt.plot(rt[:128])
        plt.show()

except(Exception) as e:
        print(e)
finally:
        print("Completed")


