#### For files that have seperated decimals for co-ordinates
import pandas as pd
import numpy as np

df=pd.read_csv('/Users/Sunny/RA-StopClassification/Datasets/raw/vehicle_specific_folders/œÊA-29058/œÊA-29058-2017-6-15.csv')
df['Latitude']=df['Latitude'].astype(float)
df['Longitude']=df['Longitude'].astype(float)

##append 0s and bring to scale
latM=max(df['lat'])
longM=max(df['long'])

latM=len(str(latM))
longM=len(str(longM))


for i, v in enumerate(df['lat']):
   diff=abs(len(str(v)) - latM)
   if diff != 0:
       df.at[i, 'lat'] = df.at[i, 'lat'] * (10**diff)

for i, v in enumerate(df['long']):
   diff=abs(len(str(v)) - longM)
   if diff != 0:
       df.at[i, 'long'] = df.at[i, 'long'] * (10**diff)



#### Joining decimals
i=0
for L, l in zip(df['Latitude'], df['lat']):
    df.at[i,'Latitude'] = L + ( l / (10 ** len(str(l))) )
    i+=1

i=0
for L, l in zip(df['Longitude'], df['long']):
    df.at[i,'Longitude'] = L + ( l / (10 ** len(str(l))) )
    i+=1
df.to_csv('/Users/Sunny/RA-StopClassification/Datasets/raw/vehicle_specific_folders/œÊA-29058/œÊA-29058-2017-6-15.csv')