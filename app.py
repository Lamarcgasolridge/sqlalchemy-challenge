import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template

#db engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)

#Reflect db into classes
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

#create session
session = Session(engine)

app = Flask(__name__)


app.config["JSON_SORT_KEYS"] = False

#Homepage
@app.route("/")
def index():
    return (
        f"~~~~~~~~~~~~~~~~~~~~~~<br/>"
        f"Available Routes:<br/>"
        f"~~~~~~~~~~~~~~~~~~~~~~<br/>"
        f"Last year's precipitation: /api/v1.0/precipitation<br/>"
        f"List of all stations: /api/v1.0/stations<br/>"
        f"Temperature observations by date: /api/v1.0/tobs<br/>"
        f"Temp stats from a given date to now: /api/v1.0/2012-05-15<br/>"
        f"Temp stats in a specified date range: /api/v1.0/2015-04-25/2016-01-05<br/>"
    )

#Convert the query to a dictionary
@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-22').filter(Measurement.date <= '2017-08-23').order_by(Measurement.date)
    
    prcp_data = []
    for r in results:
        prcp_dict = {}
        prcp_dict['date'] = r.date
        prcp_dict['prcp'] = r.prcp
        prcp_data.append(prcp_dict)
        
    return jsonify(prcp_data)
    session.close()

    
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name, Measurement.station).filter(Station.station == Measurement.station).group_by(Station.name).all()

    stations_data = []
    for r in results:
        stations_dict = {}
        stations_dict['name']    = r.name
        stations_dict['station'] = r.station
        stations_data.append(stations_dict)
    
    return jsonify(stations_data)
    session.close()
    
@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >='2016-08-22').filter(Measurement.date <= '2017-08-23').order_by(Measurement.date)
    
    tobs_data = []
    for r in results:
        tobs_dict = {}
        tobs_dict['date'] = r.date
        tobs_dict['tobs'] = r.tobs
        tobs_data.append(tobs_dict)
    
    return jsonify(tobs_data)
    session.close()

@app.route("/api/v1.0/<start>")
def temp_stats_start(start):
    results = session.query(func.min(Measurement.tobs).label('min'), func.avg(Measurement.tobs).label('avg'), func.max(Measurement.tobs).label('max')).filter(Measurement.date >= start).all()
    
    date_range_stats_data = []
    for r in results:
        date_range_stats_dict = {}
        date_range_stats_dict['Start Date'] = start
        date_range_stats_dict['Minimum Temperature'] = r.min
        date_range_stats_dict['Average Temperature'] = r.avg
        date_range_stats_dict['Maximum Temperature'] = r.max
        date_range_stats_data.append(date_range_stats_dict)
        
    return jsonify(date_range_stats_data)
    session.close()

@app.route("/api/v1.0/<start>/<end>")
def temp_stats_start_end(start, end):
    results = session.query(func.min(Measurement.tobs).label('min'), func.avg(Measurement.tobs).label('avg'), func.max(Measurement.tobs).label('max')).filter(Measurement.date >= start).filter(Measurement.date <=end).all()
    
    date_range_stats_data = []
    for r in results:
        date_range_stats_dict = {}
        date_range_stats_dict['Start Date'] = start
        date_range_stats_dict['End Date'] = end
        date_range_stats_dict['Minimum Temperature'] = r.min
        date_range_stats_dict['Average Temperature'] = r.avg
        date_range_stats_dict['Maximum Temperature'] = r.max
        date_range_stats_data.append(date_range_stats_dict)
        
    return jsonify(date_range_stats_data)
    session.close()

if __name__ == '__main__':
    app.run(debug=True)