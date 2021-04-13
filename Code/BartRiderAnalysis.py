import numpy as np
import statistics
import matplotlib.pyplot as plt
from statsmodels.graphics import tsaplots

from Code.DataBase import bart
from statsmodels.tsa.seasonal import seasonal_decompose

import BartLibs


def BARRunFFT():
    plotdata = GetBARTData_A()
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


def GetBARTData_A():
    global smoothData, scal
    query = """
                
        select avg(cast(riders as double precision)), dest, 
            extract(DOW from depart_date) as dow,
            extract(WEEK from depart_date) as week
        from hourlystationqueue
        where
                extract(ISODOW from depart_date) in (1,2,3,4,5)
          AND
                dest = 'EMBR'
          and
                depart_hour = 7
        
          and
                extract(YEAR from depart_date) in (2013,2014,2015,2017,2018)
        group by dest,  extract(WEEK from depart_date), 
                        extract(DOW from depart_date)
                
    """
    dat = bart.PGBartLocal(query)
    plotdata = list(map(lambda x: x[0], dat))
    return plotdata


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

try:
    BARRunFFT()
    #CosFFT()

    #TryDecomp()

except(Exception) as e:
    print(e)
finally:
    print("Completed")


