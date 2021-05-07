#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" BartLibs.py is a helper library, a collection of functions
    to perform tests, aggregations and other various functions
"""

import decimal
import statistics

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2_contingency
from statsmodels.graphics import tsaplots
from statsmodels.tsa.seasonal import seasonal_decompose

from Code.BARTPlots import DEBUGON


def Decomposition(data, per):
    """Performs seasonal decomposition and plot output

    Args:
        data (list): list of data in order
        per (int): period for decomposition

    Returns:
        none:
    """

    decomposition = seasonal_decompose(data, model="additive", period=per)
    fig = decomposition.plot()
    plt.show()


def ACF(data, lags):
    """Performs auto correlation on time series and plots output

    Args:
        data (list): list of data in order
        lags (int): estimate period for auto correlation

    Returns:
        none
    """
    fig = tsaplots.plot_acf(data, lags=lags)
    plt.show()
    fig = tsaplots.plot_pacf(data, lags=lags)
    plt.show()


def SumSquares(ft):
    """Performs inphase/quad sum of square root

    Args:
        ft (complex): complex number

    Returns:
        r: real number amplitude
    """
    try:
        r = np.sqrt(np.square(ft.real) + np.square(ft.imag))
    except(Exception) as e:
        print("Exception: ", e)

    return r


def Smooth_1StandardDeviation(dataSet):
    """Smooths time series data and clips at 2 standard deviations

    Args:
        dataSet (list): time series data

    Returns:
        smoothed data
    """
    returnData = []
    sdv = statistics.stdev(dataSet)
    mn = statistics.mean(dataSet)
    Maxthreshold = mn + (2.0 * sdv)
    Minthreshold = mn - (2.0 * sdv)
    for d in range(0, len(dataSet)):
        if (dataSet[d] > Maxthreshold):
            if DEBUGON:
                print(d, ' : ', dataSet[d], mn + sdv)
            returnData.append(mn + sdv)
        elif (dataSet[d] < Minthreshold):
            if DEBUGON:
                print(d, ' : ', dataSet[d], mn - sdv)
            returnData.append(mn - sdv)
        else:
            returnData.append(dataSet[d])
    return returnData


def GetTotRiders(rts):
    """Returns total riders in list of stations

    Args:
        rts (list of stations): list of stations

    Returns:
        Total riders for all stations
    """
    tot = 0
    for n in rts:
        tot = tot + n[0]
    return tot

def CalcProp(dataArray):
    """Returns 0-100% full scale data array

    Args:
        dataArray (list): data list

    Returns:
        propList: (list) proportional rider array
    """
    tot: decimal.Decimal = 0.0
    for d in dataArray:
        tot = tot + float(d)
    propList = list(map(lambda x: float((float(x) / tot)) * 100.0, dataArray))
    return propList


def ChiSqTestNxN(d1):
    """ Performs Chi-Square on NxN contigency matrix
        prints out results

    Args:
        d1 (list of list): NxN contingency matrix

    Returns:
        rejectH0 - true or false if rejected H0
        p - p-value of Chi-square test
    """
    rejectHO = False
    data = d1
    stat, p, dof, expected = chi2_contingency(data)

    if DEBUGON:
        print("\n")
        print("Chi-square contingency results")
        print("Stats:", stat)
        print("p-val:", p)
        print("Degrees of freedom:", dof)
        print("\n")

    # interpret p-value
    alpha = 0.05
    if p <= alpha:
        rejectHO = True
    return rejectHO, p


def IntersectStations(statA, statB):
    """Returns intersection of two lists

    Args:
        statA (list): list of stations
        statB (list): list of stations

    Returns:
        List of intersected stations
    """
    subSetA = [ele1 for ele1 in statA
               for ele2 in statB if (ele1[1] == ele2[1] and ele1[2] == ele2[2])]
    return subSetA


def IntersectAllStations(stats):
    """Returns intersection of all stations in input list of stations

    Args:
        stats (list): list of list of stations

    Returns:
        List of intersected stations
    """
    newList = []
    riderList = []
    for i, s in enumerate(stats):
        sub = stats[i]
        for j, k in enumerate(stats):
            if i != j:
                subPrime = IntersectStations(sub, stats[j])
                sub = subPrime
        newList.append(sub)
        riderList.append(list(map(lambda x: x[0], sub)))
    return riderList, newList


def RemoveSmallRiderCountsForStation(counts, l1):
    """Removes all stations with fewer than input rider count

    Args:
        counts (int): min riders
        l1 (list): list of stations

    Returns:
        List of trimmed stations
    """
    try:
        l1p = []
        for l in l1:
            if l[0] > counts:
                l1p.append(l)
    except(Exception) as e:
        print(e)
    return l1p


def CalcTotlRidersRun(l1):
    """Returns intersection of two lists

    Args:
        statA (list): list of stations
        statB (list): list of stations

    Returns:
        List of intersected stations
    """
    tot = 0
    for n in l1:
        for r in n:
            tot = tot + r[0]
    return tot


def CalcDroppedRiders(beforeList, afterList):
    """
    Calculate dropped riders percentage

    :param beforeList: stations before trim
    :param afterList:  stations after trim
    :return: total number of riders dropped as a percentage
    """
    b = CalcTotlRidersRun(beforeList)
    a = CalcTotlRidersRun(afterList)
    perc = a / b
    return perc


def MakeProportionalAllStations(allStations):
    """
    Takes all input stations and proportions them to 0-100% scale

    :param allStations:
    :return: all stations in proportional scaling
    """
    newAllStations = []
    for index, p in enumerate(allStations):
        d = list(map(lambda x: x[0], p))
        d = list(map(lambda x: x * 100.0 / max(d), d))
        dayList = []
        for i, statTuple in enumerate(p):
            statTPL = list(statTuple)
            statTPL[0] = d[i]
            nTuple = tuple(statTPL)
            dayList.append((nTuple))
        newAllStations.append(dayList)
    return newAllStations
