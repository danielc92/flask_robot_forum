# Robot Forum
A forum built in `flask` and `bulma` using fictional data.

Key notes:
1. Dummy data to be generated in python and exported to sqlite db file.
2. db file feeds into web application using flask-sqlalchemy
3. Avatar files can be generated using `robohash`.
4. 
5. 

# Meta Data
**robots**
- robot_id
- robot_name
- robot_age
- robot_joined

**threads**
- thread_robot_id
- thread_id
- thread_name
- thread_content
- thread_stars
- thread_tags
- thread_date

**comments**
- comment_thread_id
- comment_id
- comment_content
- comment_date
- comment_thumbs_down
- comment_thumbs_up


# Before you get started
Concepts you should be familiar with before starting;
- web applications
- databases/orm
- https/requests
- flask
- python

# Setup
**How to obtain this repository:**
```sh
git clone https://github.com/danielc92/flask_robot_forum.git
```
**Modules/dependencies:**
- `pandas`
- `flask`
- `flask-sqlalchemy`
- `bulma` css framework

Install the following dependences:
```sh
pip install pandas flask flask-sqlalchemy
```

# Tests
- Tested function to return robot text for threads and comments using this [generator](http://carterschieffer.com/hello-robot)
- Generated dummy data for `robots`, `threads` and `comments` tables to `forum-data` subdirectory.
- Pushed dummy data .csv files into sqlite.db file succesfully
- Mapped each table from database to flask application using flask-sqlalchemy
- Tested pushing query result into render template for loop

# Contributors
- Daniel Corcoran

# Sources
- [Robohash - Avatar generator](https://robohash.org/)
- [Flask-SQLAlchemy documentation](http://flask-sqlalchemy.pocoo.org/2.3/)
- [Flask documentation](http://flask.pocoo.org/docs/1.0/)
- [Bulma CSS framework](https://bulma.io/documentation/overview/start/)
- [Heroku (paas)](https://www.heroku.com/)
- [Hello Robot - text generator](http://carterschieffer.com/hello-robot/)
