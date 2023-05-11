# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
import numpy as np
import pandas as pd
import datetime as dt
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt



#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect = True)

# reflect the tables
print(Base.classes.keys())


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
#welcome page
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii climate app that you can use to research for your vacation<br/>"
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/startend"
     )

#precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    years_data = []
    years_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= previous_year).all()
    all_precip=list(np.ravel(years_data))
    return jsonify(all_precip)

#Stations route
@app.route("/api/v1.0/stations")
def stations():
    
    results=session.query(Station.station, Station.name, Station.longitude, Station.latitude, Station.elevation).all()
    all_stations=list(np.ravel(results))
    return jsonify(all_stations)

#Temperature (tobs) route
@app.route("/api/v1.0/tobs")
def tobs():
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   
    results1=session.query(Measurement.station, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= previous_year).all()
    all_tobs=list(np.ravel(results1))
    return jsonify(all_tobs)


# start and end date route
@app.route("/api/v1.0/startend")
def startend():
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    aggregate = session.query(func.avg(Measurement.tobs), func.min(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= previous_year).all()
    start_end=list(np.ravel(aggregate))
    return jsonify(start_end)







if __name__ == "__main__":
    app.run(debug=False)