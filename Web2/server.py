from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/distance')
def distance():
    return render_template('distance.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
