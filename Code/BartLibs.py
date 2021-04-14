import decimal
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
    tot: decimal.Decimal = 0.0
    for d in dataArray:
        tot = tot+float(d)
    propList = list(map(lambda x: float( (float(x)/tot) )*100.0, dataArray))
    return propList

def ChiSqTest(d1,d2):
    acceptH0 = True
    data = [d1, d2]
    stat, p, dof, expected = chi2_contingency(data)

    # interpret p-value
    alpha = 0.05
    if p <= alpha:
        acceptH0 = False
    return acceptH0, p

def ChiSqTestExp():
    # defining the table
    data = [[50000, 30000, 20000,40000,25000], [50000, 30000, 20000,38000,22000]]
    data = [[10000, 900], [20000, 2100]]
    stat, p, dof, expected = chi2_contingency(data)

    d1 = list(map(lambda x: x/1000, data[0]))
    d2 = list(map(lambda x: x/1000, data[1]))

    data = [d1, d2]
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

def RemoveSmallStationsPercent(per, l1, l2):
    try:
        propL1 = CalcProp(list(map(lambda x: x[0], l1)))
        propL2 = CalcProp(list(map(lambda x: x[0], l2)))
        l1p = []
        l2p = []
        for index, value in enumerate(propL1):
            if propL1[index] > per and propL2[index] > per:
                l1p.append(l1[index])
                l2p.append(l2[index])

    except(Exception) as e:
        print(e)

    return l1p, l2p

def RemoveSmallStations(per, l1, l2):
    try:
        dataL1 = (list(map(lambda x: x[0], l1)))
        dataL2 = (list(map(lambda x: x[0], l2)))
        l1p = []
        l2p = []
        for index, value in enumerate(dataL1):
            if dataL1[index] > per and dataL2[index] > per:
                l1p.append(l1[index])
                l2p.append(l2[index])

    except(Exception) as e:
        print(e)

    return l1p, l2p