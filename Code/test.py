import pandas as pd
df=pd.read_csv('/Users/Sunny/RA-StopClassification/Datasets/raw/concatenated/A3570.csv')
df.drop(list(range(7)),  inplace=False).to_csv('/Users/Sunny/RA-StopClassification/Datasets/raw/concatenated/A3570.csv', index=False)