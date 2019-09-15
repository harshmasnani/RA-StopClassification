####File purpose
####for "Distance traveled (km)"" feature to show distance values calculated by DistanceCalc()

import os
import glob
import pandas as pd
import math


# #swapping longitude and latitude here. Don't forget to delete pull request for StopExtraction.py if this file is executed!
# frame=frame.rename({"Latitude":"x","Longitude":"y"}, axis='columns') 
# frame=frame.rename({"x":"Longitude","y":"Latitude"}, axis='columns')

#return distance betweeen two co-ordinates(decimal digits) in meters
def distance(lat1, long1, lat2, long2):
	lat1=math.radians(lat1)
	long1=math.radians(long1)
	lat2=math.radians(lat2)
	long2=math.radians(long2)

	x=math.atan(math.sqrt((math.cos(lat2)*math.sin(long1-long2))**2+((math.cos(lat1)*math.sin(lat2))-
		(math.sin(lat1)*math.cos(lat2)*math.cos(long1-long2)))**2)/((math.sin(lat1)*math.sin(lat2))+
		(math.cos(lat1)*math.cos(lat2)*math.cos(long1-long2))))
	return x*6371009

path = r'/Users/Sunny/RA/StopClassification/Data/testDistanceTravelled'  
allFiles = glob.glob(os.path.join(path,"*.csv"))

for fileElement in allFiles:
	df = pd.read_csv(fileElement)
	
	####raw file has two columns for "Distance traveled (km)"; deleting one
	dist=df.ix[:, 'Distance traveled (km)']
	df=df.drop(columns=['Distance traveled (km)'])
	df['Distance traveled (km)']=dist

	####
	####
	####swapping longitude and latitude here. Don't forget to delete pull request for StopExtraction.py if this file is executed!
	df=df.rename({"Latitude":"x","Longitude":"y"}, axis='columns') 
	df=df.rename({"x":"Longitude","y":"Latitude"}, axis='columns')
	
	
	for i in df.index:
		if i==0:
			continue
		df.at[i, 'Distance traveled (km)']=distance(df.at[i,'Latitude'],df.at[i,'Longitude'],df.at[i-1,'Latitude'],df.at[i-1,'Longitude'])
	
	####idk why the compiler adds this weird column. Dropping it anyway!	
	df=df.drop(columns=['Distance traveled (km).1'])
	df.to_csv(fileElement)
