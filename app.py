# Step1: IMPORT DEPENDENCIES
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask
from flask import Flask, jsonify

# Step2: SET UP "HAWAII" DATABASE
# Acesss sqlite Database
engine = create_engine("sqlite:///hawaii.sqlite")
# Acesss & Query Database
Base = automap_base()
# Reflect our table
Base.prepare(engine, reflect=True)
# Save references to tables
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create session to link python
session = Session(engine)


# Step3a: CREATE OUR APP
# IMPORTANT: All code must go below Flask Instance
# Create Flask Instance
app = Flask(__name__)

# Step3: DEFINE ROUTES

# Step3a:
# Define/Create Welcome app/page route ***ROOT:HomePAge =  "/"


@app.route("/")
# Create a welcome() function
def welcome():
    # add the precipitation, stations, tobs, and temp routes
    return(
        ''' Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/station
    /api/v1.0/temp/start/end
    ''')
#!/usr/bin/env python
# export FLASK_APP = app.py
# flask run

# Step3b:
# Define/Create Precipitation app/page ROUTE
@app.route("api/v1.0/precipitation")
# Create a precipitation() function
def precipitation():
    # code that calculate date 1 yr ago from most recent date in the DB.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # write a query to get the date and precipitation for the previous year
    # NOTE .\ mean continue in next line
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    # create dictionary with date key & precipitation value.
    precip = {date: prcp for date, prcp in precipitation}
    # Use Jsonify() function to converts dict to a JSON structure format file
    return jsonify(precip)

# Step3c:
# Define/Create Station app/page ROUTE
@app.route("/api/v1.0/stations")
# Create Station fuction
def station():
    # create a query to get all of the stations in our database
    results = session.query(Station.station).all()
    # Use function np.ravel(), with results as parameter to unraveling results to a 1-dimensional array
    # Use list() fuction to convert unravelled result to a list
    stations = list(np.ravel(results))
    # jsonify the list to return JSON structure format file
    return jsonify(stations=stations)

# Step3d:
# Define/Create Monthly temp app/page ROUTE
@app.route("/api/v1.0/tobs")
# Create Station fuction
def temp_monthly():
    # code that calculate date 1 yr ago from most recent date in the DB.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Use Jsonify() function to converts dict to a JSON structure format filer
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Create Statistic Report Route to report on the minimum, average, and maximum temperatures.
# Must provide Start Date & End Date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# Define STATS function & add Start & end parmeter set both equal to none
def stats(start=None, end=None):
    # create query toselect min, av, max tempe from SQLite DB.
    sel = [func.min(Measurement.tobs), func.avg(
        Measurement.tobs), func.max(Measurement.tobs)]
    # add if-not nstatement to determine start/end dates
    if not end:
        # (*sel) is use to notate mutilple query results
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
