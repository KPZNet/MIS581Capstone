import decimal
import numpy as np
import statistics
import matplotlib.pyplot as plt
from statsmodels.graphics import tsaplots

from Code.DataBase import bart
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.ticker as mticker

import BartLibs
import BARTQueries


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
    plt.plot(realAmplitudesScaled[:int(realAmpsLen / 2.0)])
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


def BARRunFFT():
    plotdata = BARTQueries.GetAveragedWeekdayRidersToDest('EMBR', 7, '(2013,2014,2015,2016,2017,2018,2019)')
    rawLen = len(plotdata)
    print("Length of BART data :", rawLen)
    smoothData = BartLibs.Smooth_1StandardDeviation(plotdata)

    BartLibs.Decomposition(smoothData, 5)
    BartLibs.ACF(smoothData, 10)

    smoothLen = len(smoothData)
    x = list(range(smoothLen))

    plt.plot(x, smoothData,
             color='blue',
             linewidth=1
             )
    sdv = statistics.stdev(plotdata)
    mn = statistics.mean(plotdata)
    Maxthreshold = mn + (2.0 * sdv)
    Minthreshold = mn - (2.0 * sdv)
    plt.hlines(Maxthreshold, 0, smoothLen, colors="red")
    plt.hlines(Minthreshold, 0, smoothLen, colors="red")
    plt.show()
    #smoothData = smoothData[:256]
    smoothData = list(map(lambda x: x - statistics.mean(smoothData), smoothData))
    print("Smoothed Mean: ",statistics.mean(smoothData))
    ft = np.fft.fft(smoothData)
    rt = list(map(lambda x: BartLibs.SumSquares(x), ft))
    le = len(rt)
    scal = 2 / le
    rt = list(map(lambda x: scal * x, rt))
    plt.plot(rt[:int(le/2)])
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

    plotData14 = BARTQueries.GetAverageDailyDestFrom('PITT', 7, 2018)
    plotData15 = BARTQueries.GetAverageDailyDestFrom('PITT', 7, 2019)

    plotData14S, plotData15S = BartLibs.RemoveSmallStations(5, plotData14, plotData15)

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

    hypTest = "Rider Proportion\nAlpha = '{0:.9f}'\nReject H0:'{1}' ".format(pVal,rejectHO)
    plt.suptitle(hypTest)

    ax1.tick_params(labelrotation=45)
    ax2.tick_params(labelrotation=45)

    myLocator = mticker.MultipleLocator(4)
    ax1.xaxis.set_major_locator(myLocator)
    ax2.xaxis.set_major_locator(myLocator)

    #plt.setp(ax1.get_xticklabels(), rotation=30, horizontalalignment='right', fontsize='x-small')
    # set the spacing between subplots
    plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=.7,
                    wspace=0.4,
                    hspace=0.4)
    plt.show()

    rejectHO, pVal = BartLibs.ChiSqTest(pData14, pData15)
    print("Reject HO: ", rejectHO, " p-value :", pVal)

def ShowAverageDailyDestFrom():
    plotData = BARTQueries.GetAverageDailyDestFrom('PITT', 7, 2018)

    #create category names from integers
    cat_names = list(map(lambda x: x[2], plotData))
    #create random data bars
    barValues = list(map(lambda x: x[0], plotData))
    #add data to bar chart
    plt.bar(cat_names, barValues)
    plt.suptitle('Rider Distro')
    plt.xlabel('Category')
    plt.ylabel('Riders')
    plt.xticks(rotation=90)
    plt.show()

try:
    RunBARTTimeSeries()
    GetPITTDistroCompare()

    ShowAverageDailyDestFrom()

except(Exception) as e:
    print(e)
finally:
    print("Completed")


