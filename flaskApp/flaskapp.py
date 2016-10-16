from flask import Flask, render_template , jsonify ,request
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage


clientId='vccBzRmSwTHh1xi0L00DITt7JSVpGeskL7CtX1eX';
clientSecret='-Ao1JbwyuULVjzGp8i3N9a6EnpezvZIdoThWJ9Wr';
clarifaiApp = ClarifaiApp(clientId, clientSecret)

# get the general model
model = clarifaiApp.models.get("general-v1.3")

app = Flask(__name__)

# app.config['SERVER_NAME'] = 'AMAZONAWS.COM'
# app.config['SERVER_NAME'] = '127.0.0.1'


# @app.route('/')
# def index():
#   # return 'Hello from Flask!'
#   return render_template('index.html')

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/info")
def parse_info():
#output = model.predict_by_url(url='https://samples.clarifai.com/metro-north.jpg')

	image = ClImage(file_obj=open('static/uploads/colorado.png', 'rb'))
	output = model.predict([image])

	concepts = output['outputs'][0]['data']['concepts']

	threshold = 0

	keywords = []

	for concept in concepts:
		if concept['value'] > threshold:
			keywords.append( (concept['name'],concept['value']) ) 

	keywords.sort(key=lambda tup: tup[1],reverse=True)

	alexa_intput = ''

	for k in keywords:
		if alexa_intput == '':
			alexa_intput = alexa_intput + k[0]
		else:
			alexa_intput = alexa_intput + ' '+k[0]

	return alexa_intput
	
	




if __name__ == '__main__':
  # app.run()
  app.run(debug=True, port=5000)