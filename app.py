import os
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
import math
import time

# Configuration
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

def calculateTime(coxWeight, averageCrewWeight, type, time):   
    if type == "W8+" or "M8+":
        boatWeight = 100.0
        rowersWeight = 8 * averageCrewWeight
    elif type == "W4+" or "M4+":
        boatWeight = 60.0
        rowersWeight = 4 * averageCrewWeight

    if type == "W8+" or "W4+":
        minCoxWeight = 50.0
    elif type == "M8+" or "M4+":
        minCoxWeight = 55.0
        
    theoreticalMass = minCoxWeight + boatWeight + rowersWeight
    actualMass = coxWeight + boatWeight + rowersWeight
    return int(float(time) * (actualMass - theoreticalMass) / theoreticalMass / 6.0)

@app.route('/')
def index():
    return render_template('tutorial.html')

@app.route('/calculate')
def calculate():
    coxWeight = request.args.get('cox_weight', 75, type=float)
    averageCrewWeight = request.args.get('crew_weight', 75, type=float)
    type = request.args.get('type', "8+", type=str)
    _time = request.args.get('time', "10:00", type=str)
	# Attempt to parse time
    structTime = time.strptime(_time, "%M:%S")
    secs = structTime[4] * 60 + structTime[5]
    return jsonify(time=calculateTime(coxWeight, averageCrewWeight, type, secs))

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
	