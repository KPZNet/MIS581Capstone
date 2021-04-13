import numpy as np
import statistics
import matplotlib.pyplot as plt
from statsmodels.graphics import tsaplots

from Code.DataBase import bart
from statsmodels.tsa.seasonal import seasonal_decompose

import BartLibs
import BARTQueries


def BARRunFFT():
    plotdata = BARTQueries.GetWeeklyRidersToEMBRAtHour()
    rawLen = len(plotdata)
    print("Lenght of BART data :", rawLen)
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


def TryDecomp():
    N = 256
    T = 1/N
    x = np.linspace(0.0, N*T, N, endpoint=False)
    y = 10*np.sin(5 * 2.0*np.pi*x) + 0.5*np.sin(10 * 2.0*np.pi*x)
    y = list(map(lambda x: x - statistics.mean(y), y))
    BartLibs.Decomposition(y,51)


def GetPITTDistro2014():
    plotData = BARTQueries.GetYearlyRiderDistFromPITT2014()

    #set total samples
    total_samples_bar_chart = len(plotData)
    #create category names from integers
    cat_names = list(map(lambda x: x[2], plotData))
    #create random data bars
    barValues = list(map(lambda x: x[0], plotData))
    #add data to bar chart
    plt.bar(cat_names, barValues)
    plt.suptitle('Pittsburg 2014')
    plt.xlabel('Category')
    plt.ylabel('Riders')
    plt.xticks(rotation=90)
    plt.show()

def GetPITTDistro2015():
    plotData14 = BARTQueries.GetYearlyRiderDistFromPITT2014()
    plotData15 = BARTQueries.GetYearlyRiderDistFromPITT2015()

    pData14 = list(map(lambda x: x[0], plotData14))
    pData15 = list(map(lambda x: x[0], plotData15))
    #set total samples
    total_samples_bar_chart = len(plotData14)
    #create category names from integers
    cat_names = list(map(lambda x: x[2], plotData14))
    #create random data bars
    barValues = list(map(lambda x: x[0], plotData14))
    #add data to bar chart
    prop14 = BartLibs.CalcProp(pData14)
    prop15 = BartLibs.CalcProp(pData15)
    le = len(pData14)
    X = np.arange(le)
    plt.bar(X + 0.00, prop14, color = 'b', width = 0.50)
    plt.bar(X + 0.60, prop15, color = 'r', width = 0.50)


    plt.show()

    #plt.suptitle('Pittsburg 2015')
    #plt.xlabel('Category')
    #plt.ylabel('Riders')
    #plt.xticks(rotation=90)
    #plt.show()

try:
    BARRunFFT()
    GetPITTDistro2014()
    GetPITTDistro2015()
    #CosFFT()

    #TryDecomp()

except(Exception) as e:
    print(e)
finally:
    print("Completed")


