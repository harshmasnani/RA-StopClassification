##VERIFYING timestamps in consolidated file are in order
import pandas as pd

df=pd.read_csv('/Users/Sunny/RA-StopClassification/Datasets/raw/concatenated/D1317.csv')
df.Index=df.index

for i in range(1,len(df.index)):
    if (df.at[i-1,'Date and Time'] > df.at[i,'Date and Time']):
        print('Time stamping is unordered. Check ' + str(i-1) + ',' + str(i))
        break
    if(i==len(df.index)-1):
        print('File is rightly ordered')

##Write this in console when File is rightly ordered.
#df.to_csv("/Users/Sunny/RA/StopClassification/Data/raw/raw-concatenated/C1415.csv", index=False)