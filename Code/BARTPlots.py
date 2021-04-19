
import numpy as np
import statistics
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import BartLibs
import BARTQueries
from datetime import date, timedelta


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

def GetPITTDistroCompare():

    plotData14 = BARTQueries.GetAverageDailyRidersFromSource('PITT', 7, 2018)
    plotData15 = BARTQueries.GetAverageDailyRidersFromSource('PITT', 7, 2019)

    plotData14S, plotData15S = BartLibs.RemoveSmallRiderCounts(5, plotData14, plotData15)

    pData14 = list(map(lambda x: x[0], plotData14S))
    pData15 = list(map(lambda x: x[0], plotData15S))

    rejectHO, pVal = BartLibs.ChiSqTest(pData14, pData15)
    print("Reject HO: ", rejectHO, " p-value :", pVal)

    cat_names = list(map(lambda x: x[2], plotData14S))
    #add data to bar chart
    le = len(pData14)

    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.bar(cat_names, pData14)
    ax2.bar(cat_names, pData15)

    ax1.set_title("2014")
    ax2.set_title("2015")

    hypTest = "Rider Proportion\nAlpha = '{0:.9f}'\nAccept H0:'{1}' ".format(pVal,rejectHO)
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

def CompareMultipleDayRidersFrom():

    plotD = []

    start_date = date(2019, 4, 1)
    end_date = date(2019, 6, 1)
    delta = timedelta(days=1)
    while start_date <= end_date:
        if start_date.weekday() < 5:
            sDate =  start_date.strftime("%m-%d-%Y")
            da = BARTQueries.GetDailyRidersTo('PITT', 7, sDate)
            print (sDate, " Len: ", len(da) )
            if len(da) > 20:
                plotD.append( da )
        start_date += delta

    plotD_Data = []
    for n in plotD:
        plotD_Data.append(BartLibs.RemoveSmallRiderCountsForStation(5, n))

    allStatsInter, OrigList = BartLibs.IntersectAllStations(plotD_Data)
    rejectHO, pVal = BartLibs.ChiSqTestNxN(allStatsInter)
    print("Reject HO: ", not rejectHO, " p-value :", pVal)


def CompareMultipleDayRidersTo():

    plotD = []

    start_date = date(2019, 3, 1)
    end_date = date(2019, 4, 1)
    delta = timedelta(days=1)
    while start_date <= end_date:
        if start_date.weekday() < 5:
            sDate =  start_date.strftime("%m-%d-%Y")
            da = BARTQueries.GetDailyRidersFrom('PITT', 7, sDate)
            print (sDate, " Len: ", len(da) )
            if len(da) > 20:
                plotD.append( da )
        start_date += delta

    plotD_Data = []
    for n in plotD:
        plotD_Data.append(BartLibs.RemoveSmallRiderCountsForStation(5, n))

    allStatsInter, OrigList = BartLibs.IntersectAllStations(plotD_Data)
    rejectHO, pVal = BartLibs.ChiSqTestNxN(allStatsInter)
    print("Reject HO: ", not rejectHO, " p-value :", pVal)



def CompareDayRidersToYearlyAve(source1, hour1, date1, year1):

    plot1 = BARTQueries.GetDailyRiders(source1, hour1, date1)
    plot2 = BARTQueries.GetAverageDailyRidersFromSource(source1, hour1, year1)

    plot1S, plot2S = BartLibs.RemoveSmallRiderCounts(5, plot1, plot2)

    plotData1 = list(map(lambda x: x[0], plot1S))
    plotData2 = list(map(lambda x: x[0], plot2S))

    rejectHO, pVal = BartLibs.ChiSqTest(plotData1, plotData2)
    print("Reject HO: ", not rejectHO, " p-value :", pVal)

    cat_names = list(map(lambda x: x[2], plot1S))
    #add data to bar chart
    le = len(plotData1)

    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.bar(cat_names, plotData1)
    ax2.bar(cat_names, plotData2)

    title1 = 'Daily Riders from {0}\nHour {1}, date {2}'.format(source1, hour1, date1)
    title2 = 'Average Annual {0}\nHour {1}, Year {2}'.format(source1, hour1, year1)

    ax1.set_title(title1)
    ax2.set_title(title2)

    hypTest = "Rider Proportion\nAlpha = '{0:.9f}'\nAccept H0 :'{1}' ".format(pVal,rejectHO)
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



def CompareDailyRidersFromDestPerHour(hour1, source1, day1, month1, year1,
                                      hour2, source2, day2, month2, year2):

    plot1 = BARTQueries.GetDailyRiders(hour1, source1, day1, month1, year1)
    plot2 = BARTQueries.GetDailyRiders(hour2, source2, day2, month2, year2)

    plot1S, plot2S = BartLibs.RemoveSmallRiderCounts(5, plot1, plot2)

    plotData1 = list(map(lambda x: x[0], plot1S))
    plotData2 = list(map(lambda x: x[0], plot2S))

    rejectHO, pVal = BartLibs.ChiSqTest(plotData1, plotData2)
    print("Reject HO: ", rejectHO, " p-value :", pVal)

    cat_names = list(map(lambda x: x[2], plot1S))
    #add data to bar chart
    le = len(plotData1)

    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.bar(cat_names, plotData1)
    ax2.bar(cat_names, plotData2)

    ax1.set_title("2014")
    ax2.set_title("2015")

    hypTest = "Rider Proportion\nAlpha = '{0:.9f}'\nAccept H0:'{1}' ".format(pVal,rejectHO)
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

def CompareAverageDayRiders(hour1, source1, day1, year1,
                            hour2, source2, day2, year2):

    plot1 = BARTQueries.GetAverageDayRider(source1, hour1, day1, year1)
    plot2 = BARTQueries.GetAverageDayRider(source2, hour2, day2, year2)

    plot1S, plot2S = BartLibs.RemoveSmallRiderCounts(5, plot1, plot2)

    plotData1 = list(map(lambda x: x[0], plot1S))
    plotData2 = list(map(lambda x: x[0], plot2S))

    rejectHO, pVal = BartLibs.ChiSqTest(plotData1, plotData2)
    print("Reject HO: ", rejectHO, " p-value :", pVal)

    cat_names = list(map(lambda x: x[2], plot1S))
    #add data to bar chart
    le = len(plotData1)

    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.bar(cat_names, plotData1)
    ax2.bar(cat_names, plotData2)

    title1 = 'Ave Riders from {0}\nHour {1}, day {2}, Year {3}'.format(source1, hour1, day1, year1)
    title2 = 'Ave Riders from {0}\nHour {1}, day {2}, Year {3}'.format(source2, hour2, day2, year2)

    ax1.set_title(title1)
    ax2.set_title(title2)

    hypTest = "Rider Proportion\nAlpha = '{0:.9f}'\nAccept H0 :'{1}' ".format(pVal,rejectHO)
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

def CompareAverageDayRidersByMonth(source1, hour1, isodow1, month1, year1,
                                   source2, hour2, isodow2, month2, year2):

    plot1 = BARTQueries.GetAverageDayRiderByMonth(source1, hour1, isodow1, month1, year1)
    plot2 = BARTQueries.GetAverageDayRiderByMonth(source2, hour2, isodow2, month2, year2)

    plot1S, plot2S = BartLibs.RemoveSmallRiderCounts(5, plot1, plot2)

    plotData1 = list(map(lambda x: x[0], plot1S))
    plotData2 = list(map(lambda x: x[0], plot2S))

    rejectHO, pVal = BartLibs.ChiSqTest(plotData1, plotData2)
    print("Reject HO: ", rejectHO, " p-value :", pVal)

    cat_names = list(map(lambda x: x[2], plot1S))
    #add data to bar chart
    le = len(plotData1)

    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.bar(cat_names, plotData1)
    ax2.bar(cat_names, plotData2)

    title1 = 'Ave Riders from {0}\nHour {1}, day {2}, Month {3}, Year {4}'.format(source1, hour1, isodow1, month1, year1)
    title2 = 'Ave Riders from {0}\nHour {1}, day {2}, Month {3}, Year {4}'.format(source2, hour2, isodow2, month2, year2)

    ax1.set_title(title1)
    ax2.set_title(title2)

    hypTest = "Rider Proportion\nAlpha = '{0:.9f}'\nAccept H0 :'{1}' ".format(pVal,rejectHO)
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

def CompareTotalDayRidersByWeek(source1, hour1, day1, week1, year1,
                                source2, hour2, day2, week2, year2):

    plot1 = BARTQueries.GetTotalDayRiderByWeek(source1, hour1, day1, week1, year1)
    plot2 = BARTQueries.GetTotalDayRiderByWeek(source2, hour2, day2, week2, year2)

    plot1S, plot2S = BartLibs.RemoveSmallRiderCounts(5, plot1, plot2)

    plotData1 = list(map(lambda x: x[0], plot1S))
    plotData2 = list(map(lambda x: x[0], plot2S))

    rejectHO, pVal = BartLibs.ChiSqTest(plotData1, plotData2)
    print("Reject HO: ", rejectHO, " p-value :", pVal)

    cat_names = list(map(lambda x: x[2], plot1S))
    #add data to bar chart
    le = len(plotData1)

    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.bar(cat_names, plotData1)
    ax2.bar(cat_names, plotData2)

    title1 = 'Riders from {0}\nHour {1}, day {2}\n week {3}, Year {4}'.format(source1, hour1, day1, week1, year1)
    title2 = 'Riders from {0}\nHour {1}, day {2}\n week {3}, Year {4}'.format(source2, hour2, day2, week2, year2)

    ax1.set_title(title1)
    ax2.set_title(title2)

    hypTest = "Rider Proportion\nAlpha = '{0:.9f}'\nAccept H0 :'{1}' ".format(pVal,rejectHO)
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


def CompareTotalDayRidersByWeekToDest(dest1, hour1, day1, week1, year1,
                                dest2, hour2, day2, week2, year2):

    plot1 = BARTQueries.GetTotalDayRiderByWeekToDest(dest1, hour1, day1, week1, year1)
    plot2 = BARTQueries.GetTotalDayRiderByWeekToDest(dest2, hour2, day2, week2, year2)

    plot1S, plot2S = BartLibs.RemoveSmallRiderCounts(5, plot1, plot2)

    plotData1 = list(map(lambda x: x[0], plot1S))
    plotData2 = list(map(lambda x: x[0], plot2S))

    rejectHO, pVal = BartLibs.ChiSqTest(plotData1, plotData2)
    print("Reject HO: ", rejectHO, " p-value :", pVal)

    cat_names = list(map(lambda x: x[2], plot1S))
    #add data to bar chart
    le = len(plotData1)

    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.bar(cat_names, plotData1)
    ax2.bar(cat_names, plotData2)

    title1 = 'Riders to {0}\nHour {1}, day {2}\n week {3}, Year {4}'.format(dest1, hour1, day1, week1, year1)
    title2 = 'Riders to {0}\nHour {1}, day {2}\n week {3}, Year {4}'.format(dest2, hour2, day2, week2, year2)

    ax1.set_title(title1)
    ax2.set_title(title2)

    hypTest = "Rider Proportion\nAlpha = '{0:.9f}'\nAccept H0 :'{1}' ".format(pVal,rejectHO)
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

def ShowHourlyAverageRidersSource(source):
    plotData = BARTQueries.GetAverageDailySourceByHour(source)
    cat_names = list(map(lambda x: x[2], plotData))
    barValues = list(map(lambda x: x[0], plotData))
    plt.bar(cat_names, barValues)
    plt.suptitle('{0} Riders Avg by Hour'.format(source))
    plt.xlabel('Hour')
    plt.ylabel('Riders')
    plt.xticks(rotation=90)
    plt.show()

def ShowDailyRiders(hour, source, day, month, year):
    plotData = BARTQueries.GetDailyRiders(hour, source, day, month, year)
    cat_names = list(map(lambda x: x[2], plotData))
    barValues = list(map(lambda x: x[0], plotData))
    plt.bar(cat_names, barValues)
    plt.suptitle('{1} Riders AT Hour {0}, Day {2}, Month {3}, Year {4}'.format(hour, source, day, month, year))
    plt.xlabel('Dest')
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