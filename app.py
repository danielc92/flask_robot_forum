
from flask import Flask
from flask import request
from flask import url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import desc

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
    thread_robot_id = db.Column(db.Float, db.ForeignKey('robots.robot_id'))
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
    comment_thread_id = db.Column(db.Float, db.ForeignKey('threads.thread_id'))
    comment_content = db.Column(db.Text)
    comment_date = db.Column(db.Text)
    comment_thumbs_up = db.Column(db.Float)
    comment_thumbs_down = db.Column(db.Float)

    def __repr__(self):
        return '<comments %r>' % self.comment_id

# Create alias for ORM classes
C = Comments
T = Threads
R = Robots

# Helper Functions

def fetch_side_data():
    """Fetch right hand side bar data from database and return dictionary"""
    limit=10

    starred_threads = T.query.order_by(desc(T.thread_stars)).limit(limit)
    new_members = R.query.order_by(desc(R.robot_joined)).limit(limit)
    latest_comments = C.query.order_by(desc(C.comment_date)).limit(limit)

    sidebar_data = {'starred-threads': starred_threads,
                    'new-members': new_members,
                    'latest-comments': latest_comments}

    return sidebar_data

# Routes

@app.route('/')
def home():
    return render_template('home.html', side_data=fetch_side_data())

@app.route('/members/')
def members():
    members = R.query.all()
    return render_template('members.html', members=members, side_data=fetch_side_data())

@app.route('/threads/')
def threads():
    threads = T.query.join(R, R.robot_id == T.thread_robot_id).add_columns(R.robot_name, 
        T.thread_name, 
        T.thread_stars,
        T.thread_id,
        T.thread_date,
        T.thread_tags,
        T.thread_content).all()
    return render_template('threads.html', threads=threads, side_data=fetch_side_data())

@app.route('/threads/view/')
def threadview():

    thread_id = request.args.get('thread_id')

    thread = T.query.join(R, R.robot_id == T.thread_robot_id).add_columns(R.robot_name,
        R.robot_avatar, 
        T.thread_name, 
        T.thread_stars,
        T.thread_id,
        T.thread_date,
        T.thread_tags,
        T.thread_content).filter(T.thread_id==thread_id).first()
    print(thread)
    return render_template('thread-view.html', thread=thread, side_data=fetch_side_data())

@app.route('/test-query/')
def test():
    robots = R.query.all()
    threads = T.query.all()
    comments = C.query.all()
    print(robots)
    print(threads)
    print(comments)
    return '<h1>Test Route</h1>'

@app.route('/test-join/')
def testjoin():
    query = C.query.join(R, R.robot_id == T.thread_robot_id).add_columns(R.robot_name).order_by(C.comment_id).limit(10)
    for q in query:
        print(q.robot_name)
    return '<h1>Test Join Route</h1>'