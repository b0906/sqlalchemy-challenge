from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Station = Base.classes.station
Measurement = Base.classes.measurement

@app.route("/")
def index():
    return """
    <h1>ALL ROUTES</h1>
    <p><a href='/api/v1.0/precipitation'>Percipitation</a></p>
    <p><a href='/api/v1.0/stations'>All Stations</a></p>
    <p><a href='/api/v1.0/tobs'>Temperatures from Most Active Station</a></p>
    <p><a href='/api/v1.0/2010-01-01'>Descriptive Stats for Jan 1 2010</a></p>
    <p><a href='/api/v1.0/2010-01-01/2011-01-01'>Descriptive Stats for Jan 1 2010 thru Jan 1 2011</a></p>
    """
@app.route("/test")
def test():
    return ":-)"

@app.route("/api/v1.0/precipitation")
def percipitation():
    session = Session(engine)
    first_date = dt.date(2017,8,23)-dt.timedelta(days=365)
    prcp_result=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= first_date).all()

    prcp_dict = {}

    for row in prcp_result:
        date = row[0]
        prcp = row[1]
        prcp_dict[date] = prcp

    session.close()

    return prcp_dict

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    all_stations = session.query(Station.station).all()

    stations_retun = []

    for s in all_stations:
        stations_retun.append(s[0])

    session.close()
    return jsonify(stations=stations_retun)

@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)
    first_date = dt.date(2017,8,23)-dt.timedelta(days=365)
    tobs_result = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281').filter(Measurement.date >= first_date).all()

    tobs_dict = {}

    for row in tobs_result:
        date = row[0]
        tobs = row[1]
        tobs_dict[date] = tobs

    session.close()
    return tobs_dict


@app.route("/add/<num1>/<num2>")
def add(num1, num2):
    sum = int(num1) + int(num2)
    return {"sum": sum, "num1": num1, "num2": num2}


@app.route("/api/v1.0/<start>")
def averages_with_start(start):
    start_dt = dt.datetime.strptime(start, "%Y-%m-%d")
    session = Session(engine)
    start_result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),
              func.avg(Measurement.tobs)).filter(Measurement.date > start_dt).all()

    start_dict = {}

    start_list = list(start_result[0])

    start_dict["start_date"] = start_dt
    start_dict["min"] = start_list[0]
    start_dict["max"] = start_list[1]
    start_dict["avg"] = start_list[2]

    session.close()
    return start_dict


@app.route("/api/v1.0/<start>/<end>")
def averages_with_end(start, end):
    start_dt = dt.datetime.strptime(start, "%Y-%m-%d")
    end_dt =  dt.datetime.strptime(end, "%Y-%m-%d")
    session = Session(engine)
    start_result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),
              func.avg(Measurement.tobs)).filter(Measurement.date > start_dt).filter(Measurement.date < end_dt).all()

    start_dict = {}

    start_list = list(start_result[0])

    start_dict["start_date"] = start_dt
    start_dict["end_date"] = end_dt
    start_dict["min"] = start_list[0]
    start_dict["max"] = start_list[1]
    start_dict["avg"] = start_list[2]

    session.close()
    return start_dict   

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)