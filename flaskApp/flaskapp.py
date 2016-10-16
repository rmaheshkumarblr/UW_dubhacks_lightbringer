from flask import Flask, render_template , jsonify ,request, Response
from errors.upload import InvalidUploadRequestException
from base64 import b64decode
import os
import json
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


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/info")
def parse_info():
    from rapidconnect import RapidConnect
    rapid = RapidConnect('lightbringer', '3dab63eb-4166-4315-81f5-f7c79164d31f');
    result = rapid.call('MicrosoftComputerVision', 'describeImage', {
        'image': 'http://ec2-52-41-77-155.us-west-2.compute.amazonaws.com:5000/static/uploads/image.png',
        'subscriptionKey': 'a04b26d206e2482083db92c60b3b818a',
        'maxCandidates': ''
    });
    return result
#output = model.predict_by_url(url='https://samples.clarifai.com/metro-north.jpg')

	# image = ClImage(file_obj=open('static/uploads/colorado.png', 'rb'))
	# output = model.predict([image])
    #
	# concepts = output['outputs'][0]['data']['concepts']
    #
	# threshold = 0
    #
	# keywords = []
    #
	# for concept in concepts:
	# 	if concept['value'] > threshold:
	# 		keywords.append( (concept['name'],concept['value']) )
    #
	# keywords.sort(key=lambda tup: tup[1],reverse=True)
    #
	# alexa_intput = ''
    #
	# for k in keywords:
	# 	if alexa_intput == '':
	# 		alexa_intput = alexa_intput + k[0]
	# 	else:
	# 		alexa_intput = alexa_intput + ' '+k[0]
    #
	# return alexa_intput


@app.route("/uploadimage", methods=['POST'])
def upload_image():
    image_data = request.form.get('imageData', '')
    if not image_data:
        raise InvalidUploadRequestException(message='Please pass base64 encoded data', status_code=500)

    try:
        decoded_image = b64decode(image_data)
    except TypeError as e:
        msg = json.dumps({
            'message': e
        })
        response = Response(msg, status=500, mimetype='application/json')
        return response

    # should have decoded base64 image
    # remove the existing image
    img_rel_path = 'static/uploads/image.jpg'
    if os.path.exists(img_rel_path):
        os.path.remove(img_rel_path)

    try:
        # create a new file with the image as content
        with open('static/uploads/image.png', 'w+') as image_file:
            image_file.write(decoded_image)
    except Exception as e:
        msg = json.dumps({
            'message': e
        })
        response = Response(msg, status=500, mimetype='application/json')
        return response

    # sure to be free of exceptions
    # return blank
    msg = {}
    return json.dumps(msg)

if __name__ == '__main__':
  # app.run()
  app.run(host='0.0.0.0', debug=True, port=5000)
