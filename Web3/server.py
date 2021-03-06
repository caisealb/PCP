from flask import Flask, request, render_template

app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

@app.route('/speedometer')
def speedometer():
    return render_template('speedometer.html')

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/Workout')
def Workout():
    return render_template('Workout.html')

@app.route('/summary')
def test5():
    return render_template('summary.html')

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
