__author__ = "Kenneth Ceglia"
__copyright__ = "Copyright 2021, MIS581 Capstone"
__credits__ = ["Kenneth Ceglia"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Kenneth Ceglia"
__email__ = "kenneth.ceglia@csuglobal.edu"
__status__ = "Course Level"

import statistics
from datetime import timedelta
from statistics import NormalDist

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import scipy.stats as st
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.tsa.stattools import adfuller

import BARTQueries
import BartLibs


def RunBARTTimeSeries2(source, hour, year):
    """
    Runs complete time series tests, outputs plot set and test results
    :param source: Station to test
    :param hour: Hour of day
    :param year: year
    """
    plotdata = BARTQueries.GetAveragedWeekdayRidersFromSource(source, hour, year)
    title = "Daily Riders for {0} at {1}:00AM in {2}".format(source, hour, year)
    PlotTimeSeriesWithLimitBars(plotdata, title)

    smoothData = BartLibs.Smooth_1StandardDeviation(plotdata)
    PlotTimeSeriesWithLimitBars(smoothData, title)

    PlotTimeSeriesFFT(smoothData, title)

    BartLibs.Decomposition(smoothData, 5)
    BartLibs.ACF(smoothData, 10)

    # ADF statistic to check stationary
    timeseries = adfuller(smoothData, autolag='AIC')
    pVal = timeseries[1]
    print("\n\n\nAugmented Dickey-Fuller Test: pval = {0}\n\n\n".format(pVal))
    # if timeseries[0] > timeseries[4]["5%"] :
    if pVal > 0.05:
        print("Failed to Reject Ho - Time Series is Non-Stationary")
    else:
        print("Reject Ho - Time Series is Stationary")

    model = sm.tsa.UnobservedComponents(smoothData,
                                        level='fixed intercept',
                                        freq_seasonal=[{'period': 50,
                                                        'harmonics': 5}])
    res_f = model.fit(disp=False)
    print(res_f.summary())
    # The first state variable holds our estimate of the intercept
    print("fixed intercept estimated as {0:.3f}".format(res_f.smoother_results.smoothed_state[0, -1:][0]))

    res_f.plot_components()
    plt.show()


def PlotTimeSeriesFFT(smoothData, title):
    """
    Plots an FFT from time series data
    :param smoothData: time series data
    :param title: title to place on plot
    """
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


def PlotTimeSeriesWithLimitBars(plotdata, title, showBars=True):
    """
    Plot a time series line chart with standard error bars
    :param plotdata: input time series list of data
    :param title: title to put on plot
    :param showBars: show or hide error bars
    """
    rawLen = len(plotdata)
    x = list(range(rawLen))
    plt.plot(x, plotdata,
             color='blue',
             linewidth=1
             )
    if showBars:
        sdv = statistics.stdev(plotdata)
        mn = statistics.mean(plotdata)
        Maxthreshold = mn + (2.0 * sdv)
        Minthreshold = mn - (2.0 * sdv)
        plt.hlines(Maxthreshold, 0, rawLen, colors="red")
        plt.hlines(Minthreshold, 0, rawLen, colors="red")
    plt.suptitle(title)
    plt.show()


def PrintRoutes(propList):
    """
    Prints out a route with details for all stations in route
    :param propList: list of input stations
    """
    for n in propList:
        stns = len(n)
        rdr = BartLibs.GetTotRiders(n)
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
        rdrBRem = BartLibs.GetTotRiders(n)
        numStnsBRem = len(n)
        g = BartLibs.RemoveSmallRiderCountsForStation(minRiders, n)
        rdr = BartLibs.GetTotRiders(g)
        numStns = len(g)
        if numStns >= minStations and rdr > minNumber:
            riderCleaned.append(g)
        else:
            dtd = n[0][4]
            str = "SCRUBBED: Date:{0}, Stations:{1}, Riders:{2} - CStations:{3}, CRiders:{4}".format(dtd, numStns, rdr,
                                                                                                     numStnsBRem,
                                                                                                     rdrBRem)
            print(str)

    allStatsInter, origList = BartLibs.IntersectAllStations(riderCleaned)
    return allStatsInter, origList


def TestMultipleRoutes(riderContTable):
    """
    Tests multiple route variables over time for goodness of fit
    :param riderContTable: route contengency table
    :return: returns chi-square H0 result, and p-value
    """
    rejectHO, pVal = BartLibs.ChiSqTestNxN(riderContTable)
    return rejectHO, pVal


def TestMultipleRoutesAnova(df):
    """
    Run ANOVA on multiple routes to compare means of station riders
    produces boxplot, outputs ANOVA test results
    :param df: dataframe of routes
    """
    PlotRouteDestinations(df, 10)

    model = ols('riders ~ C(dest)', data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print(anova_table)


def PlotRouteDestinations(df, minRiders):
    """
    Plot a boxplot of multiple routes for means comparison
    :param df: dataframe of multiple routes
    :param minRiders: min number of riders per route to consider
    """
    try:
        if True:
            dlist = []
            plotList = df.dest.unique().tolist()
            for p in plotList:
                dlist.append(df[df['dest'] == p].riders.tolist())

            plt.boxplot(dlist, labels=plotList, vert=False, showmeans=True)
            plt.title("Rider by Stations")
            plt.xlabel('Riders')
            plt.ylabel('Station')
            plt.xticks(rotation=90)
            plt.show()

        if False:
            df = df[df['riders'] > minRiders]
            boxplot = df.boxplot(column=['riders'], by="dest", showfliers=False)
            boxplot.show()
    except:
        pass


def CompareMultipleDayRidersTo(startDate, endDate, dest, hour, minStations, minRiders, minNumber, dayInterval):
    """
    Compares multiple routes over time frame
    Cleans stations, intersects and create route contingency table
    Produces plots, goodness of fit tests
    :param startDate: Start date for route query
    :param endDate:  End date for route query
    :param dest: The destination station
    :param hour: The hour to query
    :param minStations: Min number of stations to intersect to be considered in test table
    :param minRiders: Min riders to consider for each route station (min must be > 5)
    :param minNumber: Min number of total riders for train to be considered
    :param dayInterval: Skip day interval
    """
    propList = []
    start_date = startDate
    end_date = endDate
    delta = timedelta(days=dayInterval)
    while start_date <= end_date:
        if start_date.weekday() < 5:
            sDate = start_date.strftime("%m-%d-%Y")
            da, df = BARTQueries.GetDailyRidersTo(dest, hour, sDate)
            if len(da) > 0:
                propList.append(da)
        start_date += delta

    if (len(propList) > 1):
        PrintRoutes(propList)
        allStations, allStationsComplete = ScrubRiders(propList, minRiders, minStations, minNumber)

        stations = len(allStationsComplete[0])
        rejectHO, pVal = TestMultipleRoutes(allStations)
        title = "Tuesday From {0}, RejectHO: {3}\n PVal: {2:.5f}, Days: {1}, Stations:{4} ".format(dest,
                                                                                                   len(allStations),
                                                                                                   pVal, rejectHO,
                                                                                                   stations)
        print(title)
        PlotMultiSetsTo(allStationsComplete, 1, title)
        dropRidersPerc = BartLibs.CalcDroppedRiders(propList, allStationsComplete)
        PrintRoutes(allStationsComplete)

        Plot3DRoutesTo(allStationsComplete, 1, title)
        PlotTimeSeriesRoutesTo(allStationsComplete, 1, title)
    else:
        print("No Stations Found")


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


def confidence_interval(data, confidence=0.95):
    """
    Return confidence limits for input data array
    :param data: array of rider data
    :param confidence: percentage of bands
    :return: confidence bands upper and lower
    """
    dist = NormalDist.from_samples(data)
    z = NormalDist().inv_cdf((1 + confidence) / 2.)
    h = dist.stdev * z / ((len(data) - 1) ** .5)
    return dist.mean - h, dist.mean + h


def PlotMeanRidersPerStation(df, allStationsComplete):
    """

    :param df:
    :param allStationsComplete:
    """
    stationList = df.dest.unique()
    x = []
    y = []
    errs = []
    for s in stationList:
        data = df[df['dest'] == s].riders.tolist()
        xmean = np.mean(data)
        sr = st.t.interval(0.95, len(data) - 1, loc=xmean, scale=st.sem(data))
        # mul = st.DescrStatsW(data).tconfint_mean()
        x.append(xmean)
        c1, c2 = confidence_interval(data)
        errs.append(abs(xmean - c1))

    yRange = list(range(len(stationList)))
    plt.figure()

    plt.errorbar(x, yRange, xerr=errs, fmt='o', color='k')
    plt.yticks(yRange, stationList)
    plt.show()


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

        df = AllStationsToDF(allStationsComplete)
        PlotMeanRidersPerStation(df, allStationsComplete)

        rejectHO, pVal = TestMultipleRoutes(allStations)
        TestMultipleRoutesAnova(df)
        title = "Tuesday From {0}, RejectHO: {3}\n PVal: {2:.5f}, Days: {1}, Stations:{4} ".format(origin,
                                                                                                   len(allStations),
                                                                                                   pVal, rejectHO,
                                                                                                   stations)
        print(title)
        PlotMultiSetsTo(allStationsComplete, 2, title)
        dropRidersPerc = BartLibs.CalcDroppedRiders(propList, allStationsComplete)
        PrintRoutes(allStationsComplete)

        Plot3DRoutesTo(allStationsComplete, 2, title)
        PlotTimeSeriesRoutesTo(allStationsComplete, 2, title)
    else:
        print("No Stations Found")


def CompareMultiDayRidersToYearlyAveDest(startDate, endDate, dest1, hour1, year1, minStations, minRiders, interval):
    yearlyAvg = BARTQueries.GetYearlyAverageDailyRidersToDest(dest1, hour1, year1)

    start_date = startDate
    end_date = endDate
    delta = timedelta(days=interval)
    while start_date <= end_date:
        if start_date.weekday() < 5:
            sDate = start_date.strftime("%m-%d-%Y")
            da, df = BARTQueries.GetDailyRidersTo(dest1, hour1, sDate)
            if len(da) > 0:
                dayYearPair = [da, yearlyAvg]
                allStations, allStationsComplete = ScrubRiders(dayYearPair, minRiders, minStations, minRiders)
                rejectHO, pVal = TestMultipleRoutes(allStations)
                title = "{0}, Stats: {1}RejectHO: {4}\nPVal: {2:.5f} Date {3}".format(dest1,
                                                                                      len(da), pVal,
                                                                                      sDate,
                                                                                      rejectHO)
                print(title)
                yr = "{0} Expected".format(year1)
                # PlotTwoSets(allStationsComplete, sDate, year1, 1,title)
                PlotTwoSetsTrueProp(allStationsComplete, sDate, yr, 1, title)

        start_date += delta


def CompareMultiDayRidersToYearlyAveFrom(startDate, endDate, source1, hour1, year1, minStations, minRiders, interval):
    yearlyAvg = BARTQueries.GetYearlyAverageDailyRidersFromSource(source1, hour1, year1)

    start_date = startDate
    end_date = endDate
    delta = timedelta(days=interval)
    while start_date <= end_date:
        if start_date.weekday() < 5:
            sDate = start_date.strftime("%m-%d-%Y")
            da, df = BARTQueries.GetDailyRidersFrom(source1, hour1, sDate)
            if len(da) > 0:
                dayYearPair = [da, yearlyAvg]
                allStations, allStationsComplete = ScrubRiders(dayYearPair, minRiders, minStations, minRiders)
                rejectHO, pVal = TestMultipleRoutes(allStations)
                title = "{0}, Stats: {1}RejectHO: {4}\nPVal: {2:.5f} Date {3}".format(source1,
                                                                                      len(da), pVal,
                                                                                      sDate,
                                                                                      rejectHO)
                print(title)
                # PlotTwoSets(allStationsComplete, sDate, year1, 2,title)
                PlotTwoSetsTrueProp(allStationsComplete, sDate, year1, 2, title)

        start_date += delta


def CompareMultiDayRidersToExpectedFrom(startDate, endDate, source1, hour1, year1, minStations, minRiders, interval):
    yearlyAvg = BARTQueries.GetYearlyAverageDailyRidersFromSource(source1, hour1, year1)

    start_date = startDate
    end_date = endDate
    delta = timedelta(days=interval)
    while start_date <= end_date:
        if start_date.weekday() < 5:
            sDate = start_date.strftime("%m-%d-%Y")
            da, df = BARTQueries.GetDailyRidersFrom(source1, hour1, sDate)
            if len(da) > 0:
                dayYearPair = [da, yearlyAvg]
                allStations, allStationsComplete = ScrubRiders(dayYearPair, minRiders, minStations, minRiders)
                rejectHO, pVal = TestMultipleRoutes(allStations)
                title = "{0}, Stats: {1}RejectHO: {4}\nPVal: {2:.5f} Date {3}".format(source1,
                                                                                      len(da), pVal,
                                                                                      sDate,
                                                                                      rejectHO)
                print(title)
                # PlotTwoSets(allStationsComplete, sDate, year1, 2,title)
                PlotTwoSetsTrueProp(allStationsComplete, sDate, year1, 2, title)

        start_date += delta


def PlotStationDistribution(df, station, title):
    # df = df.astype({"dest":'category'})
    df = df.astype({"riders": 'int64'})

    df = df[df['dest'] == station]
    d1 = df[df['riders'] > 150].riders.tolist()

    plt.hist(d1)
    plt.show()


def PlotStationUsage(stats, title):
    cats = list(map(lambda x: x[2], stats))
    d1 = list(map(lambda x: x[0], stats))

    X = np.arange(len(d1))
    plt.bar(X + 0.00, d1, color='b', width=0.25)
    plt.xticks(X, cats)
    plt.tick_params(labelrotation=45)

    plt.title(title)
    plt.show()


def PlotRouteSet(stats):
    sDate = stats[0][4]
    sDate = sDate.strftime("%m-%d-%Y")
    cats = list(map(lambda x: x[2], stats))
    d1 = list(map(lambda x: x[0], stats))

    d1Scale = 100.0 / max(d1)
    d1 = list(map(lambda x: x * d1Scale, d1))

    X = np.arange(len(d1))
    plt.bar(X + 0.00, d1, color='b', width=0.25)
    plt.xticks(X, cats)
    plt.tick_params(labelrotation=45)

    plt.title(sDate)
    plt.show()


def PlotTwoSets(stats, lab1, lab2, statIndex, title):
    cats = list(map(lambda x: x[statIndex], stats[0]))
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


def PlotTwoSetsTrueProp(stats, lab1, lab2, statIndex, title):
    cats = list(map(lambda x: x[statIndex], stats[0]))
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


def PlotMultiSetsTo(stats, statIndex, title):
    cats = list(map(lambda x: x[statIndex], stats[0]))
    N = len(cats)
    ns = len(stats)
    X = np.arange(N)
    barWidth = .25
    spread = (ns / 2)

    plt.rcParams["axes.prop_cycle"] = plt.cycler("color", plt.cm.tab20b.colors)
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


def PlotTotalRidersByHour(year):
    hourlyRiders, df = BARTQueries.GetTotalRidersPerHour(year)

    plt.bar(df['hour'], df['riders'])
    plt.suptitle('Total Riders by Hour : {0}'.format(year))
    plt.xlabel('Departure Hour')
    plt.ylabel('Riders')
    plt.xticks(rotation=0)
    plt.show()


def PlotAverageRidersByHour(year):
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
    labels = []
    data = []

    for i in range(4, 21):
        dv = df[df['hour'] == i].riders.tolist()
        labels.append(str(i))
        data.append(dv)

    # Creating plot
    bp = plt.boxplot(data, labels=labels, showfliers=False)
    plt.title("Riders by Hour, Station: {0}, Year:{1}".format(source, year))
    plt.xlabel('Departure Hour')
    plt.ylabel('Riders')
    # show plot
    plt.show()


def CompareRidersPerISODOW(year):
    hourlyRiders, df = BARTQueries.GetTotalRidersPerDOW(year)

    labels = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri']

    plt.bar(labels, df['riders'])
    plt.suptitle('Total Riders by Day : {0}'.format(year))
    plt.xlabel('Departure Hour')
    plt.ylabel('Riders')
    plt.xticks(rotation=0)
    plt.show()


def TwoWayAnova(source, year):
    hourlyRiders, df = BARTQueries.GetTotalRidersPerHourPerDOWForStationTEXT(source, year)
    # perform two-way ANOVA
    model = ols('riders ~ C(hour) + C(isodow) + C(hour):C(isodow)', data=df).fit()
    g = sm.stats.anova_lm(model, typ=2)
    print(g)


def PlotRidersOnMap(year):
    px.set_mapbox_access_token(open(".mapbox_token").read())

    dat, df = BARTQueries.GetTotalRidersInNetworkByHourFrom(7, year)

    fig = px.scatter_mapbox(df,
                            lat='lat', lon='long', size='riders',
                            color_continuous_scale=px.colors.cyclical.IceFire,
                            size_max=15, zoom=1)

    fig.show()

    df = df[df['riders'] > 4000]

    plt.barh(df['source'], df['riders'])
    plt.suptitle('Total Riders Departing Station : {0}'.format(year))
    plt.xlabel('Stations')
    plt.ylabel('Riders')
    plt.xticks(rotation=45)
    plt.show()


def PlotRidersOnMapTo(year):
    px.set_mapbox_access_token(open(".mapbox_token").read())

    dat, df = BARTQueries.GetTotalRidersInNetworkByHourTo(8, year)

    fig = px.scatter_mapbox(df, lat='lat', lon='long', size='riders',
                            color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)

    fig.show()

    df = df[df['riders'] > 4000]

    plt.barh(df['source'], df['riders'])
    plt.suptitle('Total Riders Arriving Station: {0}'.format(year))
    plt.xlabel('Stations')
    plt.ylabel('Riders')
    plt.xticks(rotation=45)
    plt.show()


def Plot3DRoutesTo(allStations, statIndex, title):
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')

    vals = []
    stations = list(map(lambda x: x[statIndex], allStations[0]))

    x = []
    y = []

    zBottom = []
    daynum = 0
    for d in allStations:
        statnum = 0
        for c in d:
            vals.append(c[0])
            zBottom.append(0)

            x.append(daynum)
            y.append(statnum)

            statnum = statnum + 1
        daynum = daynum + 1

    ax1.bar3d(x, y, zBottom, 1, 1, vals)

    ax1.w_yaxis.set_ticklabels(stations)
    ax1.set_xlabel('Days')
    ax1.set_ylabel('Stations')
    ax1.set_zlabel('Riders')
    plt.title(title)
    plt.show()


def PlotTimeSeriesRoutesTo(allStations, statIndex, title):
    allStations = NormalizeAllStationsData(allStations)

    listOrigins = list(zip(*allStations))

    plt.subplots(figsize=(12, 8))
    stations = list(map(lambda x: x[statIndex], allStations[0]))

    for i, station in enumerate(listOrigins):
        vals = []
        for day in station:
            vals.append(day[0])

        x = list(range(len(vals)))
        plt.plot(x, vals,
                 linewidth=1,
                 label=stations[i]
                 )
    plt.legend()
    plt.title(title)
    plt.show()


def NormalizeAllStationsData(allStations):
    for index, p in enumerate(allStations):
        d = list(map(lambda x: x[0], p))
        d = list(map(lambda x: x * 100.0 / max(d), d))
        for j, s in enumerate(p):
            listT = list(s)
            listT[0] = d[j]
            tupleL = tuple(listT)
            p[j] = tupleL
    return allStations


def PlotTotalRidersPerMonth():
    plotdata, df = BARTQueries.GetTotalRidersPerMonth()
    df = df[df['year'] < 2020]
    df = df[df['year'] > 2015]
    title = "Riders per Month 2016 to 2019"
    PlotTimeSeriesWithLimitBars(df['riders'], title, False)

    # Initialise and fit linear regression model using `statsmodels`
    model = ols('riders ~ rMonth', data=df)
    model = model.fit()
    a = model.params
    print(a)
    print(model.summary())
    month_predict = model.predict()

    plt.plot(df['rMonth'], df['riders'])  # scatter plot showing actual data
    plt.plot(df['rMonth'], month_predict, 'r', linewidth=2)  # regression line
    plt.xlabel('Months 2016 to 2019')
    plt.ylabel('Riders')
    plt.title('Riders per Month 2016 to 2019')

    plt.show()
