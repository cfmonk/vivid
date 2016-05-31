#Pulls in all posts with a specified tag

import urllib, json, io, time, csv, re, sys

accesstoken = "3082655153.1fb234f.cef14254b92c4192bf10642eef7babbe"
clientId = "a778c35c48824baca6837071dba766df"

if(len(sys.argv) < 2):
	print "Usage: python getJson.py tag"
	quit()

#Set up parameters here
tag1 = sys.argv[1]
targetLat = 33.859077
targetLon = 151.207229
ourRange = 200000
numPages = 50000

url = "https://api.instagram.com/v1/tags/" + tag1 + "/media/recent?client_id=" + clientId
#?access_token=" + accesstoken
#?client_id=" + clientId"
print url

response = urllib.urlopen(url)

data = json.loads(response.read())


myTime = time.asctime(time.localtime(time.time()))

f = open('Output' + str(myTime) + '.csv', 'wb')	

writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

outputCount = 0

def withinRange (lat1, lon1, lat2, lon2, range):
	from math import cos, asin, sqrt
	p = 0.017453292519943295
	a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
	if((12742 * asin(sqrt(a))) < range):
		return True
	return False

for x in range(0, numPages):
	for item in data['data']:
		try:
			if (item['location'] != None and item['caption'] != None and item['images'] != None):
				lat = item['location']['latitude']
				lon = item['location']['longitude']
				niceCap = re.sub(r'[^\x00-\x7F]+',' ', item['caption']['text'])
			#Check whether the post is located within our defined radius
				writer.writerow([lat,lon,niceCap, item['images']['standard_resolution']['url'],item['images']['thumbnail']['url'], item['created_time'], item['user']['username'], item['likes']['count'], str(item['tags'])])
				outputCount += 1
				print "Found " + str(outputCount) + " results"
		except:

			print "Oops, something wrong with that entry"
			print item

	url = data['pagination']['next_url']

	while True:
		try:
			response = urllib.urlopen(url)
		except:
			print "URL Load Error, waiting 5 seconds before retrying"
			time.sleep(5)
			continue
		break

	data = json.loads(response.read())
	x += 1


f.write(unicode(csv))

print "Done with " + str(outputCount) + " results"



