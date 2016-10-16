from flask import Flask, render_template , jsonify ,request
from clarifai import rest
from clarifai.rest import ClarifaiApp


clientId='vccBzRmSwTHh1xi0L00DITt7JSVpGeskL7CtX1eX';
clientSecret='-Ao1JbwyuULVjzGp8i3N9a6EnpezvZIdoThWJ9Wr';
clarifaiApp = ClarifaiApp(clientId, clientSecret)

# get the general model
model = clarifaiApp.models.get("general-v1.3")
model.predict_by_url(url='https://samples.clarifai.com/metro-north.jpg')

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



if __name__ == '__main__':
  # app.run()
  app.run(debug=True, port=5000)