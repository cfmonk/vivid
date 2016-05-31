import urllib, json, io, time, csv, re, sys, os

print len(sys.argv)
if(len(sys.argv) < 5):
	print "Usage: python geoLocate.py data.csv targetLat targetLon range"
	print "Melbourne: -37.8103854 144.8788034"
	print "Sydney: -33.8604459 151.1894196"
	quit()

dataFile = sys.argv[1]
targetLat = sys.argv[2]
targetLon = sys.argv[3]
ourRange = sys.argv[4]

outputCount = 0
inputCount = 0

inFile = open(dataFile, 'rb')
outFile = open(os.path.splitext(dataFile)[0] + "_GeoLocated.csv", 'wb');	

reader = csv.reader(inFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

row0 = reader.next()
writer.writerow(row0)

def withinRange (lat1, lon1, lat2, lon2, range):
	from math import cos, asin, sqrt
	p = 0.017453292519943295
	a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
	if((12742 * asin(sqrt(a))) < range):
		return True
	return False

for row in reader:
	inputCount += 1
	# try:
	if(withinRange(float(targetLat), float(targetLon), float(row[0]), float(row[1]), float(ourRange))):
		writer.writerow(row)
		outputCount += 1

	# except:
	# 	print "Oops"

print "Processed " + str(inputCount) + " rows with " + str(outputCount) + " results"

