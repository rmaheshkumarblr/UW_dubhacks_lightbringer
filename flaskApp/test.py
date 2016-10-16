from clarifai import rest
from clarifai.rest import ClarifaiApp
import json


clientId='vccBzRmSwTHh1xi0L00DITt7JSVpGeskL7CtX1eX';
clientSecret='-Ao1JbwyuULVjzGp8i3N9a6EnpezvZIdoThWJ9Wr';
clarifaiApp = ClarifaiApp(clientId, clientSecret)

# get the general model
model = clarifaiApp.models.get("general-v1.3")
output = model.predict_by_url(url='https://samples.clarifai.com/metro-north.jpg')


concepts = output['outputs'][0]['data']['concepts']

threshold = 0

keywords = []

for concept in concepts:
	if concept['value'] > threshold:
		keywords.append( (concept['name'],concept['value']) ) 

keywords.sort(key=lambda tup: tup[1],reverse=True)

print keywords