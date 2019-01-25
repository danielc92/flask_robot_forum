"""Imports."""
from flask import Flask
from flask import request
from flask import url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import desc
#from sqlalchemy.sql import func

app = Flask(__name__, static_folder='static')
app.debug = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PER_PAGE'] = 12
current_directory = os.getcwd()
database_path = '/notebooks/robot.db'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + current_directory + database_path
print(app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app)

# Database Models


class Robots(db.Model):
    """Maps to robots table."""

    __tablename__ = 'robots'

    robot_id = db.Column(db.Float, primary_key=True)
    robot_name = db.Column(db.Text)
    robot_avatar = db.Column(db.Text)
    robot_age = db.Column(db.Float)
    robot_joined = db.Column(db.Text)

    def __repr__(self):
        """Return record string."""
        return '<robots %r>' % self.robot_id


class Threads(db.Model):
    """Maps to threads table."""

    __tablename__ = 'threads'

    thread_id = db.Column(db.Float, primary_key=True)
    thread_robot_id = db.Column(db.Float, db.ForeignKey('robots.robot_id'))
    thread_name = db.Column(db.Text)
    thread_tags = db.Column(db.Text)
    thread_content = db.Column(db.Text)
    thread_date = db.Column(db.Text)
    thread_stars = db.Column(db.Float)

    def __repr__(self):
        """Return record string."""
        return '<threads %r>' % self.thread_id


class Comments(db.Model):
    """Maps to comments table."""

    __tablename__ = 'comments'

    comment_id = db.Column(db.Float, primary_key=True)
    comment_thread_id = db.Column(db.Float, db.ForeignKey('threads.thread_id'))
    comment_content = db.Column(db.Text)
    comment_date = db.Column(db.Text)
    comment_thumbs_up = db.Column(db.Float)
    comment_thumbs_down = db.Column(db.Float)

    def __repr__(self):
        """Return record string."""
        return '<comments %r>' % self.comment_id

# Create alias for ORM classes
C = Comments
T = Threads
R = Robots

# Create metadata
T_columns = [T.thread_content,
             T.thread_date,
             T.thread_stars,
             T.thread_id,
             T.thread_tags,
             T.thread_name,
             T.thread_robot_id]

R_columns = [R.robot_name,
             R.robot_age,
             R.robot_avatar,
             R.robot_joined,
             R.robot_id]

C_columns = [C.comment_content,
             C.comment_date,
             C.comment_id,
             C.comment_thread_id,
             C.comment_thumbs_down,
             C.comment_thumbs_up]


# Helper Functions


def fetch_side_data():
    """Fetch right hand side bar data from database and return dictionary."""
    limit = 5

    starred_threads = T.query.order_by(desc(T.thread_stars)).limit(limit)
    new_members = R.query.order_by(desc(R.robot_joined)).limit(limit)
    latest_comments = C.query.order_by(desc(C.comment_date)).limit(limit)

    sidebar_data = {'starred-threads': starred_threads,
                    'new-members': new_members,
                    'latest-comments': latest_comments}

    return sidebar_data


@app.route('/')
def home():
    """Route to view news, the home page."""
    return render_template('home.html', side_data=fetch_side_data())


@app.route('/contact/')
def contact():
    """Route to view news, the contact page."""
    return render_template('contact.html', side_data=fetch_side_data())


@app.route('/sources/')
def sources():
    """Route to view news, the sources page."""
    return render_template('sources.html', side_data=fetch_side_data())


@app.route('/about/')
def about():
    """Route to view news, the about page."""
    return render_template('about.html', side_data=fetch_side_data())


@app.route('/members/')
def members():
    """Route to view a multiple members."""
    page_number = request.args.get('page_number', 1)
    members = R.query.paginate(page=1, per_page=app.config['PER_PAGE'], error_out=True)
    return render_template('members.html', members=members, side_data=fetch_side_data())


@app.route('/threads/')
def threads():
    """Route to view multiple threads."""
    threads = T.query.join(R, R.robot_id == T.thread_robot_id)\
                     .add_columns(*R_columns + T_columns).all()
    return render_template('threads.html', threads=threads, side_data=fetch_side_data())


@app.route('/threads/view/')
def threadview():
    """Route to view a single thread."""
    thread_id = request.args.get('thread_id')

    thread = T.query.join(R, R.robot_id == T.thread_robot_id)\
                    .add_columns(*R_columns + T_columns)\
                    .filter(T.thread_id == thread_id).first()
    return render_template('thread-view.html', thread=thread, side_data=fetch_side_data())


@app.route('/members/view/')
def memberview():
    """Route to view a single member."""
    member_id = request.args.get('member_id')

    has_threads = True
    member_data = T.query.join(R, R.robot_id == T.thread_robot_id)\
                         .add_columns(*R_columns + T_columns)\
                         .filter(R.robot_id == member_id).all()

    if not member_data:
        print("MEMBER DATA UPDATED TO ALL ROBOTS")
        member_data = R.query.filter(R.robot_id == member_id).limit(1)
        has_threads = None


    return render_template('member-view.html',
                           has_threads=has_threads,
                           member_data=member_data,
                           side_data=fetch_side_data())

# Test Routes - for checking query results


@app.route('/test-query/')
def test():
    """Test queries."""
    robots = R.query.all()
    threads = T.query.all()
    comments = C.query.all()
    print(threads)
    print(robots)
    print(comments)
    return '<h1>Test Route</h1>'


@app.route('/test-join/')
def testjoin():
    """Test join queries."""
    query = C.query.join(R, R.robot_id == T.thread_robot_id)\
                   .add_columns(R.robot_name)\
                   .order_by(C.comment_id).limit(10)

    for q in query:
        print(q.robot_name)
    return '<h1>Test Join Route</h1>'
