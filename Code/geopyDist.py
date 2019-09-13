from geopy.distance import great_circle
from geopy.distance import vincenty

p1 = (31.8300167,35.0662833) # (lat, lon) - https://goo.gl/maps/TQwDd
p2 = (31.8300000,35.0708167) # (lat, lon) - https://goo.gl/maps/lHrrg
vincenty(p1, p2).meters
429.16765838976664
great_circle(p3, p4).meters
428.4088367903001