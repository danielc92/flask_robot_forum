"""Imports."""
from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import desc
from sqlalchemy import and_
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
    robot_image = db.Column(db.Text)

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
             R.robot_id,
             R.robot_image]

C_columns = [C.comment_content,
             C.comment_date,
             C.comment_id,
             C.comment_thread_id,
             C.comment_thumbs_down,
             C.comment_thumbs_up]

all_columns = T_columns + R_columns + C_columns

# Helper Functions
def clean_search(raw_search):
    """Return cleaned search item."""
    if len(raw_search.strip()) > 0:
        search = raw_search
    else:
        search = None

    return search


def return_search_terms(search_string):
    """Return search terms as a list from a search string object."""
    if search_string == '':
        return [search_string]
    else:
        terms = search_string.split(' ')
        terms_stripped = list(map(str.strip, terms))
        search_list = [term for term in terms_stripped if term != '']
        return search_list


def return_search_conditions(search_list, table_name):
    """Return list of search conditions using sqlalchemy."""
    if table_name == 'Robots':
        search_conditions = [R.robot_name.ilike('%{}%'.format(term)) for term in search_list]
    elif table_name == 'Threads':   
        search_conditions = [T.thread_name.ilike('%{}%'.format(term)) for term in search_list]
    return search_conditions


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


@app.route('/members/', methods=['POST', 'GET'])
def members():
    """Route to view a multiple members."""
    if request.method == "POST":
        search = request.form['search']
        return redirect(url_for('members', search=search, page_number=1))
    else:
        search = request.args.get('search', None)
        page_number_string = request.args.get('page_number', '1')
        page_number = float(page_number_string)
        if search:
            search_terms = return_search_terms(search)
            search_conditions = return_search_conditions(search_terms, 'Robots')
            members = R.query.filter(and_(*search_conditions)).order_by(R.robot_name)\
                             .paginate(page=page_number, per_page=app.config['PER_PAGE'], error_out=True)
        else:
            members = R.query.order_by(R.robot_name).paginate(page=page_number, per_page=app.config['PER_PAGE'], error_out=True)
        
        return render_template('members.html', members=members, search=search, side_data=fetch_side_data())


@app.route('/threads/', methods = ['POST', 'GET'])
def threads():
    """Route to view multiple threads."""
    if request.method == "POST":
        search = request.form['search']
        return redirect(url_for('threads', search=search, page_number=1))
    else:
        search = request.args.get('search', None)
        page_number_string = request.args.get('page_number', '1')
        page_number = float(page_number_string)
        
        if search:
            search_terms = return_search_terms(search)
            search_conditions = return_search_conditions(search_terms, 'Threads')
            threads = T.query.join(R, R.robot_id == T.thread_robot_id)\
                      .add_columns(*R_columns + T_columns)\
                      .order_by(T.thread_name)\
                      .filter(*search_conditions)\
                      .paginate(page=page_number, per_page=app.config['PER_PAGE'], error_out=True)
        else:
            threads = T.query.join(R, R.robot_id == T.thread_robot_id)\
                             .add_columns(*R_columns + T_columns)\
                             .order_by(T.thread_name)\
                             .paginate(page=page_number, per_page=app.config['PER_PAGE'], error_out=True)
        
        return render_template('threads.html', threads=threads, search=search, side_data=fetch_side_data())


@app.route('/threads/view/')
def threadview():
    """Route to view a single thread."""
    thread_id = request.args.get('thread_id')

    threads = T.query.join(R, T.thread_robot_id == R.robot_id)\
                     .filter(T.thread_id == thread_id)\
                     .add_columns(*R_columns + T_columns).all()

    comments = C.query.join(T, C.comment_thread_id == T.thread_robot_id)\
                      .join(R, R.robot_id == T.thread_robot_id)\
                      .filter(T.thread_id == thread_id)\
                      .add_columns(*all_columns).all()

    return render_template('thread-view.html', threads=threads, comments=comments, side_data=fetch_side_data())


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
    thread_id = int(request.args.get('thread_id','1'))
    query = C.query.join(T, C.comment_thread_id == T.thread_robot_id)\
                   .join(R, R.robot_id == T.thread_robot_id)\
                   .filter(T.thread_id == thread_id)\
                   .add_columns(*all_columns).order_by(C.comment_date)\
                   .all()

    for q in query:
        print(q.comment_content)

    return '<h1>Test Join Route</h1>'
