from flask import Flask, request, render_template

app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

@app.route('/test')
def test():
    return render_template('test.html')

    @app.route('/speed')
    def speed():
        return render_template('speed.html')

@app.route('/barchart')
def barchart():
    return render_template('moving_barChart.html')

@app.route('/gauge')
def gauge():
    return render_template('gauge.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
