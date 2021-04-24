from random import random

import numpy as np
import pandas
import statistics
from cycler import cycler
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import matplotlib.ticker as mticker
import BartLibs
import BARTQueries
from datetime import date, timedelta
import plotly.express as px
import pandas as pd
from matplotlib.cm import get_cmap
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.tsa.stattools import adfuller

from mpl_toolkits.mplot3d import axes3d





def RunBARTTimeSeries():
    plotdata = BARTQueries.GetAveragedWeekdayRidersToDest('EMBR', 7, '(2013,2014,2015,2016,2017,2018,2019)')
    pd = plotdata

    # ADF statistic to check stationarity
    timeseries = adfuller ( pd )
    if timeseries[0] > timeseries[4]["5%"] :
        print ( "Failed to Reject Ho - Time Series is Non-Stationary" )
    else :
        print ( "Reject Ho - Time Series is Stationary" )

    model = sm.tsa.UnobservedComponents ( pd,
                                    level='fixed intercept',
                                    seasonal=5)
    res_f = model.fit ( disp=False )
    print ( res_f.summary () )
    # The first state variable holds our estimate of the intercept
    print ( "fixed intercept estimated as {0:.3f}".format ( res_f.smoother_results.smoothed_state[0, -1 :][0] ) )

    res_f.plot_components ()
    plt.show ()


def RunBARTTimeSeries2(source, hour, year):
    plotdata = BARTQueries.GetAveragedWeekdayRidersFromSource(source, hour, year)
    title = "Daily Riders for {0} at {1}:00AM in {2}".format(source, hour, year)
    PlotTimeSeriesWithLimitBars(plotdata, title)

    smoothData = BartLibs.Smooth_1StandardDeviation(plotdata)
    PlotTimeSeriesWithLimitBars(smoothData, title)

    PlotTimeSeriesFFT(smoothData, title)

    BartLibs.Decomposition(smoothData, 5)
    BartLibs.ACF(smoothData, 10)


    # ADF statistic to check stationarity
    timeseries = adfuller ( smoothData ,autolag='AIC')
    pVal = timeseries[1]
    print("\n\n\nAugmented Dickey-Fuller Test: pval = {0}\n\n\n".format(pVal))
    #if timeseries[0] > timeseries[4]["5%"] :
    if pVal > 0.05:
        print ( "Failed to Reject Ho - Time Series is Non-Stationary" )
    else :
        print ( "Reject Ho - Time Series is Stationary" )

    model = sm.tsa.UnobservedComponents ( smoothData,
                                    level='fixed intercept',
                                          freq_seasonal=[{'period' : 50,
                                                          'harmonics' : 5}] )
    res_f = model.fit ( disp=False )
    print ( res_f.summary () )
    # The first state variable holds our estimate of the intercept
    print ( "fixed intercept estimated as {0:.3f}".format ( res_f.smoother_results.smoothed_state[0, -1 :][0] ) )

    res_f.plot_components ()
    plt.show ()


def PlotTimeSeriesFFT(smoothData, title):
    smoothMean = statistics.mean(smoothData)
    smoothDataZeroed = list(map(lambda x: x - smoothMean, smoothData))
    ft = np.fft.fft(smoothDataZeroed)
    realAmplitudes = list(map(lambda x: BartLibs.SumSquares(x), ft))
    realAmpsLen = len(realAmplitudes)
    fftScale = 2.0 / (realAmpsLen)
    realAmplitudesScaled = list(map(lambda x: fftScale * x, realAmplitudes))
    plt.plot(realAmplitudesScaled[:int(realAmpsLen / 3.0)])
    plt.suptitle(title)
    plt.show()


def PlotTimeSeriesWithLimitBars(plotdata, title):
    rawLen = len(plotdata)
    x = list(range(rawLen))
    plt.plot(x, plotdata,
             color='blue',
             linewidth=1
             )
    sdv = statistics.stdev(plotdata)
    mn = statistics.mean(plotdata)
    Maxthreshold = mn + (2.0 * sdv)
    Minthreshold = mn - (2.0 * sdv)
    plt.hlines(Maxthreshold, 0, rawLen, colors="red")
    plt.hlines(Minthreshold, 0, rawLen, colors="red")
    plt.suptitle(title)
    plt.show()


def CosFFT():
    N = 512
    T = 1 / N
    F = int(20)
    P = int(np.round(N / F))
    print("Frequency: ", F)
    print("Period: ", P)
    x = np.linspace(0.0, N, N, endpoint=False)
    y = 10 * np.sin(F * 2.0 * np.pi * (x / N))  # + 5*np.sin(10 * 2.0*np.pi*x)
    y = list(map(lambda x: x - statistics.mean(y), y))
    plt.plot(x, y,
             color='blue',
             linewidth=1
             )
    plt.show()

    ft = np.fft.fft(y)
    rt = []
    rt = list(map(lambda x: BartLibs.SumSquares(x), ft))
    le = len(rt)
    scal = 2 / le
    rt = list(map(lambda x: scal * x, rt))
    plt.plot(rt[:int(N / 2)])
    plt.show()

    BartLibs.Decomposition(y, P)
    BartLibs.ACF(y, P * 2)


def PrintRoutes(propList):
    for n in propList:
        stns = len ( n )
        rdr = BartLibs.GetTotRiders ( n )
        dtd = n[0][4]
        str = "Date:{0}, Stations:{1}, Riders:{2}".format(dtd, stns, rdr)
        print(str)


def PlotRoutes(plotdata):

    for d in plotdata:
        data = list ( map ( lambda x : x[0], d ) )
        x = list( range( len(d)))
        plt.plot(x, data,
                 linewidth=1
                 )

    plt.suptitle("test")
    plt.show()



def ScrubRiders(propList, minRiders, minStations, minNumber):
    riderCleaned = []
    for n in propList:
        rdrBRem = BartLibs.GetTotRiders ( n )
        numStnsBRem = len (n)
        g = BartLibs.RemoveSmallRiderCountsForStation(minRiders, n)
        rdr = BartLibs.GetTotRiders (g)
        numStns = len(g)
        if numStns >= minStations and rdr > minNumber:
            riderCleaned.append(g)
        else:
            dtd = n[0][4]
            str = "SCRUBBED: Date:{0}, Stations:{1}, Riders:{2} - CStations:{3}, CRiders:{4}".format ( dtd, numStns, rdr, numStnsBRem, rdrBRem )
            print(str)

    allStatsInter, origList = BartLibs.IntersectAllStations(riderCleaned)
    return allStatsInter, origList


def TestMultipleRoutes(riderContTable):
    rejectHO, pVal = BartLibs.ChiSqTestNxN(riderContTable)
    return rejectHO, pVal


def CompareMultipleDayRidersToX(startDate, endDate, dest, hour, minStations, minRiders):
    propList = []
    start_date = startDate
    end_date = endDate
    delta = timedelta(days=1)
    while start_date <= end_date:
        if start_date.weekday() < 5:
            sDate = start_date.strftime("%m-%d-%Y")
            da = BARTQueries.GetDailyRidersTo(dest, hour, sDate)
            if len(da) > minStations:
                propList.append(da)
        start_date += delta

    if (len(propList) > 1):
        allStations, allStationsComplete = ScrubRiders(minRiders, propList)
        rejectHO, pVal = TestMultipleRoutes(allStations)
        print("MultiRiders From {0}, Reject: {3}, Num: {1}, PVal: {2}".format(dest, len(allStations), pVal, rejectHO))
    else:
        print("No Stations Found")

def CompareMultipleDayRidersTo(startDate, endDate, dest, hour, minStations, minRiders, minNumber, dayInterval):
    propList = []
    start_date = startDate
    end_date = endDate
    delta = timedelta(days=dayInterval)
    while start_date <= end_date:
        if start_date.weekday() < 5:
            sDate = start_date.strftime("%m-%d-%Y")
            da = BARTQueries.GetDailyRidersTo(dest, hour, sDate)
            if len(da) > 0:
                propList.append(da)
        start_date += delta

    if (len(propList) > 1):
        PrintRoutes(propList)
        allStations, allStationsComplete = ScrubRiders(propList, minRiders, minStations, minNumber)

        stations = len(allStationsComplete[0])
        rejectHO, pVal = TestMultipleRoutes(allStations)
        title = "MultiRiders From {0}, RejectHO: {3}\n PVal: {2:.5f}, Days: {1}, Stations:{4} ".format(dest,
                                                                                                       len(allStations),
                                                                                                       pVal, rejectHO,
                                                                                                       stations)
        print(title)
        PlotMultiSets(allStationsComplete, title)
        PrintRoutes ( allStationsComplete )
    else:
        print("No Stations Found")

def CompareMultipleDayRidersFrom(startDate, endDate, origin, hour, minStations, minRiders, minNumber, dayInterval):
    propList = []
    start_date = startDate
    end_date = endDate
    delta = timedelta(days=dayInterval)
    while start_date <= end_date:
        if start_date.weekday() < 5:
            sDate = start_date.strftime("%m-%d-%Y")
            da, df = BARTQueries.GetDailyRidersFrom(origin, hour, sDate)
            if len(da) > 0:
                propList.append(da)
        start_date += delta

    if (len(propList) > 1):
        PrintRoutes(propList)
        allStations, allStationsComplete = ScrubRiders(propList, minRiders, minStations, minNumber)

        stations = len(allStationsComplete[0])
        rejectHO, pVal = TestMultipleRoutes(allStations)
        title = "MultiRiders From {0}, RejectHO: {3}\n PVal: {2:.5f}, Days: {1}, Stations:{4} ".format(origin,
                                                                                                       len(allStations),
                                                                                                       pVal, rejectHO,
                                                                                                       stations)
        print(title)
        PlotMultiSets(allStationsComplete, title)
        dropRidersPerc = BartLibs.CalcDroppedRiders(propList, allStationsComplete)
        PrintRoutes ( allStationsComplete )

        PlotRoutes(allStationsComplete)
    else:
        print("No Stations Found")


def CompareMultiDayRidersToYearlyAveDest(startDate, endDate, dest1, hour1, year1, minStations, minRiders):
    yearlyAvg = BARTQueries.GetYearlyAverageDailyRidersToDest(dest1, hour1, year1)

    start_date = startDate
    end_date = endDate
    delta = timedelta(days=1)
    while start_date <= end_date:
        if start_date.weekday() < 5:
            sDate = start_date.strftime("%m-%d-%Y")
            da = BARTQueries.GetDailyRidersTo(dest1, hour1, sDate)
            if len(da) > minStations:
                dayYearPair = [da, yearlyAvg]
                allStations, allStationsComplete = ScrubRiders(minRiders, dayYearPair)
                rejectHO, pVal = TestMultipleRoutes(allStations)
                print("MultiRiders To {0}, Stats: {1}, RejectHO: {4}, PVal: {2:.5f}  Date: {3}".format(dest1, len(da),
                                                                                                       pVal, sDate,
                                                                                                       rejectHO))
                # CompareRouteProportions(da, yearlyAvg)
        start_date += delta


def CompareMultiDayRidersToYearlyAveFrom(startDate, endDate, source1, hour1, year1, minStations, minRiders):
    yearlyAvg = BARTQueries.GetYearlyAverageDailyRidersFromSource(source1, hour1, year1)

    start_date = startDate
    end_date = endDate
    delta = timedelta(days=1)
    while start_date <= end_date:
        if start_date.weekday() < 5:
            sDate = start_date.strftime("%m-%d-%Y")
            da = BARTQueries.GetDailyRidersFrom(source1, hour1, sDate)
            if len(da) > minStations:
                dayYearPair = [da, yearlyAvg]
                allStations, allStationsComplete = ScrubRiders(minRiders, dayYearPair)
                rejectHO, pVal = TestMultipleRoutes(allStations)
                title = "MultiRiders From {0}, Stats: {1}\nRejectHO: {4}, PVal: {2:.5f}\nDate {3}".format(source1,
                                                                                                          len(da), pVal,
                                                                                                          sDate,
                                                                                                          rejectHO)
                print(title)
                PlotMultiSets(allStationsComplete, title)
                PlotTwoSets(allStationsComplete, sDate, year1, title)
                PlotTwoSetsTrueProp(allStationsComplete, sDate, year1, title)
                # CompareRouteProportions(da, yearlyAvg)
        start_date += delta

def PlotStationUsage(stats, title):
    cats = list(map(lambda x: x[2], stats))
    d1 = list(map(lambda x: x[0], stats))

    X = np.arange(len(d1))
    plt.bar(X + 0.00, d1, color='b', width=0.25)
    plt.xticks(X, cats)
    plt.tick_params(labelrotation=45)

    plt.title(title)
    plt.show()

def PlotRouteSet(stats, title):
    cats = list(map(lambda x: x[2], stats))
    d1 = list(map(lambda x: x[0], stats))

    X = np.arange(len(d1))
    plt.bar(X + 0.00, d1, color='b', width=0.25)
    plt.xticks(X, cats)
    plt.tick_params(labelrotation=45)

    plt.title(title)
    plt.show()

def PlotTwoSets(stats, lab1, lab2, title):
    cats = list(map(lambda x: x[2], stats[0]))
    d1 = list(map(lambda x: x[0], stats[0]))
    d2 = list(map(lambda x: x[0], stats[1]))
    X = np.arange(len(d1))
    plt.bar(X + 0.00, d1, color='b', width=0.25)
    plt.bar(X + 0.3, d2, color='r', width=0.25)
    plt.xticks(X, cats)
    plt.legend(labels=[lab1, lab2])
    plt.tick_params(labelrotation=45)

    plt.title(title)
    plt.show()


def PlotTwoSetsTrueProp(stats, lab1, lab2, title):
    cats = list(map(lambda x: x[2], stats[0]))
    d1 = list(map(lambda x: x[0], stats[0]))
    d2 = list(map(lambda x: x[0], stats[1]))

    d1Scale = 100.0 / max(d1)
    d2Scale = 100.0 / max(d2)

    d1 = list(map(lambda x: x * d1Scale, d1))
    d2 = list(map(lambda x: x * d2Scale, d2))

    X = np.arange(len(d1))
    plt.bar(X + 0.00, d1, color='b', width=0.25)
    plt.bar(X + 0.3, d2, color='r', width=0.25)
    plt.xticks(X, cats)
    plt.legend(labels=[lab1, lab2])
    plt.tick_params(labelrotation=45)

    plt.title(title)
    plt.show()


def PlotMultiSets(stats, title):
    cats = list(map(lambda x: x[2], stats[0]))
    N = len(cats)
    ns = len(stats)
    X = np.arange(N)
    barWidth = .25
    spread = (ns/2)

    plt.rcParams["axes.prop_cycle"] = plt.cycler ( "color", plt.cm.tab20b.colors )
##
##    colors = [hsv_to_rgb([(i * 0.618033988749895) % 1.0, 1, 1])
##              for i in range(100)]
##    plt.rc('axes', prop_cycle=(cycler('color', colors)))
##


    for index, p in enumerate(stats):
        d = list(map(lambda x: x[0], p))
        d = list(map(lambda x: x * 100.0 / max(d), d))
        plt.bar(X + (barWidth * index) / spread, d, width=barWidth / 2)

    plt.xticks(X + barWidth / 2, cats)
    plt.tick_params(labelrotation=45)

    plt.title(title)
    plt.show()


def PlotYearlySumRidersPerOrigin(origin, year):
    hourlyRiders = BARTQueries.GetSumYearRidersPerHour(origin, year)
    cat_names = list(map(lambda x: x[1], hourlyRiders))
    barValues = list(map(lambda x: x[0], hourlyRiders))
    plt.bar(cat_names, barValues)
    plt.suptitle('Total Riders : {0}'.format(year))
    plt.xlabel('Hour')
    plt.ylabel('Riders')
    plt.xticks(rotation=90)
    plt.show()


def ShowAverageWeeklyRiderForHour(dest, hour, year):
    plotdata = BARTQueries.GetAverageWeeklyRiderForHour(dest, hour, year)
    viewData = list(map(lambda x: x[0], plotdata))
    PlotTimeSeriesWithLimitBars(viewData)

    smoothData = BartLibs.Smooth_1StandardDeviation(viewData)
    PlotTimeSeriesWithLimitBars(smoothData)

    # PlotTimeSeriesFFT(smoothData)
    # BartLibs.Decomposition(smoothData, 4)
    # BartLibs.ACF(smoothData, 10)

def PlotTotalRidersByHour(year):
    hourlyRiders, df = BARTQueries.GetTotalRidersPerHour(year)

    plt.bar(df['hour'], df['riders'])
    plt.suptitle('Total Riders : {0}'.format(year))
    plt.xlabel('Departure Hour')
    plt.ylabel('Riders')
    plt.xticks(rotation=0)
    plt.show()

def PlotTotalRidersByHourBySource(source, year):
    hourlyRiders, df = BARTQueries.GetTotalRidersPerHourForStation(source, year)

    plt.bar(df['hour'], df['riders'])
    plt.suptitle('Total Riders : {0}'.format(year))
    plt.xlabel('Departure Hour')
    plt.ylabel('Riders')
    plt.xticks(rotation=0)
    plt.show()

def GetTotalRidersPerHourPerDayForStation(source, year):
    hourlyRiders, df = BARTQueries.GetTotalRidersPerHourForStation(source, year)

    plt.bar(df['hour'], df['riders'])
    plt.suptitle('Total Riders : {0}'.format(year))
    plt.xlabel('Departure Hour')
    plt.ylabel('Riders')
    plt.xticks(rotation=0)
    plt.show()

def CompareRidersPerHourPerDayForStation(source, year):
    hourlyRiders, df = BARTQueries.GetTotalRidersPerHourPerDOWForStation(source, year)
    labels =[]
    data = []

    for i in range(4, 21):
        dv = df[df['hour'] == i].riders.tolist()
        labels.append(str(i))
        data.append(dv)

    # Creating plot
    bp = plt.boxplot(data, labels=labels)
    plt.title("Riders by Hour, Station: {0}, Year:{1}".format(source,year))
    plt.xlabel('Departure Hour')
    plt.ylabel('Riders')
    # show plot
    plt.show()

def CompareRidersPerISODOWForStation2(source, year):
    hourlyRiders, df = BARTQueries.GetTotalRidersPerDOWForStation(source, year)
    labels =[]
    data = []

    for i in range(1, 6):
        dv = df[df['isodow'] == i].riders.tolist()
        labels.append(str(i))
        data.append(dv)

    labels = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri']
    # Creating plot
    bp = plt.boxplot(data, labels=labels)
    plt.title("Riders by DOW, Station: {0}, Year:{1}".format(source,year))
    plt.xlabel('DOW')
    plt.ylabel('Riders')
    # show plot
    plt.show()


def TwoWayAnova(source, year):
    hourlyRiders, df = BARTQueries.GetTotalRidersPerHourPerDOWForStationTEXT(source, year)
    #perform two-way ANOVA
    model = ols('riders ~ C(hour) + C(isodow) + C(hour):C(isodow)', data=df).fit()
    g = sm.stats.anova_lm(model, typ=2)
    print(g)

def PlotRidersOnMap(year):

    px.set_mapbox_access_token(open(".mapbox_token").read())

    dat, df = BARTQueries.GetTotalRidersInNetworkByHourFrom(7,year)

    fig = px.scatter_mapbox(df, lat='lat', lon='long', size='riders',
                            color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)

    fig.show()

