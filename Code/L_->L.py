#Some files have labels "Longitude " and "Latitutde "; removing the whitespace here.
import pandas as pd
from os import listdir
from os.path import isfile, join
import re

path='/Users/Sunny/RA-StopClassification/Datasets/raw/vehicle_specific_folders/œÊA-D1317'
listFiles = [f for f in listdir(path) if isfile(join(path, f))]

for x in listFiles:
    y=re.split('\.',x)
    if(y[-1]!='csv'):
        listFiles.remove(x)

#need full path. appending
for i in range(0,len(listFiles)):
    listFiles[i]=path + '/' + listFiles[i]

for i in listFiles:
    print(i)
    df=pd.read_csv(i)
    df=df.rename({"Latitude ": "Latitude", "Longitude ": "Longitude"}, axis='columns')
    df.to_csv(i, index=False)