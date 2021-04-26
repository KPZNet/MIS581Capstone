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
    # BARTPlots.PlotTotalRidersPerMonth()
    # BARTPlots.CompareRidersPerHourPerDayForStation("CONC", 2019)
    # BARTPlots.CompareRidersPerISODOWForStation2("CONC", 2019)
    # BARTPlots.TwoWayAnova('CONC', 2019)
    #
    # BARTPlots.PlotTotalRidersByHourBySource('CONC',2019)
    # BARTPlots.GetTotalRidersPerHourPerDayForStation('CONC', 2019)
    #
    # BARTPlots.RunBARTTimeSeries2("CONC", 7, 2019)
    #
    #BARTPlots.PlotRidersOnMap(2019)
    #BARTPlots.PlotRidersOnMapTo(2019)

    # BARTPlots.PlotYearlySumRidersPerOrigin("CONC", 2019)

    # BARTPlots.CompareMultiDayRidersToYearlyAveFrom(date(2019,3, 1),date(2019, 4, 1),'CONC', 7, 2019, 1, 5, 1)
    # BARTPlots.CompareMultiDayRidersToYearlyAveDest(date(2019, 11, 1),date(2019, 12, 30),'19TH', 8, 2019, 1, 5, 1)

    BARTPlots.CompareMultipleDayRidersFrom ( date ( 2019, 1, 1 ), date ( 2019, 12, 30 ), 'CONC', 7, 15, 5, 0, 1 )
    BARTPlots.CompareMultipleDayRidersTo(date(2019, 1, 1),date(2019, 12, 20), '19TH', 8, 20, 5, 0,1)
    #BARTPlots.PlotTotalRidersByHour(2019)
    #BARTPlots.CompareRidersPerISODOW(2019)

except(Exception) as e:
    print(e)
finally:
    print("Completed")


