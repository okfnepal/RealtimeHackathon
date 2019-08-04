#!/usr/bin/env python3
import pyflux as pf
import numpy as np
import pandas as pd
from config import data_file, data_csv, mixed, pkr
from flask import Flask, render_template, request
from sklearn.preprocessing import OneHotEncoder
from scipy.stats import zscore

application = Flask(__name__)

df = pd.read_csv(data_file)
df = df.drop_duplicates()
df1 = pd.read_csv(data_csv)
df1 = df1.drop_duplicates()
df3 = pd.read_csv(mixed)
df3 = df3.drop_duplicates()
df4 = pd.read_csv(pkr)
onehotencoder = OneHotEncoder()

#Hourly Basis Values of Bhaktapur
@application.route('/hourlydata')
def hour_ac():
  data = df
  data = data.drop_duplicates(subset='localDateTime')
  data['hour'] = pd.to_datetime(data['localDateTime']).dt.hour
  data['hour'] = data['hour'].astype(int)
  data = data[['hour','value']]
  data = data.groupby(['hour'])[['value']].mean()
  data = pd.DataFrame(data)
  data = data.sort_index()
  series = [{"name": 'Value', "data": data['value'].values.tolist()}]
  xAxis = {"categories": list(data['value'].keys()),"title": {"text": 'Hour'}}
  title = {"text": 'Hourly values of Bhaktapur Data'}
  return render_template('viz.html',title=title, series=series, xAxis=xAxis)

@application.route('/zoom')
def zoomed():
  data = df
  data = data.drop_duplicates(subset='localDateTime')
  data['index'] = data.index
  return render_template('zoom.html')

#Weekly Data of Bhaktapur
@application.route('/weeklydata')
def week_ac():
  data = df
  data = data.drop_duplicates(subset='localDateTime')
  data['week'] = pd.to_datetime(data['localDateTime']).dt.week
  data['week'] = data['week'].astype(int)
  data = data[['week','value']]
  data = data.groupby(['week'])[['value']].mean()
  data = pd.DataFrame(data)
  data = data.sort_index()
  series = [{"name": 'Value', "data": data['value'].values.tolist()}]
  xAxis = {"categories": list(data['value'].keys()),"title": {"text": 'Week'}}
  title = {"text": 'Weekly values of Bhaktapur Data'}
  return render_template('viz.html',title=title, series=series, xAxis=xAxis)

#Weekly Data of Bhaktapur
@application.route('/dailydata')
def daily_viz():
  data = df
  data = data.drop_duplicates(subset='localDateTime')
  data['week'] = pd.to_datetime(data['localDateTime']).dt.day
  data['week'] = data['week'].astype(int)
  data = data[['week','value']]
  data = data.groupby(['week'])[['value']].mean()
  data = pd.DataFrame(data)
  data = data.sort_index()
  series = [{"name": 'Value', "data": data['value'].values.tolist()}]
  xAxis = {"categories": list(data['value'].keys()),"title": {"text": 'Days'}}
  title = {"text": 'Weekly values of Bhaktapur Data'}
  return render_template('viz.html',title=title, series=series, xAxis=xAxis)

#Weekday Data of Bhaktapur
@application.route('/weekday')
def weekday_viz():
  data = df
  data = data.drop_duplicates(subset='localDateTime')
  data['weekday'] = pd.to_datetime(data['localDateTime']).dt.weekday
  data['weekday'] = data['weekday'].astype(str)
  data = data[['weekday','value']]
  data = data.groupby(['weekday'])[['value']].mean()
  data = pd.DataFrame(data)
  series = [{"name": 'Value', "data": data['value'].values.tolist()}]
  xAxis = {"categories": list(data['value'].keys()),"title": {"text": 'Week Days'}}
  title = {"text": 'Week Day values of Bhaktapur Data'}
  return render_template('viz.html',title=title, series=series, xAxis=xAxis)

#Weekday Basis comparison of Dang and Bhaktapur
@application.route('/place/weekday')
def weekday_value():
  data = df3[['stationName','localDateTime','value']]
  data = data.groupby(['stationName','localDateTime'])[['value']].mean()
  data = pd.DataFrame(data).reset_index()
  data['weekday'] = pd.to_datetime(data['localDateTime']).dt.weekday
  data['weekday'] = data['weekday'].astype(str)
  data = data[['stationName','weekday','value']]
  data = data.groupby(['stationName','weekday'])[['value']].mean()
  data = pd.DataFrame(data).reset_index()
  bkt = data[data['stationName']=='Bhaktpur ']
  dang = data[data['stationName']=='Dang']
  series = [{"name": 'Bhaktapur', "data": bkt['value'].values.tolist()}, 
            {"name": 'Dang', "data": dang['value'].values.tolist()}]
  xAxis = {"categories": list(data['weekday'].unique()),"title": {"text": 'Week Days'}}
  title = {"text": 'Values Comparison in Weekdays of Dang and Bhaktapur'}
  return render_template('viz.html',title=title, series=series, xAxis=xAxis)

#Daily Basis comparison of Dang and Bhaktapur
@application.route('/place/daily')
def day_value():
  data = df3[['stationName','localDateTime','value']]
  data = data.groupby(['stationName','localDateTime'])[['value']].mean()
  data = pd.DataFrame(data).reset_index()
  data['weekday'] = pd.to_datetime(data['localDateTime']).dt.day
  data['weekday'] = data['weekday'].astype(str)
  data = data[['stationName','weekday','value']]
  data = data.groupby(['stationName','weekday'])[['value']].mean()
  data = pd.DataFrame(data).reset_index()
  bkt = data[data['stationName']=='Bhaktpur ']
  dang = data[data['stationName']=='Dang']
  series = [{"name": 'Bhaktapur', "data": bkt['value'].values.tolist()}, 
            {"name": 'Dang', "data": dang['value'].values.tolist()}]
  xAxis = {"categories": list(data['weekday'].unique()),"title": {"text": 'Day'}}
  title = {"text": 'Values Comparison in Weekdays of Dang and Bhaktapur'}
  return render_template('viz.html',title=title, series=series, xAxis=xAxis)

# Hourly
@application.route('/place/hourly')
def hourly_value():
  data = df3[['stationName','localDateTime','value']]
  data = data.groupby(['stationName','localDateTime'])[['value']].mean()
  data = pd.DataFrame(data).reset_index()
  data['weekday'] = pd.to_datetime(data['localDateTime']).dt.hour
  data['weekday'] = data['weekday'].astype(str)
  data = data[['stationName','weekday','value']]
  data = data.groupby(['stationName','weekday'])[['value']].mean()
  data = pd.DataFrame(data).reset_index()
  bkt = data[data['stationName']=='Bhaktpur ']
  dang = data[data['stationName']=='Dang']
  series = [{"name": 'Bhaktapur', "data": bkt['value'].values.tolist()}, 
            {"name": 'Dang', "data": dang['value'].values.tolist()}]
  xAxis = {"categories": list(data['weekday'].unique()),"title": {"text": 'Week Days'}}
  title = {"text": 'Values Comparison Hourly of Dang and Bhaktapur'}
  return render_template('viz.html',title=title, series=series, xAxis=xAxis)

#Hourly Basis comparison
@application.route('/pkr/hour/')
def hour_pkr():
  data = df4[['localDateTime','value','airTemperature','rainfall']]
  data = data.drop_duplicates(subset='localDateTime')
  data['hour'] = pd.to_datetime(data['localDateTime']).dt.hour
  data['hour'] = data['hour'].astype(int)
  data = data[['hour','value','airTemperature','rainfall']]
  data = data.groupby(['hour'])[['value','airTemperature','rainfall']].sum()
  data = pd.DataFrame(data)
  data = data.sort_index()
  series = [{"name": 'Value', "data": data['value'].values.tolist()}, {"name": 'Air Temperature', "data": data['airTemperature'].values.tolist()},{"name": 'Rainfall', "data": data['rainfall'].values.tolist()}]
  xAxis = {"categories": list(data['value'].keys()),"title": {"text": 'Hour'}}
  title = {"text": 'Value vs Air Temperature vs Rainfall in Every Hour'}
  return render_template('viz.html',title=title, series=series, xAxis=xAxis)

#Prediction of Values of Dang and Bhaktapur
@application.route('/prediction/bkt')
def predictions() :
  data = df.drop_duplicates(subset='localDateTime')
  data['month_year'] = pd.to_datetime(data['localDateTime']).dt.to_period('D')
  data['month_year'] = data['month_year'].astype(str)
  frame1 = data.groupby('month_year')[['value']].mean().reset_index()
  frame1 = frame1.set_index('month_year')
  z = frame1[['value']]
  value_model = pf.ARIMA(data=z, ar=4, ma=4, family=pf.Normal())
  value_model.fit("MLE")
  value_new = value_model.predict(h=3)
  final = pd.concat([value_new], axis=1, join_axes=[value_new.index])
  new = pd.DataFrame(final)
  new.index = new.index.astype(str)
  xAxis = {"categories": list(new['value'].keys())}
  series = [{"name": 'Value', "data": new['value'].values.tolist()}]
  title = {"text": 'Value Prediction of Bhaktapur'}
  return render_template('pre.html',title=title, series=series, xAxis=xAxis)

if __name__ == '__main__':
	application.run('0.0.0.0', debug = True)