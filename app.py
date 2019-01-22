
from flask import Flask,render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, static_folder='static')
app.debug = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
current_directory = os.getcwd()
database_path = '/notebooks/robot.db'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + current_directory + database_path
print(app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app)

# Database Models

class Robots(db.Model):
    """Maps to robots table"""
    __tablename__ = 'robots'

    robot_id = db.Column(db.Float, primary_key=True)
    robot_name = db.Column(db.Text)
    robot_avatar = db.Column(db.Text)
    robot_age = db.Column(db.Float)
    robot_joined = db.Column(db.Text)

    def __repr__(self):
        return '<robots %r>' % self.robot_id

class Threads(db.Model):
    """Maps to threads table"""
    __tablename__ = 'threads'

    thread_id = db.Column(db.Float, primary_key=True)
    thread_robot_id = db.Column(db.Float)
    thread_name = db.Column(db.Text)
    thread_tags = db.Column(db.Text)
    thread_content = db.Column(db.Text)
    thread_date = db.Column(db.Text)
    thread_stars = db.Column(db.Float)

    def __repr__(self):
        return '<threads %r>' % self.thread_id

class Comments(db.Model):
    """Maps to comments table"""
    __tablename__ = 'comments'

    comment_id = db.Column(db.Float, primary_key=True)
    comment_thread_id = db.Column(db.Float)
    comment_content = db.Column(db.Text)
    comment_date = db.Column(db.Text)
    comment_thumbs_up = db.Column(db.Float)
    comment_thumbs_down = db.Column(db.Float)

    def __repr__(self):
        return '<comments %r>' % self.comment_id

# Routes

@app.route('/')
def home():
    robots = Robots.query.all()
    return render_template('base.html', robots = robots)

@app.route('/test/')
def test():
    robots = Robots.query.all()
    threads = Threads.query.all()
    comments = Comments.query.all()
    print(robots)
    print(threads)
    print(comments)
    return '<h1>Test Route</h1>'