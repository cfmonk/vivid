import urllib, json, io, time, csv, re, sys, datetime, os

if(len(sys.argv) < 2):
	print "Usage python addTime.py data.csv"
	
#Set up parameters here
dataFile = sys.argv[1]

inFile = open(dataFile, 'rb')
outFile = open(os.path.splitext(dataFile)[0] + "_WithDate.csv", 'wb');	

reader = csv.reader(inFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

outputCount = 0
inputCount = 0

row0 = reader.next()
row0.append('humanDate')
writer.writerow(row0)

for row in reader:
	inputCount += 1
	try:
		row.append(datetime.datetime.fromtimestamp(int(row[5])).strftime('%Y-%m-%d %H:%M:%S'))
		writer.writerow(row)
		outputCount += 1

	except:
		print "Oops"

print "Processed " + str(inputCount) + " rows with " + str(outputCount) + " results"