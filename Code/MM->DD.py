import pandas as pd


df=pd.read_csv('/Users/Sunny/RA-StopClassification/Datasets/raw/vehicle_specific_folders/œÊA-29058/œÊA-29058-2017-8-6.csv')

for i,v in enumerate(df['Date and Time']):
    temp=v[0:5] + v[8:10] + v[4:7] + v[10:]
    df.at[i,'Date and Time'] = temp

df.to_csv('/Users/Sunny/RA-StopClassification/Datasets/raw/vehicle_specific_folders/œÊA-29058/œÊA-29058-2017-8-6.csv', index=False)