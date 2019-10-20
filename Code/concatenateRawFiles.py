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
    return datetime.datetime.strptime(asPDdataframe.at[0,'Date and Time'],'%Y-%m-%d  %H:%M:%S')

path='/Users/Sunny/RA/StopClassification/Data/raw/湘A-C1415'
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

#assumes the above works and files are in order.
mainFrame=pd.DataFrame()

for i in range(0,len(listF)-2):
    if(i%2==0 or i==len(listF)-2):
        f1=pd.read_csv(listF[i])
        f2=pd.read_csv(listF[i+1])

        a=f1.at[len(f1.index)-1,'Date and Time']
        for j in range(0,len(f2.index)):
          if a >= f2.at[j,'Date and Time']:
              f2.drop(f2.index[j], inplace=True)#delete f2 row
              break

        mainFrame= mainFrame.append(f1,ignore_index=True)
        mainFrame= mainFrame.append(f2, ignore_index=True)

mainFrame.Index=mainFrame.index
mainFrame.at[0,'Distance_geopy']=0
mainFrame.to_csv("/Users/Sunny/RA/StopClassification/Data/raw/raw-concatenated/C1415.csv", index=False)

##################################2 done################################