import decimal
import numpy as np
import statistics
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
from statsmodels.graphics import tsaplots
from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd

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


def GetTotRiders(rts):
    tot = 0
    for n in rts:
        tot = tot + n[0]
    return tot


def CalcProp(dataArray):
    tot: decimal.Decimal = 0.0
    for d in dataArray:
        tot = tot+float(d)
    propList = list(map(lambda x: float( (float(x)/tot) )*100.0, dataArray))
    return propList

def ChiSqTestNxN(d1):
    rejectHO = False
    data = d1
    stat, p, dof, expected = chi2_contingency(data)

    print("\n")
    print("Chi-square contingency results")
    print("Stats:", stat)
    print("p-val:", p)
    print("Degrees of freedome:",dof)
    print("\n")


    # interpret p-value
    alpha = 0.05
    if p <= alpha:
        rejectHO = True
    return rejectHO, p


def IntersectStations(statA, statB):
    subSetA = [ele1 for ele1 in statA
           for ele2 in statB if (ele1[1] == ele2[1] and ele1[2] == ele2[2]) ]
    return subSetA


def IntersectAllStations(stats):
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
    try:
        l1p = []
        for l in l1:
            if l[0] > counts:
                l1p.append(l)
    except(Exception) as e:
        print(e)
    return l1p

def CalcTotlRidersRun(l1):
    tot = 0
    for n in l1:
        for r in n:
            tot = tot + r[0]
    return tot

def CalcDroppedRiders(beforeList, afterList):
    b = CalcTotlRidersRun(beforeList)
    a = CalcTotlRidersRun(afterList)
    perc = a/b
    return perc

def MakeProportionalAllStations(allStations):
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