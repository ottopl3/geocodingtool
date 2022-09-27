from os import path
import sys
import requests
import json
from requests.structures import CaseInsensitiveDict

def geoObject(id, jsonDump):
	if len(jsonDump['features'])>0:
		result = '{"resultId":"' + str(id) + '","query":"' + jsonDump['query']['text'] + '", "lat":"' + str(jsonDump['features'][0]['properties']['lat']) + '", "lon":"' + str(jsonDump['features'][0]['properties']['lon']) + '"}'
	else:
		result = '{"resultId":"' + str(id) + '","query":"' + jsonDump['query']['text'] + '", "lat":"na", "lon":"na"}'
	return result

API_KEY = "YOUR_API_KEY"
YOUR_COUNTRY_CODE = "YOUR_COUNTRY_CODE"

input_filename=	sys.argv[1]
data_file = open(input_filename,'r', encoding='utf-8')

dirname = path.dirname(input_filename)

data = json.load(data_file)
data_file.close()
i=0
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
f=open(dirname + "resultjson.json","w", encoding='utf-8')
f.write('[')
for address in data:
	print(address['addr_text'])
	i=i+1

	url = "https://api.geoapify.com/v1/geocode/search?text=" + address['addr_text'] + "&filter=countrycode:"+YOUR_COUNTRY_CODE+"&apiKey=" + API_KEY
	print(url)
	
	resp = requests.get(url, headers=headers)

	print(resp.status_code)
	geoResult = geoObject(address['id'], resp.json())
	print(geoResult)

	f.write(geoResult)
	if i<len(data):
		f.write(',')
f.write(']')
f.close()
	