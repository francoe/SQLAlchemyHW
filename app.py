from matplotlib import style
style.use('ggplot')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

year_ago = dt.datetime(2017,8,23) - dt.timedelta(weeks = 52)

precip_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
precip_dict = {}
precip_dict.update(precip_query)

station_query = session.query(Station.station).all()
station_list = []
station_dict = {}
station_dict['station'] = station_query
station_list.append(station_dict)

tobs_query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_ago).all()
tobs_dict = {}
tobs_dict.update(tobs_query)






from flask import Flask, jsonify

app = Flask(__name__)



@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome!"

@app.route("/api/v1.0/precipitation")
def precipitation():
	return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
	return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
	return jsonify(tobs_dict)

#@app.route("/api/v1.0/<start>")
#def start():
#	return xxxx

@app.route("/api/v1.0/<start>/<end>")
def calc_start_end_tobs(start, end):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    start_end_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    start_end_dict = {
        'Min' : start_end_query[0][0],
        'Average' : start_end_query[0][1],
        'Max' : start_end_query[0][2]
    }
    return start_end_dict
    #return jsonify(start_end_dict)



if __name__ == "__main__":
    app.run(debug=True)