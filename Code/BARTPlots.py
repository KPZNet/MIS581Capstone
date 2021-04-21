from random import random

import numpy as np
import pandas
import statistics
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import BartLibs
import BARTQueries
from datetime import date, timedelta
import random


def RunBARTTimeSeries():
    plotdata = BARTQueries.GetAveragedWeekdayRidersToDest('EMBR', 7, '(2013,2014,2015,2016,2017,2018,2019)')

    PlotTimeSeriesWithLimitBars(plotdata)

    smoothData = BartLibs.Smooth_1StandardDeviation(plotdata)
    PlotTimeSeriesWithLimitBars(smoothData)

    PlotTimeSeriesFFT(smoothData)

    BartLibs.Decomposition(smoothData, 5)
    BartLibs.ACF(smoothData, 10)


def PlotTimeSeriesFFT(smoothData):
    smoothMean = statistics.mean(smoothData)
    smoothDataZeroed = list(map(lambda x: x - smoothMean, smoothData))
    ft = np.fft.fft(smoothDataZeroed)
    realAmplitudes = list(map(lambda x: BartLibs.SumSquares(x), ft))
    realAmpsLen = len(realAmplitudes)
    fftScale = 2.0 / (realAmpsLen)
    realAmplitudesScaled = list(map(lambda x: fftScale * x, realAmplitudes))
    plt.plot(realAmplitudesScaled[:int(realAmpsLen / 3.0)])
    plt.suptitle("Fourrier Transform Rider Frequency")
    plt.show()


def PlotTimeSeriesWithLimitBars(plotdata):
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
    plt.suptitle("BART Daily Rider EMBR 7:00AM")
    plt.show()


def CosFFT():
    N = 512
    T = 1/N
    F = int(20)
    P = int(np.round(N/F))
    print("Frequency: ", F)
    print("Period: ",P)
    x = np.linspace(0.0, N, N, endpoint=False)
    y = 10*np.sin(F * 2.0*np.pi*(x/N)) #+ 5*np.sin(10 * 2.0*np.pi*x)
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
    plt.plot(rt[:int(N/2)])
    plt.show()

    BartLibs.Decomposition(y, P)
    BartLibs.ACF(y, P*2 )



def ScrubRiders(minRiders, propList) :
    riderCleaned = []
    for n in propList :
        riderCleaned.append(BartLibs.RemoveSmallRiderCountsForStation(minRiders, n))
    allStatsInter, origList = BartLibs.IntersectAllStations(riderCleaned)
    return allStatsInter, origList

def TestMultipleRoutes(riderContTable):
    rejectHO, pVal = BartLibs.ChiSqTestNxN(riderContTable)
    return rejectHO, pVal

def CompareMultipleDayRidersTo(startDate, endDate, dest, hour, minStations, minRiders):

    propList = []
    start_date = startDate
    end_date = endDate
    delta = timedelta(days = 1)
    while start_date <= end_date:
        if start_date.weekday() < 5:
            sDate =  start_date.strftime("%m-%d-%Y")
            da = BARTQueries.GetDailyRidersTo(dest, hour, sDate)
            if len(da) > minStations:
                propList.append( da )
        start_date += delta

    if( len(propList) > 1 ):
        allStations, allStationsComplete = ScrubRiders(minRiders, propList)
        rejectHO, pVal = TestMultipleRoutes(allStations)
        print("MultiRiders From {0}, Reject: {3}, Num: {1}, PVal: {2}".format( dest, len(allStations), pVal, rejectHO ) )
    else:
        print("No Stations Found")


def CompareMultipleDayRidersFrom(startDate, endDate, origin, hour, minStations, minRiders):

    propList = []
    start_date = startDate
    end_date = endDate
    delta = timedelta(days = 1)
    while start_date <= end_date:
        if start_date.weekday() < 5:
            sDate =  start_date.strftime("%m-%d-%Y")
            da = BARTQueries.GetDailyRidersFrom(origin, hour, sDate)
            if len(da) > minStations:
                propList.append( da )
        start_date += delta

    if( len(propList) > 1 ):
        allStations, allStationsComplete = ScrubRiders(minRiders, propList)
        rejectHO, pVal = TestMultipleRoutes(allStations)
        print("MultiRiders To {0}, RejectHO: {3}, Num: {1}, PVal: {2}".format( origin, len(allStations), pVal, rejectHO ) )
        PlotMultiSets(allStationsComplete, "title")
    else:
        print("No Stations Found")


def CompareMultiDayRidersToYearlyAveDest(startDate, endDate, dest1, hour1, year1, minStations, minRiders):

    yearlyAvg = BARTQueries.GetYearlyAverageDailyRidersToDest(dest1, hour1, year1)

    start_date = startDate
    end_date = endDate
    delta = timedelta(days=1)
    while start_date <= end_date:
        if start_date.weekday() < 5:
            sDate =  start_date.strftime("%m-%d-%Y")
            da = BARTQueries.GetDailyRidersTo(dest1, hour1, sDate)
            if len(da) > minStations:
                dayYearPair = [da, yearlyAvg]
                allStations, allStationsComplete = ScrubRiders(minRiders, dayYearPair)
                rejectHO, pVal = TestMultipleRoutes( allStations)
                print("MultiRiders To {0}, Stats: {1}, RejectHO: {4}, PVal: {2}  Date: {3}".format(dest1, len(da), pVal, sDate, rejectHO))
                #CompareRouteProportions(da, yearlyAvg)
        start_date += delta

def CompareMultiDayRidersToYearlyAveFrom(startDate, endDate, source1, hour1, year1, minStations, minRiders):

    yearlyAvg = BARTQueries.GetYearlyAverageDailyRidersFromSource(source1, hour1, year1)

    start_date = startDate
    end_date = endDate
    delta = timedelta(days=1)
    while start_date <= end_date:
        if start_date.weekday() < 5:
            sDate =  start_date.strftime("%m-%d-%Y")
            da = BARTQueries.GetDailyRidersFrom(source1, hour1, sDate)
            if len(da) > minStations:
                dayYearPair = [da, yearlyAvg]
                allStations, allStationsComplete = ScrubRiders(minRiders, dayYearPair)
                rejectHO, pVal = TestMultipleRoutes(allStations)
                title = "MultiRiders From {0}, Stats: {1}\nRejectHO: {4}, PVal: {2:.5f}\nDate {3}".format(source1, len(da), pVal,                                                                                       sDate, rejectHO)
                print(title)
                PlotMultiSets(allStationsComplete, title)
                PlotTwoSets(allStationsComplete, sDate, year1, title)
                PlotTwoSetsTrueProp(allStationsComplete, sDate, year1, title)
                #CompareRouteProportions(da, yearlyAvg)
        start_date += delta


def PlotTwoSets(stats, lab1, lab2, title):
    cats = list(map(lambda x: x[2], stats[0]))
    d1 = list(map(lambda x: x[0], stats[0]))
    d2 = list(map(lambda x: x[0], stats[1]))
    X = np.arange( len(d1) )
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

    d1Scale = 100.0/max(d1)
    d2Scale = 100.0/max(d2)

    d1 = list(map(lambda x: x*d1Scale, d1))
    d2 = list(map(lambda x: x*d2Scale, d2))


    X = np.arange( len(d1) )
    plt.bar(X + 0.00, d1, color='b', width=0.25)
    plt.bar(X + 0.3, d2, color='r', width=0.25)
    plt.xticks(X, cats)
    plt.legend(labels=[lab1, lab2])
    plt.tick_params(labelrotation=45)

    plt.title(title)
    plt.show()

def PlotMultiSets(stats, title):
    cats = list(map(lambda x: x[2], stats[0]))
    X = np.arange(len(cats))
    barWidth = .25
    n = len(cats)/4
    for index, p in enumerate(stats):
        c = (random.random(), random.random(), random.random())
        d = list(map(lambda x: x[0], p))
        d = list(map(lambda x: x*100.0/max(d), d))
        plt.bar(X + (barWidth*index)/10, d, color=c, width=barWidth/2)

    plt.xticks(X + barWidth/2, cats)
    plt.tick_params(labelrotation=45)

    plt.title(title)
    plt.show()


def PlotComareRouteDistros(date1, hour1, pVal, plot1S, rejectHO, source1, year1):
    cat_names = list(map(lambda x: x[2], plot1S))
    # add data to bar chart
    le = len(plotData1)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.bar(cat_names, plotData1)
    ax2.bar(cat_names, plotData2)
    title1 = 'Daily Riders from {0}\nHour {1}, date {2}'.format(source1, hour1, date1)
    title2 = 'Average Annual {0}\nHour {1}, Year {2}'.format(source1, hour1, year1)
    ax1.set_title(title1)
    ax2.set_title(title2)
    hypTest = "Rider Proportion\nAlpha = '{0:.9f}'\nAccept H0 :'{1}' ".format(pVal, rejectHO)
    plt.suptitle(hypTest)
    ax1.tick_params(labelrotation=45)
    ax2.tick_params(labelrotation=45)
    myLocator = mticker.MultipleLocator(4)
    ax1.xaxis.set_major_locator(myLocator)
    ax2.xaxis.set_major_locator(myLocator)
    # set the spacing between subplots
    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=.7,
                        wspace=0.4,
                        hspace=0.4)
    plt.show()


def PlotYearlySumRidersPerOrigin(origin, year):
    hourlyRiders = BARTQueries.GetSumYearRidersPerHour(origin,year)
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