import os
import glob
import pandas as pd
import tkinter as tk
from tkinter import filedialog

path = r'Enter your path for files here'  
allFiles = glob.glob(os.path.join(path,"*.csv"))

dfList = [] #list of files cleaned.
keyList = [] #list for file identifiers.

for fileName in allFiles:

    df = pd.read_csv(fileName)
    df.index += 1

    df['Date and Time'] = df['Date and Time'].astype('datetime64[s]')
   
    #time elapsed calculation. O for first value.
    df['TimeDIff'] = (df['Date and Time']-df['Date and Time'].shift()).fillna(0)

    df = df.drop(columns=['Index', 'Date and Time', 'Distance traveled (km).1', 'Status', 'Position'])

    #distance elapsed and type conversion.
    df['DistanceDiff'] = df['Distance traveled (km)'].diff().fillna(df['Distance traveled (km)'])
    df['DistanceDiff'] = df['DistanceDiff'].astype(int)

    dfList.append(df)
    keyList.append('F' + str(len(keyList) + 1))

#concat all dfs in dfList in one single 'frame' by pandas.
frame = pd.concat(dfList, keys=keyList, names = ['File Number', 'Index'])

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = 'raised')
canvas1.pack()

def exportCSV():
    global df
    
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    frame.to_csv(export_file_path, index = None, header=True)

saveAsButton_CSV = tk.Button(text='Export CSV', command=exportCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 150, window=saveAsButton_CSV)

root.mainloop()
