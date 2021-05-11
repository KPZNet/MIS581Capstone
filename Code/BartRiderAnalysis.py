__author__ = "Kenneth Ceglia"
__copyright__ = "Open Source"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Kenneth Ceglia"
__email__ = "kenceglia@gmail.com"
__status__ = "Course Work"

""" BartRiderAnalysis is the main entry point and executes different
    functions to plot, test, clean or wrangle data
    This file contains all calling functions and serves as main line application
    for Capstone project
"""
from datetime import date

import numpy.random
import time
import BartLibs
import BARTPlots


try:
    #Start for marking execution time
    start_time = time.time()

    #RQ1
    #Boxplot Riders by Hour for Year, ANOVA for hours and days
    BARTPlots.CompareRidersPerHourPerDayForStation("CONC", 2019)
    BARTPlots.CompareRidersPerISODOWForStation2("CONC", 2019)
    BARTPlots.TwoWayAnova('CONC', 2019)

    #General plots for various descriptive stats
    BARTPlots.PlotTotalRidersByHour(2019)
    BARTPlots.CompareRidersPerISODOW(2019)
    BARTPlots.PlotTotalRidersByHourBySource('CONC',2019)
    BARTPlots.GetTotalRidersPerHourPerDayForStation('CONC', 2019)
    BARTPlots.PlotYearlySumRidersPerOrigin("CONC", 2019)

    #Timeseries and autocorrelation views and tests
    BARTPlots.RunBARTTimeSeries2("CONC", 7, 2019)

    #Map overlays for stations and rider levels
    BARTPlots.PlotRidersOnMap(2019)
    BARTPlots.PlotRidersOnMapTo(2019)

    #RQ2 RQ3
    #Rider contigency tables comparing riders for the year
    BARTPlots.CompareMultipleDayRidersFrom ( date ( 2019, 1, 1 ), date ( 2019, 12, 30 ), 'CONC', 7, 15, 5, 0, 1 )
    BARTPlots.CompareMultipleDayRidersTo(date(2019, 1, 1),date(2019, 12, 30), '19TH', 8, 20, 5, 0,1)

    #Compare riders per day with yearly averages
    BARTPlots.CompareMultiDayRidersToYearlyAveFrom(date(2019,4, 1),date(2019, 5, 1),'CONC', 7, 2019, 1, 5, 1)
    BARTPlots.CompareMultiDayRidersToYearlyAveDest(date(2019, 12, 1),date(2019, 12, 30),'19TH', 8, 2019, 1, 5, 1)

    #RQ4
    #Regression Fit
    BARTPlots.PlotTotalRidersPerMonth()


    #Print out execution time
    print("\n\n\nEXECUTION Time : %s seconds " % (time.time() - start_time))

except(Exception) as e:
    print("<<< EXCEPTION >>>")
    print(e)
finally:
    print("Completed")


