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
from statsmodels.graphics import tsaplots

import bart
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose



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

def Decomposition(data, per):

    decomposition = seasonal_decompose(data, model="additive", period=per)
    fig = decomposition.plot()
    plt.show()

def ACF(data):
    # Display the autocorrelation plot of your time series
    fig = tsaplots.plot_acf(data, lags=24)
    plt.show()
    # Display the partial autocorrelation plot of your time series
    fig = tsaplots.plot_pacf(data, lags=24)
    plt.show()



def SumSquares(ft):
  r =  np.sqrt(  np.square(ft.real) + np.square(ft.imag)  )
  return r


def BARRunFFT():
    global smoothData, scal
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
    plotdata = list(map(lambda x: x[0], dat))
    smoothData = Smooth_1StandardDeviation(plotdata)

    Decomposition(smoothData, 5)
    ACF(smoothData)

    datasize = len(smoothData)
    x = list(range(datasize))
    fig, ax1 = plt.subplots(figsize=(20, 5))
    p1, = ax1.plot(x, smoothData,
                   color='blue',
                   linewidth=1
                   )
    sdv = statistics.stdev(plotdata)
    mn = statistics.mean(plotdata)
    Maxthreshold = mn + (2.0 * sdv)
    Minthreshold = mn - (2.0 * sdv)
    plt.hlines(Maxthreshold, 0, datasize, colors="red")
    plt.hlines(Minthreshold, 0, datasize, colors="red")
    plt.show()
    smoothData = smoothData[:256]
    smoothData = list(map(lambda x: x - statistics.mean(smoothData), smoothData))
    print(statistics.mean(smoothData))
    ft = np.fft.fft(smoothData)
    rt = []
    rt = list(map(lambda x: SumSquares(x), ft))
    le = len(rt)
    scal = 2 / le
    rt = list(map(lambda x: scal * x, rt))
    plt.plot(rt[:128])
    plt.show()

def CosFFT():
    N = 256
    T = 2/N
    x = np.linspace(0.0, N*T, N, endpoint=False)
    y = 10*np.sin(5 * 2.0*np.pi*x) + 0.5*np.sin(10 * 2.0*np.pi*x)
    y = list(map(lambda x: x - statistics.mean(y), y))
    fig, ax1 = plt.subplots(figsize=(20, 5))
    p1, = ax1.plot(x, y,
                   color='blue',
                   linewidth=1
                   )
    plt.show()

    ft = np.fft.fft(y)
    rt = []
    rt = list(map(lambda x: SumSquares(x), ft))
    le = len(rt)
    scal = 2 / le
    rt = list(map(lambda x: scal * x, rt))
    plt.plot(rt[:128])
    plt.show()

def TryDecomp():
    N = 256
    T = 1/N
    x = np.linspace(0.0, N*T, N, endpoint=False)
    y = 10*np.sin(5 * 2.0*np.pi*x) + 0.5*np.sin(10 * 2.0*np.pi*x)
    y = list(map(lambda x: x - statistics.mean(y), y))
    Decomposition(y,51)

try:
    BARRunFFT()
    #CosFFT()

    #TryDecomp()

except(Exception) as e:
        print(e)
finally:
        print("Completed")


