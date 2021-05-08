__author__ = "Kenneth Ceglia"
__copyright__ = "Open Source"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Kenneth Ceglia"
__email__ = "kenceglia@gmail.com"
__status__ = "Course Work"

""" BartLibs.py is a helper library, a collection of functions
    to perform tests, aggregations and other various functions
"""

import decimal
import statistics
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2_contingency
from statsmodels.graphics import tsaplots
from statsmodels.tsa.seasonal import seasonal_decompose
from statistics import NormalDist
import scipy.stats as st

DEBUGON = False

def ConfidenceInterval(data, confidence=0.95):
    """
    Return confidence limits for input data array

    :param data: array of rider data
    :param confidence: percentage of bands
    :return: confidence bands upper and lower
    """
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), st.sem(a)
    h = se * st.t.ppf((1 + confidence) / 2., n-1)
    return m-h, m+h

def ConfidenceIntervalT(data, confidence=0.95):
    c1, c2 = st.t.interval(alpha=confidence, df=len(data)-1, loc=np.mean(data), scale=st.sem(data))
    return c1, c2

def TestMultipleRoutes(riderContTable):
    """
    Tests multiple route variables over time for goodness of fit

    :param riderContTable: route contengency table
    :return: returns chi-square H0 result, and p-value
    """
    rejectHO, pVal = ChiSqTestNxN(riderContTable)
    return rejectHO, pVal

def PrintRoutes(propList):
    """
    Prints out a route with details for all stations in route

    :param propList: list of input stations
    """
    if DEBUGON:
        for n in propList:
            stns = len(n)
            rdr = GetTotRiders(n)
            dtd = n[0][4]
            str = "Date:{0}, Stations:{1}, Riders:{2}".format(dtd, stns, rdr)
            print(str)


def ScrubRiders(propList, minRiders, minStations, minNumber):
    """
    Cleans list of stations

    :param propList: Station list
    :param minRiders: minimum number of riders per station
    :param minStations: min number of intersected stations for route
    :param minNumber: min number of total riders for route
    :return: list of cleaned stations per route
    """
    riderCleaned = []
    for n in propList:
        rdrBRem = GetTotRiders(n)
        numStnsBRem = len(n)
        g = RemoveSmallRiderCountsForStation(minRiders, n)
        rdr = GetTotRiders(g)
        numStns = len(g)
        if numStns >= minStations and rdr > minNumber:
            riderCleaned.append(g)
        else:
            dtd = n[0][4]
            str = "SCRUBBED: Date:{0}, Stations:{1}, Riders:{2} - CStations:{3}, CRiders:{4}".format(dtd, numStns, rdr,
                                                                                                     numStnsBRem,
                                                                                                     rdrBRem)
            if DEBUGON:
                print(str)

    allStatsInter, origList = IntersectAllStations(riderCleaned)
    return allStatsInter, origList

def AllStationsToDF(allStationsComplete):
    """
    Convert list of stations to Pandas dataframe for convenience

    :param allStationsComplete: List of stations for route in list of lists
    :return: Dataframe of route stations
    """
    cols = ['riders', 'source', 'dest', 'depart_hour', 'depart_date']
    ls = []
    for day in allStationsComplete:
        for s in day:
            ls.append(s)
    dfrs = pd.DataFrame(ls, columns=cols)
    dfrs = dfrs.astype({"dest": 'category'})
    dfrs = dfrs.astype({"riders": 'int64'})
    return dfrs


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
