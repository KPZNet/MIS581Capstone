import decimal
import numpy as np
import statistics
import matplotlib.pyplot as plt
from statsmodels.graphics import tsaplots

from Code.DataBase import bart
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.ticker as mticker
from datetime import date, timedelta

import BartLibs
import BARTQueries
import BARTPlots


try:
    #BARTPlots.CompareRidersPerHourPerDayForStation("CONC", 2019)
    #BARTPlots.CompareRidersPerISODOWForStation2("CONC", 2019)
    #BARTPlots.TwoWayAnova('CONC', 2019)
    #BARTPlots.PlotTotalRidersByHourBySource('PHIL',2019)
    #BARTPlots.GetTotalRidersPerHourPerDayForStation('PITT', 2019)

    # BARTPlots.ShowHourlyAverageRidersSource('PITT')
    #BARTPlots.RunBARTTimeSeries2("CONC", 7, 2019)
    #BARTPlots.RunBARTTimeSeries()

    #BARTPlots.PlotRidersOnMap(2019)
    #BARTPlots.PlotRidersOnMapTo(2019)
    #BartLibs.ChiSqTestExp()
    #BARTPlots.PlotYearlySumRidersPerOrigin("PITT", 2019)

    BARTPlots.CompareMultiDayRidersToYearlyAveFrom(date(2019, 2, 1),date(2019, 7, 1),'CONC', 7, 2019, 1, 5)
    #BARTPlots.CompareMultiDayRidersToYearlyAveDest(date(2019, 2, 1),date(2019, 7, 1),'MONT', 8, 2017, 20, 5)

    #BARTPlots.CompareMultipleDayRidersFrom ( date ( 2019, 1, 1 ), date ( 2019, 12, 30 ), 'CONC', 7, 20, 5, 0, 1 )
    #BARTPlots.CompareMultipleDayRidersTo(date(2019, 1, 1),date(2019, 12, 28), '19TH', 8, 17, 5, 500,1)

    #BARTPlots.CompareMultipleDayRidersFrom ( date ( 2019, 1, 1 ), date ( 2019, 12, 30 ), 'SFIA', 7, 5, 5, 0, 1 )




except(Exception) as e:
    print(e)
finally:
    print("Completed")


