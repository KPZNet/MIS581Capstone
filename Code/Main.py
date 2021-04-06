import requests
import numpy as np
import statistics
import csv
import os
from datetime import timedelta, date
import calendar
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import bart



query = 'select sum(riders), dest, date' \
        '      from hourlystationqueue' \
        '     where '\
            '            extract(ISODOW from depart_date) in (1,2,3,4,5) '\
        '       AND '\
        '             dest = \'EMBR\' '\
            '    and ' \
        '              hour = 7 '  \
        '      and date <   \'10-Dec-2015\'   ' \
        '      and ' \
        '           extract(YEAR from date) in (2015)  ' \
        '     group by dest, date     ' 

dat = bart.PGBart(query)
plotdata = dat[:,1]


#define number of samples to plot
total_samples_line_chart = 50

#create x independent data
x = list( range(total_samples_line_chart) )
#generate three data sets of random values spaced throughout Y scales
y1 = np.random.normal(100, 50, total_samples_line_chart) 
y2 = np.random.normal(1000, 75, total_samples_line_chart) 
#make this set a function of correlated data set with some random noise added
y3 = list( map(AddRandomNoise, y2) ) 
y4 = np.random.normal(300, 20, total_samples_line_chart) 
#create plot figure and give it a good size
fig, ax1 = plt.subplots(figsize = (20,5))
#add curves to plot
p1, =ax1.plot(x, y1, 
        color='red',   
        linewidth=0.75,  
        linestyle='--', label = "Boiler"
        )
p2, =ax1.plot(x, y2, 
        color='green',   
        linewidth=2.0, label = "Reactor"
        )
p3, =ax1.plot(x, y3, 
        color='blue',   
        linewidth=1 , label = "Gearbox"
        )  
#create second Y axis sharing the same X axis   
ax2 = ax1.twinx()
#add data to the new Y axis
p4, =ax2.plot(x, y4, 
        color='purple',   
        linewidth=2, label = "Fuel Line"
        )    
ax2.set_ylim(0,700) 
#add a title
plt.suptitle('Line Chart with Multiple Y Units')
#set labels
ax1.set_xlabel('Seconds')
ax1.set_ylabel('Scale 1 - Pressure')
ax2.set_ylabel('Scale 2 - Temperature')

#set a legend for each data curve
lines = [p1, p2, p3, p4]
ax2.legend(lines, [l.get_label() for l in lines])
plt.show()


