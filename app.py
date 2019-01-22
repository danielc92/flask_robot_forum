from flask import Flask,render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, static_folder='static')
app.debug = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
current_directory = os.getcwd()
database_path = '/notebooks/robots'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + current_directory + database_path
db = SQLAlchemy(app)

class Robots(db.Model):
	"""Maps to robots table"""
	__table_name__ = 'robots'
	robot_id = db.Column('robot_id', db.Float)
	robot_name = db.Column('robot_name', db.Text)
	robot_avatar = db.Column('robot_avatar', db.Text)
	robot_age = db.Column('robot_age', db.Float)
	robot_joined = db.Column('robot_joined', db.Text)

@app.route('/')
def home():
	return '<h1>Hello World</h1>'