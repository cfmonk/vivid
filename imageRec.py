import unirest, sys, csv, os

dataFile = sys.argv[1]

#Mashape key www.mashape.com
mashape = "Y0U52MuGUPmshDRjkPxwfEhAXolMp1D4pzKjsnGvUOcj9xdwtc"

inFile = open(dataFile, 'rb')
outFile = open(os.path.splitext(dataFile)[0] + "_Recognised.csv", 'wb');

reader = csv.reader(inFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

outputCount = 0
inputCount = 0

row0 = reader.next()
row0.append('desciption')
writer.writerow(row0)

for row in reader:
	inputCount += 1
	url = row[1]
	print "Trying: " + url
	try:
		response = unirest.post("https://camfind.p.mashape.com/image_requests",
  headers={
    "X-Mashape-Key": mashape,
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"
  },
  params={
    "focus[x]": "480",
    "focus[y]": "640",
    "image_request[altitude]": "27.912109375",
    "image_request[language]": "en",
    "image_request[latitude]": "35.8714220766008",
    "image_request[locale]": "en_US",
    "image_request[longitude]": "14.3583203002251",
    "image_request[remote_image_url]": url
  }
)

		token = response.body['token']
		response = unirest.get("https://camfind.p.mashape.com/image_responses/" + token,
			  headers={
			    "X-Mashape-Key": mashape,
			    "Accept": "application/json"
			  }
			)

		status = response.body['status']
		print status

		# These code snippets use an open-source library. http://unirest.io/python
		i = 0
		while status != "completed":
			i += 1
			response = unirest.get("https://camfind.p.mashape.com/image_responses/" + token,
			  headers={
			    "X-Mashape-Key": mashape,
			    "Accept": "application/json"
			  }
			)
			status = response.body['status']
			print status

			#Sometimes CamFind returns skipped or timeout which means it won't ever return complete, breaking out here will force an error and record N/A
			if status == "skipped" or status=="timeout":
				break
		
		print response.body['name']

		row.append(response.body['name'])
		writer.writerow(row)

		outputCount += 1

	except:
		row.append("N/A")
		writer.writerow(row)		

print "Processed " + str(inputCount) + " rows with " + str(outputCount) + " results"
