import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from sklearn import decomposition
from sklearn import preprocessing
import datetime
from scipy import stats
from sklearn import cluster
from math import sin, cos, sqrt, atan2, radians
#import keras as kr

matplotlib.style.use('fivethirtyeight')
matplotlib.rcParams['font.size'] = 12
matplotlib.rcParams['figure.figsize'] = (10,10)

taxiDB = pd.read_csv('./Dataset/train.csv')
taxiDB_Test = pd.read_csv('./Dataset/test.csv')

print("Total number of samples in training dataset: ", taxiDB.shape)
print("Total number of samples in test dataset: ", taxiDB_Test.shape)

print("Columns of training dataset:", taxiDB.columns)
print("Columns of training dataset:", taxiDB_Test.columns)

"""
print(taxiDB.head(1))
#Shuffle data
taxiDB = taxiDB.sample(frac=1)
print(taxiDB.head(1))
"""

#print(taxiDB.loc[:,'pickup_longitude'])
#print(taxiDB.loc[:,'pickup_latitude'])


#Utility functions...

def compute_distances(data):
    pickup_latitudes = data["pickup_latitude"]
    pickup_longitudes = data["pickup_longitude"]

    dropoff_latitudes = data["dropoff_latitude"]
    dropoff_longitudes = data["dropoff_longitude"]

    delta_lat = dropoff_latitudes - pickup_latitudes
    delta_long = dropoff_longitudes - pickup_longitudes
    delta_long = delta_long * np.cos(pickup_latitudes)

    return 110.25 * np.sqrt(np.square(delta_long) + np.square(delta_lat))

#print(compute_distances(taxiDB))

def datetimes_to_date_and_time(data):
    """
    Take dateTimes split them into date and time
        after that assign them into different columns...
    """
    pickup_datetimes = data.loc[:,'pickup_datetime']
    dropoff_datetimes = data.loc[:, 'dropoff_datetime']

    #Conversion operation...

    #bosluga gore ayir. Ilk kisim tarihi
    #ikinci kisim zamani verir. Zamani :, Tarihi -
    #gore ayir....

    pickup_Date =[]
    pickup_Time = []

    for dateTime in pickup_datetimes:
        date, time = dateTime.split(" ")
        pickup_Date.append(date)
        pickup_Time.append(time)

    dropoff_Date = []
    dropoff_Time = []

    for dateTime in pickup_datetimes:
        date, time = dateTime.split(" ")
        dropoff_Date.append(date)
        dropoff_Time.append(time)

    #Assign minutes as new column in

    data.loc[:, 'pickup_datetime_date'] = (pickup_Date)
    data.loc[:, 'pickup_datetime_time'] = (pickup_Time)

    data.loc[:, 'dropoff_datetime_date'] = (dropoff_Date)
    data.loc[:, 'dropoff_datetime_time'] = (dropoff_Time)

    return data

def datetimes_to_time_in_minutes(datetimes):
    """
    Take data and slice datetimes then
        convert time(ex. 17:26:48) to minute
    """
    minute_results  =[]
    for i in range(len(datetimes)):

        date_time = datetimes[i]
        time = date_time.split(" ")[1]

        times = time.split(":")

        minute_results.append(float(times[0]*60 + times[1]))

    return minute_results

def datetime_to_time_in_minutes(datetime):

    time = datetime.split(" ")[1]
    times = time.split(":")

    return float(times[0]*60 + times[1])

taxiDB = datetimes_to_date_and_time(taxiDB)
#print(taxiDB["pickup_datetime_time"])
#print(taxiDB["pickup_datetime"])


#zero mean, unit variance normalization
def zeroMean_UnitVariance_Normalization(column):
    """
    To specific column values, convert them into zero mean, unit variance...
    """
    #To calculate manually= (column - np.mean(column)) / np.std(column)
    return preprocessing.scale(column) #using sklearn preprocessing

#normalized = zeroMean_UnitVariance_Normalization(taxiDB["passenger_count"])
#print(normalized.mean())


#if date is weekday result = 1 else result=-1
def date_to_weekday(dates):
    """
    Take dates column then determine this date is weekday or not.
    """
    weekDays = []
    for i in range(len(dates)):
        date = dates[i]
        day, month, year = date.split("-")
        dayNo = datetime.date(year, month, day).weekday()

        if dayNo<5:
            weekDays.append(1)
        else:
            weekDays.append(-1)

    return weekDays

#calculate for given date which week of a year.
def date_week_of_year(dates):
    """
    Given date, calculate weekNumber. [0-51]
    """
    weekNo = []
    for i in range(len(dates)):
        date = dates[i]
        day, month, year = date.split("-")
        weekNo.append(datetime.date(year, month, day).isocalendar()[1])
    return weekNo

#calculate part of day: Morning,Afternoon, Evening, Night
def part_of_day(times):

    """"
        Morning - 1
        Afternoon - 2
        Evening - 3
        Night - 4
    """

    dayPart = []

    for i in range(len(times)):
        time  = times[i]

        if time > '21:00:00' or time < '04:00:00':
            dayPart.append(4) # Night
        elif time > '04:00:00' and time < '10:00:00':
            dayPart.append(1) # Morning
        elif time > '10:00:00' and time < '16:00:00':
            dayPart.append(2)
        else:
            dayPart.append(3)

    return dayPart

part_of_day(taxiDB['pickup_datetime_time'])

print("End of the Saturday!...06-08-2017")