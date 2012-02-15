from __future__ import with_statement
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
from math import pow

# Configuration
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

def calculateTime(weight, type, time):
    boatWeight = 0.0
    if type == "8":
        boatWeight = 100.0
    elif type == "4":
        boatWeight = 60.0	
    return int(float(time) / pow(weight + boatWeight, 0.222))

@app.route('/')
def index():
    return render_template('tutorial.html')

@app.route('/calculate')
def calculate():
    weight = request.args.get('weight', 0, type=float)
    _type = request.args.get('type', "Unknown", type=str)
    _time = request.args.get('time', 0, type=float)
    return jsonify(time=calculateTime(weight, _type, _time))
    #return jsonify(time=_type)

if __name__ == '__main__':
    app.run()
	