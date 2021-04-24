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
    # BARTPlots.ShowAverageDailyRidersFromSource('PITT', 7, 2016)
    # BARTPlots.GetPITTDistroCompare()

    # BARTPlots.ShowDailyRiders(7, 'PITT', 11, 3, 2015)
    # BARTPlots.ShowDailyRiders(7, 'PITT', 11, 4, 2015)
    #

    # BARTPlots.CompareDailyRidersFromDestPerHour(7, 'PITT', 2, 3, 2015,
    #                                              7, 'PITT', 8, 3, 2015)

    # BARTPlots.ShowAverageWeeklyRiderForHour('EMBR', 7, '(2013,2014,2015,2016,2017,2018,2019)')
    # BARTPlots.CompareAverageDayRiders(7, 'PITT', 1,  2018,
    #                                   7, 'PITT', 1,  2019)

    # BARTPlots.CompareAverageDayRidersByMonth('PITT', 7, 1, 4, 2019,
    #                                          'PITT', 7, 1, 3, 2019)

    #BARTPlots.PlotRidersOnMap(2019)
    #BARTPlots.PlotRidersOnMapTo(2019)
    #BartLibs.ChiSqTestExp()
    #BARTPlots.PlotYearlySumRidersPerOrigin("PITT", 2019)
    #BARTPlots.CompareMultiDayRidersToYearlyAveFrom(date(2019, 2, 1),date(2019, 7, 1),'PITT', 7, 2017, 20, 5)
    #BARTPlots.CompareMultiDayRidersToYearlyAveDest(date(2019, 2, 1),date(2019, 7, 1),'MONT', 8, 2017, 20, 5)
    #BARTPlots.CompareMultipleDayRidersFrom(date(2019, 1, 1),date(2019, 12, 30), 'PHIL', 7, 19, 5, 0, 1)
    #BARTPlots.CompareMultipleDayRidersFrom ( date ( 2019, 1, 1 ), date ( 2019, 12, 30 ), 'CONC', 7, 20, 5, 0, 1 )
    BARTPlots.CompareMultipleDayRidersTo(date(2019, 1, 1),date(2019, 12, 28), '19TH', 8, 17, 5, 500,1)




except(Exception) as e:
    print(e)
finally:
    print("Completed")


