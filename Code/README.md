Run in the following order

1.distanceTravelled.py-calculates greatest circle distance and does intermediate cleaning of files in a particular folder(assuming one folder per vehicle) 

2.concatenateRawfiles.py-makes a single file for a single vehicle preserving order of timestamps and taking care of redundant entries.

3.verifyTimestamps.py-verifies joined file is in order

4.StopExtraction.py-extracts stops with controlled tolerance.

Note- all time values are in decimal minutes, speed km/hr and distance values in kms in the resultant Stops file. 
