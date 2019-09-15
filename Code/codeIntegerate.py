####Code to be integerated
import statistics

#verify stops
#file resolution i.e interval between timestamps for a file=time
time=
accuracy=90
if elementPrevious != 0 && 
						abs(frame.at[count,'Average Speed from Previous stop']*time-frame.at[count, 'Distance from previous stop'])
						<
						((100-accuracy)/100)*frame.at[count, 'Distance from previous stop']

#speed variance before stop

#assuming StartRow and StopRow pertain to an encountered Stop
S=frame.at[count-1, StopRow+1]
E=frame[count,StartRow-1]
statistics.variance(df.loc[S:E, 'Speed (km/h)'])