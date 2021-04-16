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
    # BARTPlots.CompareDailyRidersFromDestPerHour(7, 'PITT', 16, 3, 2015,
    #                                             7, 'PITT', 15, 4, 2015)

    BARTPlots.CompareAverageDayRiders(7, 'PITT', 1,  2018,
                                      9, 'PITT', 2,  2018)

except(Exception) as e:
    print(e)
finally:
    print("Completed")


