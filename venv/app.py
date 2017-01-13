from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# db admin tool
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import requests

# creates app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Ken@localhost/kensdatabase'
app.config['SECRET_KEY'] = '????-/???g8??'

# creates db connection object
db = SQLAlchemy(app)

class Alarm(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  numOfUpvotes = db.Column(db.Integer)
  text = db.Column(db.String(255))
  
  def __init__(self, numOfUpvotes, text):
    self.numOfUpvotes = numOfUpvotes
    self.text = text

  def __repr__(self):
    return '<Alarm %r>' % self.id

@app.route('/')
def index():
  alarms = Alarm.query.all()
  alarms = sorted(alarms, key=lambda x: x.id, reverse=False)
  return render_template('index.html', alarms=alarms)

@app.route('/alarm/', methods=['POST'])
def addAlarm():
  numOfUpvotes = 0
  text=request.form['text']

  # check if text is blank
  if text == '':
    return redirect(url_for('index'))

  text = text.upper()
  myAlarm = Alarm(numOfUpvotes, text)
  db.session.add(myAlarm)
  db.session.commit()

  alarmId = myAlarm.id

  # make post to heroku
  r = requests.post("http://handshake-bellbird.herokuapp.com/push", data={'alarm_id': alarmId})
  print r

  return redirect(url_for('index'))

@app.route('/upvote/', methods=['PUT'])
def upvote():
  alarmId = request.form['alarmId']
  print alarmId
  myAlarm = Alarm.query.filter_by(id=alarmId).all()[0]
  myAlarm.numOfUpvotes += 1
  db.session.commit()
  return '<div>Upvote successful!</div>'











