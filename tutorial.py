import os
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
import math

# Configuration
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

def calculateTime(weight, type, time):
    boatWeight = 0.0
    if type == "8+":
        boatWeight = 100.0
        rowersWeight = 8 * 80.0
    elif type == "4+":
        boatWeight = 60.0
        rowersWeight = 4 * 80.0		
    theoreticalMass = 55.0 + boatWeight
    actualMass = weight + boatWeight
    return int(float(time) * (actualMass - theoreticalMass) / theoreticalMass)

@app.route('/')
def index():
    return render_template('tutorial.html')

@app.route('/calculate')
def calculate():
    weight = request.args.get('weight', 55, type=float)
    _type = request.args.get('type', "8+", type=str)
    _time = request.args.get('time', 360, type=float)
    return jsonify(time=calculateTime(weight, _type, _time))

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
	