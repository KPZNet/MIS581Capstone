import requests
import numpy as np
import statistics
import csv
import os
from datetime import timedelta, date
import calendar
import psycopg2
from scipy.stats import chi2_contingency

import matplotlib.pyplot as plt
from statsmodels.graphics import tsaplots

from Code.DataBase import bart
from statsmodels.tsa.seasonal import seasonal_decompose

def Decomposition(data, per):

    decomposition = seasonal_decompose(data, model="additive", period=per)
    fig = decomposition.plot()
    plt.show()

def ACF(data, lags):
    # Display the autocorrelation plot of your time series
    fig = tsaplots.plot_acf(data, lags=lags)
    plt.show()
    # Display the partial autocorrelation plot of your time series
    fig = tsaplots.plot_pacf(data, lags=lags)
    plt.show()

def SumSquares(ft):
    try:
        r =  np.sqrt(  np.square(ft.real) + np.square(ft.imag)  )
    except(Exception) as e:
        print("Exception: ", e)

    return r

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


def CalcProp(dataArray):
    tot = 0
    for d in dataArray:
        tot = tot+d
    propList = list(map(lambda x: (x/tot)*100.0, dataArray))
    return propList

def ChiSqTest(d1,d2):
    rejectHO = False
    data = [d1, d2]
    stat, p, dof, expected = chi2_contingency(data)

    # interpret p-value
    alpha = 0.05
    if p <= alpha:
        rejectHO = True
    return rejectHO, p

def ChiSqTestExp():
    # defining the table
    data = [[10000, 8000, 10,50,20], [1000, 800, 1,5,2]]
    stat, p, dof, expected = chi2_contingency(data)
    d1 = CalcProp(data[0])
    d2 = CalcProp(data[1])
    data = [d1, d2]
    stat, p, dof, expected = chi2_contingency(data)

    # interpret p-value
    alpha = 0.05
    print("p value is " + str(p))
    if p <= alpha:
        print('Dependent (reject H0)')
    else:
        print('Independent (H0 holds true)')
    return p