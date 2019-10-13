import pandas as pd
import datetime
import math

frame3=pd.DataFrame(columns=['StopID','VehicleID','StartRow','StopRow','StartTime','EndTime','Duration','Latitude','Longitude','Average Speed before stop','Distance from previous stop(in kms)','Time travelled before stop','Speed Variance'])
df=pd.read_csv('/Users/Sunny/RA/StopClassification/Data/raw/raw-concatenated/C1415.csv')
frame=pd.read_csv("/Users/Sunny/RA/StopClassification/Data/cleaned/Stops-C1415.csv")
innerJack=0
n=1111111111111
a1=0
a2=0
timeThresh=0

def breakStops():
    global frame3
    global innerJack
    for i in frame.index:
        print(i)
        if (frame.at[int(i),'Duration'] > 1440):
            n=math.ceil(frame.at[int(i),'Duration']/1440) #n=no of subsections of the stop.

            for x in range (0,n): #split stops>1day and append to frame3

                if innerJack == 99:
                    innerJack = 0
                    break
                timeThresh=datetime.datetime.strptime(df.at[int(frame.at[int(i),'StartRow'])-1,'Date and Time'],'%Y-%m-%d  %H:%M:%S') + ((x+1)*datetime.timedelta(seconds=86400))
                if(x==0):
                    a1=int(frame.at[int(i),'StartRow']) #start index
                    a2=int(frame.at[int(i),'StopRow'])

                for j in range(a1, a2+1):
                    if(datetime.datetime.strptime(df.at[j,'Date and Time'], '%Y-%m-%d  %H:%M:%S') > timeThresh):
                        framex = pd.DataFrame()
                        framex.at[0, 'StopID'] = 0
                        framex.at[0, 'VehicleID'] = name
                        framex.at[0, 'StartRow'] = a1
                        framex.at[0, 'StopRow'] = j - 1
                        framex.at[0, 'StartTime'] = df.at[a1, 'Date and Time']
                        framex.at[0, 'EndTime'] = df.at[j - 1, 'Date and Time']
                        #framex.at[0, 'Latitude'] = averageLat(a1,j-1)
                        #framex.at[0, 'Longitude'] = averageLong(a1,j-1)

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
                        dur = datetime.datetime.strptime(df.at[j - 1, 'Date and Time'],'%Y-%m-%d  %H:%M:%S') - datetime.datetime.strptime(df.at[a1, 'Date and Time'], '%Y-%m-%d  %H:%M:%S')
                        # converting to minutes here
                        framex.at[0, 'Duration'] = (dur.days * 24 * 60) + (dur.seconds / 60)
                        frame3=frame3.append(framex,ignore_index=True)

                        #just a check to verify....(I forgot!, but if this statement prints, then something's wrong)
                        if(((j-1)-a1) < 0):
                            print(str(a1) + ' ' + str(j-1) + ' ' + str(i))


                        a1 = int(j)

                        g=datetime.datetime.strptime(df.at[j,'Date and Time'],'%Y-%m-%d  %H:%M:%S')-datetime.datetime.strptime(df.at[j-1,'Date and Time'],'%Y-%m-%d  %H:%M:%S')
                        if g.days>0:

                            framex=pd.DataFrame()
                            framex.at[0, 'StopID']=0
                            framex.at[0,'VehicleID'] = name
                            framex.at[0,'StartRow']=j
                            framex.at[0,'StopRow']= frame.at[i,'StopRow']
                            framex.at[0,'StartTime']= df.at[j,'Date and Time']
                            framex.at[0,'EndTime']=df.at[int(frame.at[i,'StopRow']),'Date and Time']
                            #framex.at[0,'Latitude'] = averageLat(a1,j-1)
                            #framex.at[0,'Longitude'] = averageLong(a1,j-1)
                            framex.at[0,'Average Speed before stop'] = 0
                            framex.at[0,'Distance from previous stop(in kms)'] = 0
                            framex.at[0,'Time travelled before stop'] = 0
                            framex.at[0,'Speed Variance'] = 0

                            dur=datetime.datetime.strptime(df.at[int(frame.at[i,'StopRow']),'Date and Time'],'%Y-%m-%d  %H:%M:%S')-datetime.datetime.strptime(df.at[j,'Date and Time'],'%Y-%m-%d  %H:%M:%S')
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
                        # frame1.at[int(i) + x, 'Latitude'] = averageLat(a1,j)
                        # frame1.at[int(i) + x, 'Longitude'] = averageLong(a1,j)
                        framex.at[0, 'Average Speed before stop'] = 0
                        framex.at[0, 'Distance from previous stop(in kms)'] = 0
                        framex.at[0, 'Time travelled before stop'] = 0
                        framex.at[0, 'Speed Variance'] = 0

                        dur = datetime.datetime.strptime(df.at[j, 'Date and Time'],'%Y-%m-%d  %H:%M:%S') - datetime.datetime.strptime(df.at[a1, 'Date and Time'],'%Y-%m-%d  %H:%M:%S')
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
            # frame1.at[int(i) + x, 'Latitude'] = averageLat(a1,j)
            # frame1.at[int(i) + x, 'Longitude'] = averageLong(a1,j)
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
        print(i)
        if (frame.at[int(i),'Duration'] > 1440):
            n=math.ceil(frame.at[int(i),'Duration']/1440) #n=no of subsections of the stop.

            for x in range (0,n): #split stops>1day and append to frame3

                if innerJack == 99:
                    innerJack = 0
                    break
                timeThresh=datetime.datetime.strptime(df.at[int(frame.at[int(i),'StartRow']),'Date and Time'],'%Y-%m-%d  %H:%M:%S') + ((x+1)*datetime.timedelta(seconds=86400))
                if(x==0):
                    a1=int(frame.at[int(i),'StartRow']) #start index
                    a2=int(frame.at[int(i),'StopRow'])

                for j in range(a1, a2+1):
                    if(datetime.datetime.strptime(df.at[j,'Date and Time'], '%Y-%m-%d  %H:%M:%S') > timeThresh):
                        framex = pd.DataFrame()
                        framex.at[0, 'StopID'] = 0
                        framex.at[0, 'VehicleID'] = name
                        framex.at[0, 'StartRow'] = a1
                        framex.at[0, 'StopRow'] = j - 1
                        framex.at[0, 'StartTime'] = df.at[a1, 'Date and Time']
                        framex.at[0, 'EndTime'] = df.at[j - 1, 'Date and Time']
                        #framex.at[0, 'Latitude'] = averageLat(a1,j-1)
                        #framex.at[0, 'Longitude'] = averageLong(a1,j-1)

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
                        dur = datetime.datetime.strptime(df.at[j - 1, 'Date and Time'],'%Y-%m-%d  %H:%M:%S') - datetime.datetime.strptime(df.at[a1, 'Date and Time'], '%Y-%m-%d  %H:%M:%S')
                        # converting to minutes here
                        framex.at[0, 'Duration'] = (dur.days * 24 * 60) + (dur.seconds / 60)
                        frame3=frame3.append(framex,ignore_index=True)

                        #just a check to verify....(I forgot!, but if this statement prints, then something's wrong)
                        if(((j-1)-a1) < 0):
                            print(str(a1) + ' ' + str(j-1) + ' ' + str(i))


                        a1 = int(j)

                        g=datetime.datetime.strptime(df.at[j,'Date and Time'],'%Y-%m-%d  %H:%M:%S')-datetime.datetime.strptime(df.at[j-1,'Date and Time'],'%Y-%m-%d  %H:%M:%S')
                        if g.days>0:

                            framex=pd.DataFrame()
                            framex.at[0, 'StopID']=0
                            framex.at[0,'VehicleID'] = name
                            framex.at[0,'StartRow']=j
                            framex.at[0,'StopRow']= frame.at[i,'StopRow']
                            framex.at[0,'StartTime']= df.at[j,'Date and Time']
                            framex.at[0,'EndTime']=df.at[int(frame.at[i,'StopRow']),'Date and Time']
                            #framex.at[0,'Latitude'] = averageLat(a1,j-1)
                            #framex.at[0,'Longitude'] = averageLong(a1,j-1)
                            framex.at[0,'Average Speed before stop'] = 0
                            framex.at[0,'Distance from previous stop(in kms)'] = 0
                            framex.at[0,'Time travelled before stop'] = 0
                            framex.at[0,'Speed Variance'] = 0

                            dur=datetime.datetime.strptime(df.at[int(frame.at[i,'StopRow']),'Date and Time'],'%Y-%m-%d  %H:%M:%S')-datetime.datetime.strptime(df.at[j,'Date and Time'],'%Y-%m-%d  %H:%M:%S')
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
                        # frame1.at[int(i) + x, 'Latitude'] = averageLat(a1,j)
                        # frame1.at[int(i) + x, 'Longitude'] = averageLong(a1,j)
                        framex.at[0, 'Average Speed before stop'] = 0
                        framex.at[0, 'Distance from previous stop(in kms)'] = 0
                        framex.at[0, 'Time travelled before stop'] = 0
                        framex.at[0, 'Speed Variance'] = 0

                        dur = datetime.datetime.strptime(df.at[j, 'Date and Time'],'%Y-%m-%d  %H:%M:%S') - datetime.datetime.strptime(df.at[a1, 'Date and Time'],'%Y-%m-%d  %H:%M:%S')
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
            # frame1.at[int(i) + x, 'Latitude'] = averageLat(a1,j)
            # frame1.at[int(i) + x, 'Longitude'] = averageLong(a1,j)
            framex.at[0, 'Average Speed before stop'] = frame.at[i,'Average Speed before stop']
            framex.at[0, 'Distance from previous stop(in kms)'] = frame.at[i,'Distance from previous stop(in kms)']
            framex.at[0, 'Time travelled before stop'] = frame.at[i,'Time travelled before stop']
            framex.at[0, 'Speed Variance'] = frame.at[i,'Speed Variance']

            framex.at[0,'Duration']=frame.at[i,'Duration']
            frame3=frame3.append(framex, ignore_index=True)

breakStops()

while not((frame3.Duration<1440).all()):
    frame=frame3
    frame3=pd.DataFrame()
    breakStopsAgain()

frame3.StopID=frame3.index
