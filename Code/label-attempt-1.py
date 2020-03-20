import pandas as pd
import datetime
import os

frame=pd.read_csv("/Users/Sunny/RA/StopClassification/Data/cleaned/Stops-C1415.csv")
delframe=pd.read_csv("/Users/Sunny/RA/StopClassification/Data/raw/湘A-C1415/tracking-deliveries/deliveries-C1415-harsh.csv")
jack=-999

##deleting previous instances of labelled-Stops-C1415.csv

os.remove("/Users/Sunny/RA/StopClassification/Data/cleaned/labelled-Stops-C1415.csv")

##Marking Stops for 'Arrival at store' as 'A' ; frame.loc[frame['Label']=='A']
for i in delframe.index:
    l=[]
    l1=[]
    x=datetime.datetime.strptime(delframe.at[i,"Arrival Time at Store"],'%Y-%m-%d  %H:%M')
    for j in frame.index:
        y=datetime.datetime.strptime(frame.at[j, 'StartTime'], '%Y-%m-%d  %H:%M:%S')
        if y > x and y <= x+datetime.timedelta(seconds=600):
            l.append(j)
        if y > x+datetime.timedelta(seconds=600):
            break

    for k in range(0,len(l)):
        l1.append(frame.at[l[k],'Duration'])
        if len(l1)!=0:
            frame.at[l[l1.index(max(l1))],'Label']='A'

##Marking Stops for 'Departure time Warehouse' as 'DW' ; frame.loc[frame['Label']=='DW']
for i in delframe.index:
    l=[]
    l1=[]
    x=datetime.datetime.strptime(delframe.at[i,"Departure time Warehouse"],'%Y-%m-%d  %H:%M')
    for j in frame.index:
        y=datetime.datetime.strptime(frame.at[j, 'EndTime'], '%Y-%m-%d  %H:%M:%S')
        if y > x and y <= x+datetime.timedelta(seconds=900):
            l.append(j)
        if y > x+datetime.timedelta(seconds=900):
            break

    for k in range(0,len(l)):
        l1.append(frame.at[l[k],'Duration'])
        if len(l1)!=0:
            frame.at[l[l1.index(max(l1))],'Label']='DW'

##Marking Stops for 'Time returned to the warehouse' as 'RW'


frame.to_csv("/Users/Sunny/RA/StopClassification/Data/cleaned/labelled-Stops-C1415.csv")