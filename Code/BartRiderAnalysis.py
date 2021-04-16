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
    BARTPlots.ShowHourlyAverageRidersSource('PITT')
    BARTPlots.RunBARTTimeSeries()
    BARTPlots.ShowAverageDailyDestFrom()
    BARTPlots.GetPITTDistroCompare()

except(Exception) as e:
    print(e)
finally:
    print("Completed")


