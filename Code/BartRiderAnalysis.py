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
import BARTPlots


try:
    # BARTPlots.ShowHourlyAverageRidersSource('PITT')
    # BARTPlots.RunBARTTimeSeries()
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
    #                                          'PITT', 7, 1, 4, 2019)


    #BartLibs.ChiSqTestExp()
     BARTPlots.CompareTotalDayRidersByWeek('PITT', 7, (1,2,3,4,5), 2, 2018,
                                           'PITT', 7, (1,2,3,4,5), 11, 2018)

    # BARTPlots.CompareTotalDayRidersByWeekToDest('EMBR', 7, (1,2,3,4,5), 8, 2018,
    #                                       'EMBR', 7, (1,2,3,4,5), 9, 2018)

    # BARTPlots.CompareTotalDayRidersByWeek('PITT', 7, 1, 5, 2018,
    #                                       'PITT', 7, 2, 5, 2018)

except(Exception) as e:
    print(e)
finally:
    print("Completed")


