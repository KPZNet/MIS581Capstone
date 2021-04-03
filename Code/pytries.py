import requests
import numpy as np
import statistics
import csv
import os
from datetime import timedelta, date
import datetime as dt
import calendar
import bart



try:
    r = bart.GetBARTLine("1")
    result = map(lambda x: x['station'], r)
except (Exception) as e:
    print(e)
finally:
    print("Completed")