#!!!!!! Warning- this code modifies all file present in the 'path' variable below. Please copy and retain a copy elsewhere if needed.

####File purpose
####for "Distance traveled (km)"" feature to show distance values calculated by DistanceCalc() and geopy

import os
import glob
import pandas as pd
import math
from geopy.distance import great_circle


# return distance betweeen two co-ordinates(decimal digits) in meters
def distance(lat1, long1, lat2, long2):
    lat1 = math.radians(lat1)
    long1 = math.radians(long1)
    lat2 = math.radians(lat2)
    long2 = math.radians(long2)
    delta = abs(long1 - long2)

    x = math.atan(math.sqrt((math.cos(lat2) * math.sin(delta)) ** 2 + ((math.cos(lat1) * math.sin(lat2)) -
                                                                       (math.sin(lat1) * math.cos(lat2) * math.cos(
                                                                           delta))) ** 2) / (
                              (math.sin(lat1) * math.sin(lat2)) +
                              (math.cos(lat1) * math.cos(lat2) * math.cos(delta))))
    return x * 6371009.0


# return distance using geopy
def distance_great_cirlce(lat1, long1, lat2, long2):
    return great_circle((lat1, long1), (lat2, long2)).meters


path = r'/Users/Sunny/RA-StopClassification/Datasets/raw/vehicle_specific_folders/œÊA-D1317'
allFiles = glob.glob(os.path.join(path, "*.csv"))

for fileElement in allFiles:
    print(fileElement)
    df = pd.read_csv(fileElement)

    ####raw file has two columns for "Distance traveled (km)"; deleting one
    dist = df.ix[:, 'Distance traveled (km)']
    df = df.drop(columns=['Distance traveled (km)'])
    df['Distance traveled (km)'] = dist

    ####
    ####
    ####
    if ( any( df['Latitude'] > 90) or any(df['Latitude'] < -90) ):
        df = df.rename({"Latitude": "x", "Longitude": "y"}, axis='columns')
        df = df.rename({"x": "Longitude", "y": "Latitude"}, axis='columns')

    # overwrite 'Distance traveled (km)' with distance calculated in meters by distance(lat1, long1, lat2, long2)
    # for i in df.index:
    #     if i == 0:
    #         continue
    #     df.at[i, 'Distance traveled (km)'] = distance(df.at[i, 'Latitude'], df.at[i, 'Longitude'],   \
    #                                                 df.at[i - 1, 'Latitude'], df.at[i - 1, 'Longitude'])
    #
    # adding column 'Distance_geopy' with distance calulated in meters by distance_great_cirlce(lat1, long1, lat2, long2)
    for i in df.index:
        if type(i) != int:
            print(fileElement)
        elif i == 0:
            continue
        df.at[i, 'Distance_geopy'] = distance_great_cirlce(df.at[i, 'Latitude'], df.at[i, 'Longitude'], df.at[i - 1, 'Latitude'], df.at[i - 1, 'Longitude'])

    ####idk why the compiler adds this weird column. Dropping it anyway!
    # df = df.drop(columns=['Distance traveled (km).1'])

    ### converting to hh:mm:ss
    df['Date and Time'] = pd.to_datetime(df['Date and Time'])
    df['Date and Time'] = df['Date and Time'].apply(lambda x: str(x))

    df.to_csv(fileElement)