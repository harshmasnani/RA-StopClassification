import os
import glob
import pandas as pd
import datetime as dt
import tkinter as tk
from tkinter import filedialog

path = r'Your Path'  
allFiles = glob.glob(os.path.join(path,"*.csv"))

dfList = []
keyList = []

for fileElement in allFiles:

    df = pd.read_csv(fileElement)

    col_names = ['StopID', 'StartRow', 'StartTime', 'StopRow', 'EndTime', 'Latitude', 'Longitude','Distance from previous stop', 'Average Speed from Previous stop']
    frame = pd.DataFrame(columns = col_names)

    count = 0
    elementPrevious = -1
    distance1 = -1
    firstStop = -1
    lat = 0.0
    lon = 0.0
    n = 0
    speed = 0
    nForSpeed = 0

    df['Date and Time'] = df['Date and Time'].astype('datetime64[s]')

    for i in df.index:
        if df.at[i,'Speed (km/h)'] == 0:
            if elementPrevious != 0:    
                frame.at[count,'StopID'] = count + 1
                frame.at[count,'StartRow'] = i + 1
                frame.at[count,'StartTime'] = df.at[i,'Date and Time']
                lat +=df.at[i,'Latitude']
                lon +=df.at[i,'Longitude']
                if distance1 == -1:
                    distance1 = df.at[i,'Distance traveled (km)']
                else:
                    distance2 = df.at[i,'Distance traveled (km)']
                    frame.at[count,'Distance from previous stop'] = distance2 - distance1
                    distance1 = distance2
                if firstStop == -1:
                    firstStop = 0
                else:
                    frame.at[count,'Average Speed from Previous stop'] = speed/nForSpeed
                    speed = 0
                    nForSpeed = 0
                n += 1
            else:
                lat +=df.at[i,'Latitude']
                lon +=df.at[i,'Longitude']
                n += 1
            if i == len(df.index) - 1:
                frame.at[count,'Latitude'] = lat/n
                frame.at[count,'Longitude'] = lon/n
                frame.at[count,'StopRow'] = i + 1
                frame.at[count,'EndTime'] = df.at[i,'Date and Time']
        else:
            if elementPrevious == 0:
                frame.at[count,'StopRow'] = i
                frame.at[count,'EndTime'] = df.at[i,'Date and Time']
                frame.at[count,'Latitude'] = lat/n
                frame.at[count,'Longitude'] = lon/n
                count += 1
                lat = 0.0
                lon = 0.0
                n = 0
                speed += df.at[i,'Speed (km/h)']
                nForSpeed += 1
            else:
                if firstStop == 0:
                    speed += df.at[i,'Speed (km/h)']
                    nForSpeed += 1
        elementPrevious = df.at[i,'Speed (km/h)']

    frame.at[0,'Distance from previous stop'] = 0
    frame.at[0,'Average Speed from Previous stop'] = 0

    frame['stopDuration'] = (frame['EndTime'] - frame['StartTime']).dt.seconds
    frame['TimeDIffbtwStops'] = (((frame['StartTime']-frame['EndTime'].shift()).fillna(dt.timedelta(hours=00)))).dt.seconds
    
    dfList.append(frame)
    keyList.append('File:' + str(len(keyList) + 1))

frameFinal = pd.concat(dfList, keys=keyList)

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = 'raised')
canvas1.pack()

def exportCSV ():
    global df
    
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    frameFinal.to_csv (export_file_path, index = None, header=True)

saveAsButton_CSV = tk.Button(text='Export CSV', command=exportCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 150, window=saveAsButton_CSV)

root.mainloop()
