#duration between 10 mins and 180 labelled as 'D'-delivery stop and rest 'M'- maintenance

import pandas as pd
frame=pd.read_csv("/Users/Sunny/RA/StopClassification/Data/cleaned/Stops-C1415.csv")

for i in frame.index:
    if frame.at[i,'Duration'] >=10 and  frame.at[i,'Duration'] <= 180:
        frame.at[i,'Label']='D'
    else:
        frame.at[i,'Label']='M'

frame.to_csv("/Users/Sunny/Desktop/expirement-dummylabel/labelled-dummy-Stops-C1415.csv")