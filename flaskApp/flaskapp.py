from flask import Flask, render_template , jsonify ,request
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