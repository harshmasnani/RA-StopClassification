#1.verify files are in order in the list
#2.delete redunadnt entries and join
#

import pandas as pd
import re
from os import listdir
from os.path import isfile, join
import datetime

#key for sorted()
def csort(r):
    asPDdataframe=pd.read_csv(r)
    return datetime.datetime.strptime(asPDdataframe.at[0, 'Date and Time'],'%Y-%m-%d  %H:%M:%S')

path='/Users/Sunny/RA-StopClassification/Datasets/raw/vehicle_specific_folders/œÊA-D1317'
listFiles = [f for f in listdir(path) if isfile(join(path, f))]

#retain just the csvs. Folder might have some hidden files that are not visible in a gui application(finder, file explorer etc. .)
for x in listFiles:
    y=re.split('\.',x)
    if(y[-1]!='csv'):
        listFiles.remove(x)

#need full path. appending
for i in range(0,len(listFiles)):
    listFiles[i]=path + '/' + listFiles[i]

listFiles.sort() #easying the custom sort
listF=sorted(listFiles,key=csort)

##################################1 done################################

#Delete entries in top rows of files that cause Timestamp un-ordering
for i in range (0,len(listF)-1):
    f1 = pd.read_csv(listF[i])
    f2 = pd.read_csv(listF[i + 1])

    print(listF[i])

    a=f1.at[len(f1.index) - 1, 'Date and Time']

    l = []
    for j in range(0,len(f2.index)):
        if a >= f2.at[j, 'Date and Time']:
            l.append(j)
    f2.drop(l, inplace = False).to_csv(listF[i+1], index=False)


#assumes the above works and files are in order. Concatenating.
mainFrame=pd.DataFrame()

for i in listF:
    f=pd.read_csv(i)
    mainFrame = mainFrame.append(f, ignore_index=True)

mainFrame.Index=mainFrame.index
mainFrame.at[0,'Distance_geopy']=0
mainFrame.to_csv("/Users/Sunny/RA-StopClassification/Datasets/raw/concatenated/D1317.csv", index=False)

##################################2 done################################