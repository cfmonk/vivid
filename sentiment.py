import unirest, sys, csv, os

dataFile = sys.argv[1]

mashape = "Y0U52MuGUPmshDRjkPxwfEhAXolMp1D4pzKjsnGvUOcj9xdwtc"

inFile = open(dataFile, 'rb')
outFile = open(os.path.splitext(dataFile)[0] + "_Sentiment.csv", 'wb');

reader = csv.reader(inFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

outputCount = 0
inputCount = 0

row0 = reader.next()
row0.append('sentiment')
row0.append('neg')
row0.append('neutral')
row0.append('pos')
writer.writerow(row0)

for row in reader:
	inputCount += 1
	caption = row[1]
	print "Trying: " + caption
	try:
		response = unirest.post("https://japerk-text-processing.p.mashape.com/sentiment/",
		  headers={
		    "X-Mashape-Key": mahsape,
		    "Content-Type": "application/x-www-form-urlencoded",
		    "Accept": "application/json"
		  },
		  params={
		    "text": str(caption),
		    "lang": "english"
		  }
		)

		print response.body['label']
		print response.body['probability']['neg']
		print response.body['probability']['neutral']
		print response.body['probability']['pos']

		row.append(response.body['label'])
		row.append(response.body['probability']['neg'])
		row.append(response.body['probability']['neutral'])
		row.append(response.body['probability']['pos'])

		writer.writerow(row)

		outputCount += 1

	except:
		row.append("N/A")
		writer.writerow(row)		

print "Processed " + str(inputCount) + " rows with " + str(outputCount) + " results"
