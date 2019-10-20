#The STUFF

import pandas as pd
import re
import statistics
import datetime
import math

##writing correct indexes in the consolidated file
fileElementxx = '/Users/Sunny/RA/StopClassification/Data/raw/raw-concatenated/C1415.csv'
dfxx = pd.read_csv(fileElementxx)
dfxx.Index=dfxx.index
dfxx.to_csv('/Users/Sunny/RA/StopClassification/Data/raw/raw-concatenated/C1415.csv', index=False)


fileElement = '/Users/Sunny/RA/StopClassification/Data/raw/raw-concatenated/C1415.csv'
df = pd.read_csv(fileElement)

##some 0 values in Dist_geopy are missing. Filling NAs with 0
df.Distance_geopy=df.Distance_geopy.fillna(0)

#converting from pandas.Series to calculate time values
df['Date and Time'] = df['Date and Time'].astype('datetime64[s]')

#indexes in the consolidated file might be discrepant. dropping
del df['Index']

# calculates the index before i where speed was 0
def last0index(i):
    for j in range(i - 2, -1, -1):
        if df.at[j, 'Speed (km/h)'] == 0:
            return j


# calculates the index after i for which speed remains 0. The vehicle starts moving(non-zero speed after this index)
def next0index(i):
    for j in range(i + 1, len(df.index)):
        if df.at[j, 'Speed (km/h)'] != 0:
            return j - 1
        if j==len(df.index)-1:
            return j

# given StartRow-'S' and StopRow-'E' of a latitude, calculates average
def averageLat(S, E):
    total = 0
    n = (E - S) + 1
    for i in range(S, E + 1):
        total += df.at[i, 'Latitude']
    return total / n


# given StartRow-'S' and StopRow-'E' of a longitude, calculates average
def averageLong(S, E):
    total = 0
    n = (E - S) + 1
    for i in range(S, E + 1):
        total += df.at[i, 'Longitude']
    return total / n


x1 = []#list of avgSpeed*timeTravelled
x2 = []#list of dist
jumped =[] #list of stop index skipped by verifyStop

frame3=pd.DataFrame(columns=['StopID','VehicleID','StartRow','StopRow','StartTime','EndTime','Duration','Latitude','Longitude','Average Speed before stop','Distance from previous stop(in kms)','Time travelled before stop','Speed Variance'])
innerJack=0
n=1111111111111
a1=0
a2=0
timeThresh=0

def breakStops():
    global frame3
    global innerJack
    for i in frame.index:
        #print(i)
        if (frame.at[int(i),'Duration'] > 1440):
            n=math.ceil(frame.at[int(i),'Duration']/1440) #n=no of subsections of the stop.

            for x in range (0,n): #split stops>1day and append to frame3

                if innerJack == 99:
                    innerJack = 0
                    break
                timeThresh=datetime.datetime.strptime(str(df.at[int(frame.at[int(i),'StartRow'])-1,'Date and Time']),'%Y-%m-%d  %H:%M:%S') + ((x+1)*datetime.timedelta(seconds=86400))
                if(x==0):
                    a1=int(frame.at[int(i),'StartRow']) #start index
                    a2=int(frame.at[int(i),'StopRow'])

                for j in range(a1, a2+1):
                    if(datetime.datetime.strptime(str(df.at[j,'Date and Time']), '%Y-%m-%d  %H:%M:%S') > timeThresh):
                        framex = pd.DataFrame()
                        framex.at[0, 'StopID'] = 0
                        framex.at[0, 'VehicleID'] = name
                        framex.at[0, 'StartRow'] = a1
                        framex.at[0, 'StopRow'] = j - 1
                        framex.at[0, 'StartTime'] = df.at[a1, 'Date and Time']
                        framex.at[0, 'EndTime'] = df.at[j - 1, 'Date and Time']
                        framex.at[0, 'Latitude'] = averageLat(a1,j-1)
                        framex.at[0, 'Longitude'] = averageLong(a1,j-1)

                        if(x==0): #firstsubsection will have these details of the stop before that
                            framex.at[0, 'Average Speed before stop'] = frame.at[i, 'Average Speed before stop']
                            framex.at[0, 'Distance from previous stop(in kms)'] = frame.at[i, 'Distance from previous stop(in kms)']
                            framex.at[0, 'Time travelled before stop'] = frame.at[i, 'Time travelled before stop']
                            framex.at[0, 'Speed Variance'] = frame.at[i, 'Speed Variance']
                        else:
                            framex.at[0, 'Average Speed before stop'] = 0
                            framex.at[0, 'Distance from previous stop(in kms)'] = 0
                            framex.at[0, 'Time travelled before stop'] = 0
                            framex.at[0, 'Speed Variance'] = 0
                         # in datetime.timedelta format. Convert as necessary.
                        dur = datetime.datetime.strptime(str(df.at[j - 1, 'Date and Time']),'%Y-%m-%d  %H:%M:%S') - datetime.datetime.strptime(str(df.at[a1, 'Date and Time']), '%Y-%m-%d  %H:%M:%S')
                        # converting to minutes here
                        framex.at[0, 'Duration'] = (dur.days * 24 * 60) + (dur.seconds / 60)
                        frame3=frame3.append(framex,ignore_index=True)

                        #just a check to verify....(I forgot!, but if this statement prints, then something's wrong)
                        if(((j-1)-a1) < 0):
                            print(str(a1) + ' ' + str(j-1) + ' ' + str(i))


                        a1 = int(j)

                        g=datetime.datetime.strptime(str(df.at[j,'Date and Time']),'%Y-%m-%d  %H:%M:%S')-datetime.datetime.strptime(str(df.at[j-1,'Date and Time']),'%Y-%m-%d  %H:%M:%S')
                        if g.days>0:

                            framex=pd.DataFrame()
                            framex.at[0, 'StopID']=0
                            framex.at[0,'VehicleID'] = name
                            framex.at[0,'StartRow']=j
                            framex.at[0,'StopRow']= frame.at[i,'StopRow']
                            framex.at[0,'StartTime']= df.at[j,'Date and Time']
                            framex.at[0,'EndTime']=df.at[int(frame.at[i,'StopRow']),'Date and Time']
                            framex.at[0,'Latitude'] = averageLat(j,int(frame.at[i,'StopRow']))
                            framex.at[0,'Longitude'] = averageLong(j,int(frame.at[i,'StopRow']))
                            framex.at[0,'Average Speed before stop'] = 0
                            framex.at[0,'Distance from previous stop(in kms)'] = 0
                            framex.at[0,'Time travelled before stop'] = 0
                            framex.at[0,'Speed Variance'] = 0

                            dur=datetime.datetime.strptime(str(df.at[int(frame.at[i,'StopRow']),'Date and Time']),'%Y-%m-%d  %H:%M:%S')-datetime.datetime.strptime(str(df.at[j,'Date and Time']),'%Y-%m-%d  %H:%M:%S')
                            framex.at[0, 'Duration']=(dur.days*24*60)+(dur.seconds/60)
                            frame3=frame3.append(framex, ignore_index=True)

                            innerJack = 99

                        break

                    if j==a2:

                        framex=pd.DataFrame()
                        framex.at[0, 'StopID'] = 0
                        framex.at[0, 'VehicleID'] = name
                        framex.at[0, 'StartRow'] = a1
                        framex.at[0, 'StopRow'] = j
                        framex.at[0, 'StartTime'] = df.at[a1, 'Date and Time']
                        framex.at[0, 'EndTime'] = df.at[j, 'Date and Time']
                        framex.at[0, 'Latitude'] = averageLat(a1,j)
                        framex.at[0, 'Longitude'] = averageLong(a1,j)
                        framex.at[0, 'Average Speed before stop'] = 0
                        framex.at[0, 'Distance from previous stop(in kms)'] = 0
                        framex.at[0, 'Time travelled before stop'] = 0
                        framex.at[0, 'Speed Variance'] = 0

                        dur = datetime.datetime.strptime(str(df.at[j, 'Date and Time']),'%Y-%m-%d  %H:%M:%S') - datetime.datetime.strptime(str(df.at[a1, 'Date and Time']),'%Y-%m-%d  %H:%M:%S')
                        #converting to minutes here
                        framex.at[0, 'Duration'] = (dur.days*24*60)+(dur.seconds/60)
                        frame3=frame3.append(framex, ignore_index=True)
                        break
        else:

            framex=pd.DataFrame()
            framex.at[0, 'StopID'] = 0
            framex.at[0, 'VehicleID'] = name
            framex.at[0, 'StartRow'] = frame.at[i,'StartRow']
            framex.at[0, 'StopRow'] = frame.at[i,'StopRow']
            framex.at[0, 'StartTime'] = frame.at[i,'StartTime']
            framex.at[0, 'EndTime'] = frame.at[i,'EndTime']
            framex.at[0, 'Latitude'] = averageLat(int(frame.at[i,'StartRow']), int(frame.at[i,'StopRow']))
            framex.at[0, 'Longitude'] = averageLong(int(frame.at[i,'StartRow']), int(frame.at[i,'StopRow']))
            framex.at[0, 'Average Speed before stop'] = frame.at[i,'Average Speed before stop']
            framex.at[0, 'Distance from previous stop(in kms)'] = frame.at[i,'Distance from previous stop(in kms)']
            framex.at[0, 'Time travelled before stop'] = frame.at[i,'Time travelled before stop']
            framex.at[0, 'Speed Variance'] = frame.at[i,'Speed Variance']

            framex.at[0,'Duration']=frame.at[i,'Duration']
            frame3=frame3.append(framex, ignore_index=True)

def breakStopsAgain():
    global frame3
    global innerJack
    for i in frame.index:
        #print(i)
        if (frame.at[int(i),'Duration'] > 1440):
            n=math.ceil(frame.at[int(i),'Duration']/1440) #n=no of subsections of the stop.

            for x in range (0,n): #split stops>1day and append to frame3

                if innerJack == 99:
                    innerJack = 0
                    break
                timeThresh=datetime.datetime.strptime(str(df.at[int(frame.at[int(i),'StartRow']),'Date and Time']),'%Y-%m-%d  %H:%M:%S') + ((x+1)*datetime.timedelta(seconds=86400))
                if(x==0):
                    a1=int(frame.at[int(i),'StartRow']) #start index
                    a2=int(frame.at[int(i),'StopRow'])

                for j in range(a1, a2+1):
                    if(datetime.datetime.strptime(str(df.at[j,'Date and Time']), '%Y-%m-%d  %H:%M:%S') > timeThresh):
                        framex = pd.DataFrame()
                        framex.at[0, 'StopID'] = 0
                        framex.at[0, 'VehicleID'] = name
                        framex.at[0, 'StartRow'] = a1
                        framex.at[0, 'StopRow'] = j - 1
                        framex.at[0, 'StartTime'] = df.at[a1, 'Date and Time']
                        framex.at[0, 'EndTime'] = df.at[j - 1, 'Date and Time']
                        framex.at[0, 'Latitude'] = averageLat(a1,j-1)
                        framex.at[0, 'Longitude'] = averageLong(a1,j-1)

                        if(x==0): #firstsubsection will have these details of the stop before that
                            framex.at[0, 'Average Speed before stop'] = frame.at[i, 'Average Speed before stop']
                            framex.at[0, 'Distance from previous stop(in kms)'] = frame.at[i, 'Distance from previous stop(in kms)']
                            framex.at[0, 'Time travelled before stop'] = frame.at[i, 'Time travelled before stop']
                            framex.at[0, 'Speed Variance'] = frame.at[i, 'Speed Variance']
                        else:
                            framex.at[0, 'Average Speed before stop'] = 0
                            framex.at[0, 'Distance from previous stop(in kms)'] = 0
                            framex.at[0, 'Time travelled before stop'] = 0
                            framex.at[0, 'Speed Variance'] = 0
                         # in datetime.timedelta format. Convert as necessary.
                        dur = datetime.datetime.strptime(str(df.at[j - 1, 'Date and Time']),'%Y-%m-%d  %H:%M:%S') - datetime.datetime.strptime(str(df.at[a1, 'Date and Time']), '%Y-%m-%d  %H:%M:%S')
                        # converting to minutes here
                        framex.at[0, 'Duration'] = (dur.days * 24 * 60) + (dur.seconds / 60)
                        frame3=frame3.append(framex,ignore_index=True)

                        #just a check to verify....(I forgot!, but if this statement prints, then something's wrong)
                        if(((j-1)-a1) < 0):
                            print(str(a1) + ' ' + str(j-1) + ' ' + str(i))


                        a1 = int(j)

                        g=datetime.datetime.strptime(str(df.at[j,'Date and Time']),'%Y-%m-%d  %H:%M:%S')-datetime.datetime.strptime(str(df.at[j-1,'Date and Time']),'%Y-%m-%d  %H:%M:%S')
                        if g.days>0:

                            framex=pd.DataFrame()
                            framex.at[0, 'StopID']=0
                            framex.at[0,'VehicleID'] = name
                            framex.at[0,'StartRow']=j
                            framex.at[0,'StopRow']= frame.at[i,'StopRow']
                            framex.at[0,'StartTime']= df.at[j,'Date and Time']
                            framex.at[0,'EndTime']=df.at[int(frame.at[i,'StopRow']),'Date and Time']
                            framex.at[0,'Latitude'] = averageLat(j,int(frame.at[i,'StopRow']))
                            framex.at[0,'Longitude'] = averageLong(j,int(frame.at[i,'StopRow']))
                            framex.at[0,'Average Speed before stop'] = 0
                            framex.at[0,'Distance from previous stop(in kms)'] = 0
                            framex.at[0,'Time travelled before stop'] = 0
                            framex.at[0,'Speed Variance'] = 0

                            dur=datetime.datetime.strptime(str(df.at[int(frame.at[i,'StopRow']),'Date and Time']),'%Y-%m-%d  %H:%M:%S')-datetime.datetime.strptime(str(df.at[j,'Date and Time']),'%Y-%m-%d  %H:%M:%S')
                            framex.at[0, 'Duration']=(dur.days*24*60)+(dur.seconds/60)
                            frame3=frame3.append(framex, ignore_index=True)

                            innerJack = 99

                        break

                    if j==a2:

                        framex=pd.DataFrame()
                        framex.at[0, 'StopID'] = 0
                        framex.at[0, 'VehicleID'] = name
                        framex.at[0, 'StartRow'] = a1
                        framex.at[0, 'StopRow'] = j
                        framex.at[0, 'StartTime'] = df.at[a1, 'Date and Time']
                        framex.at[0, 'EndTime'] = df.at[j, 'Date and Time']
                        framex.at[0, 'Latitude'] = averageLat(a1,j)
                        framex.at[0, 'Longitude'] = averageLong(a1,j)
                        framex.at[0, 'Average Speed before stop'] = 0
                        framex.at[0, 'Distance from previous stop(in kms)'] = 0
                        framex.at[0, 'Time travelled before stop'] = 0
                        framex.at[0, 'Speed Variance'] = 0

                        dur = datetime.datetime.strptime(str(df.at[j, 'Date and Time']),'%Y-%m-%d  %H:%M:%S') - datetime.datetime.strptime(str(df.at[a1, 'Date and Time']),'%Y-%m-%d  %H:%M:%S')
                        #converting to minutes here
                        framex.at[0, 'Duration'] = (dur.days*24*60)+(dur.seconds/60)
                        frame3=frame3.append(framex, ignore_index=True)
                        break
        else:

            framex=pd.DataFrame()
            framex.at[0, 'StopID'] = 0
            framex.at[0, 'VehicleID'] = name
            framex.at[0, 'StartRow'] = frame.at[i,'StartRow']
            framex.at[0, 'StopRow'] = frame.at[i,'StopRow']
            framex.at[0, 'StartTime'] = frame.at[i,'StartTime']
            framex.at[0, 'EndTime'] = frame.at[i,'EndTime']
            framex.at[0, 'Latitude'] = averageLat(int(frame.at[i,'StartRow']),int(frame.at[i,'StopRow']))
            framex.at[0, 'Longitude'] = averageLong(int(frame.at[i,'StartRow']),int(frame.at[i,'StopRow']))
            framex.at[0, 'Average Speed before stop'] = frame.at[i,'Average Speed before stop']
            framex.at[0, 'Distance from previous stop(in kms)'] = frame.at[i,'Distance from previous stop(in kms)']
            framex.at[0, 'Time travelled before stop'] = frame.at[i,'Time travelled before stop']
            framex.at[0, 'Speed Variance'] = frame.at[i,'Speed Variance']

            framex.at[0,'Duration']=frame.at[i,'Duration']
            frame3=frame3.append(framex, ignore_index=True)


#helper method to verify stop by distance formula. returns 0 if stop verified successfully. a=index where potential stop was encountered.
def verifyStop(a):
    tolerance = 100  # in percentage.
    dist = 0
    speed = 0
    recordsEncSpeed = 0
    timeTravelled = (df.at[a, 'Date and Time'] - df.at[last0index(a) + 1, 'Date and Time']).total_seconds()

    for k in range(a, last0index(a) + 1, -1):
        dist += df.at[k, 'Distance_geopy']

    for j in range(a - 1, last0index(a), -1):
        speed += df.at[j, 'Speed (km/h)']
        recordsEncSpeed += 1
    avgSpeed = ((speed / recordsEncSpeed)) * (1000 / 3600)  # in meters per second

    avgS = speed / recordsEncSpeed
    x1.append(avgSpeed * timeTravelled)
    x2.append(dist)
    # catches values that are dist+%tolerance and dist-%tolerance
    if abs((avgSpeed * timeTravelled) - dist) <= ((tolerance / 100) * dist):
        return 0
    else:
        return -999

#helper method to verify stop by distance formula. returns 10 if stop verified successfully. a=index of following 0s. i=index of potential stop skipped by verifyStop()
def verifyInnerStop(a,i):
    tolerance = 100  # in percentage.
    dist = 0
    speed = 0
    recordsEncSpeed = 0
    timeTravelled= (df.at[a, 'Date and Time'] - df.at[last0index(i) + 1, 'Date and Time']).total_seconds()

    for k in range(a, last0index(i) + 1, -1):
        dist += df.at[k, 'Distance_geopy']

    for j in range(a - 1, last0index(i), -1):
        speed += df.at[j, 'Speed (km/h)']
        recordsEncSpeed += 1
    for l in range(a-1,i,-1):
        speed+=math.sqrt(statistics.variance(df.loc[last0index(i)+1:i-1,'Speed (km/h)']))
    avgSpeed = ((speed / recordsEncSpeed)) * (1000 / 3600)  # in meters per second
    avgS = speed / recordsEncSpeed
    # catches values that are dist+%tolerance and dist-%tolerance
    if abs((avgSpeed * timeTravelled) - dist) <= ((tolerance / 100) * dist):
        return 10
    else:
        return -888

# method returning average speed
def avgS(a):
    speed = 0
    recordsEncSpeed = 0

    for j in range(a - 1, last0index(a), -1):
        speed += df.at[j, 'Speed (km/h)']
        recordsEncSpeed += 1
    avgSpeed = (speed / recordsEncSpeed)
    return avgSpeed


# creating a new frame and appending to it
frame = pd.DataFrame()

# truncating the .csv extension of the consolidated file and assigning it to name, for VehicleId
name = fileElement
name = re.split('/', name)  # USE \ FOR WINDOWS / FOR LINUX
name = name[-1]
name = re.split(".csv", name)
name = name[0]


# StopId initially set to -1, incremented at every stop
stopNumber = -1

#writing a separate loop for detecting first stop if vehicle is stationary from the onset of the file
if df.at[0,'Speed (km/h)']==0:
    i=0
    #Verfification for first stop here
    stopNumber = stopNumber + 1
    frame.at[stopNumber, 'StopID'] = int(stopNumber)
    frame.at[stopNumber, 'VehicleID'] = name
    frame.at[stopNumber, 'StartRow'] = i
    frame.at[stopNumber, 'StopRow'] = next0index(i)
    frame.at[stopNumber, 'StartTime'] = df.at[i, 'Date and Time']
    frame.at[stopNumber, 'EndTime'] = df.at[next0index(i), 'Date and Time']
    frame.at[stopNumber, 'Duration'] = (frame.at[stopNumber, 'EndTime'] - frame.at[stopNumber, 'StartTime']) + (df.at[1,'Date and Time']-df.at[0,'Date and Time'])   # in Timedelta format. Convert as necessary
    frame.at[stopNumber, 'Latitude'] = averageLat(i, next0index(i))
    frame.at[stopNumber, 'Longitude'] = averageLong(i, next0index(i))
    frame.at[stopNumber, 'Average Speed before stop'] = 0
    frame.at[stopNumber, 'Distance from previous stop(in kms)'] = 0
    frame.at[stopNumber, 'Time travelled before stop'] = 0
    frame.at[stopNumber, 'Speed Variance'] = 0

for i in df.index:
    if i == 0:
        continue
    if df.at[i, 'Speed (km/h)'] == 0 and df.at[i - 1, 'Speed (km/h)'] != 0:
        # delegating to verifyStop(i) here
        code = verifyStop(i)
        if code==-999:
            jumped.append(i)
            for x in range(i+1, next0index(i)+1):
                innerCode=verifyInnerStop(x,i)
                if innerCode==10:
                    stopNumber = stopNumber + 1
                    frame.at[stopNumber, 'StopID'] = int(stopNumber)
                    frame.at[stopNumber, 'VehicleID'] = name
                    frame.at[stopNumber, 'StartRow'] = x
                    frame.at[stopNumber, 'StopRow'] = next0index(x)
                    frame.at[stopNumber, 'StartTime'] = df.at[x, 'Date and Time']
                    frame.at[stopNumber, 'EndTime'] = df.at[next0index(x), 'Date and Time']
                    frame.at[stopNumber, 'Duration'] = frame.at[stopNumber, 'EndTime'] - df.at[x - 1, 'Date and Time']
                    frame.at[stopNumber, 'Latitude'] = averageLat(x, next0index(x))
                    frame.at[stopNumber, 'Longitude'] = averageLong(x, next0index(x))
                    frame.at[stopNumber, 'Average Speed before stop'] = avgS(i)#upto i-the jumped stop
                    if ((last0index(i) + 1) - (i - 1)) == 0:#upto i-the jumped stop
                        frame.at[stopNumber, 'Speed Variance'] = df.at[i - 1, 'Speed (km/h)']
                    else:
                        frame.at[stopNumber, 'Speed Variance'] = statistics.variance(
                            df.loc[last0index(i) + 1:i - 1, 'Speed (km/h)'])
                break

        if code == 0:
            #start writing to frame if stop detected(code=0 returned by verifyStop)
            stopNumber = stopNumber + 1
            frame.at[stopNumber, 'StopID'] = int(stopNumber)
            frame.at[stopNumber, 'VehicleID'] = name
            frame.at[stopNumber, 'StartRow'] = i
            frame.at[stopNumber, 'StopRow'] = next0index(i)
            frame.at[stopNumber, 'StartTime'] = df.at[i, 'Date and Time']
            frame.at[stopNumber, 'EndTime'] = df.at[next0index(i), 'Date and Time']
            frame.at[stopNumber, 'Duration'] = frame.at[stopNumber, 'EndTime'] - df.at[i-1, 'Date and Time']  # in Timedelta format. Convert as necessary
            frame.at[stopNumber, 'Latitude'] = averageLat(i, next0index(i))
            frame.at[stopNumber, 'Longitude'] = averageLong(i, next0index(i))
            frame.at[stopNumber, 'Average Speed before stop'] = avgS(i)
            if((last0index(i)+1)-(i-1))==0:
                frame.at[stopNumber, 'Speed Variance'] = df.at[i-1,'Speed (km/h)']
            else:
                frame.at[stopNumber, 'Speed Variance'] = statistics.variance(df.loc[last0index(i)+1:i-1, 'Speed (km/h)'])
####Writing this loop to calculate distance between stops.
for i in frame.StopID:
    totalDist=0
    if i==0:
        continue
    a=int(frame.loc[i-1,'StopRow']) #index to start counting distance
    b=int(frame.loc[i,'StartRow'])
    for l in range(a,b+1):
        totalDist+=df.at[l,'Distance_geopy']
    frame.at[i,'Distance from previous stop(in kms)']=totalDist/1000
    frame.at[i,'Time travelled before stop']=df.at[b,'Date and Time']-df.at[a,'Date and Time']

##converting Duration Timedelta value to minutes
for i in frame.index:
    days=frame.Duration[i].days
    seconds=frame.Duration[i].seconds
    minutes=(days*24*60)+(seconds/60)
    frame.Duration[i]=minutes


##converting Time Travelled before stop from Timedelta to minutes
for i in frame.index:
    if i==0:
        continue
    days=frame.at[i,'Time travelled before stop'].days
    seconds=frame.at[i,'Time travelled before stop'].seconds
    minutes=(days*24*60)+(seconds/60)
    frame.at[i,'Time travelled before stop']=minutes

breakStops()

while not((frame3.Duration<1440).all()):
    frame=frame3
    frame3=pd.DataFrame()
    breakStopsAgain()

frame3.StopID=frame3.index


frame3.to_csv("/Users/Sunny/RA/StopClassification/Data/cleaned/Stops-C1415.csv", index=False)