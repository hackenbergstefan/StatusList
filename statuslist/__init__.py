from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = None
db = None

def _create_test_data():
    """Creates test data."""
    import datetime
    from .model import Job
    job = Job('Hasen ausmisten', 3)
    job.run(datetime.date(2016, 9, 30))
    Job('Einkaufen', 10)
    job = Job('Fenster putzen', 30)
    job.run(datetime.date(2016, 9, 7))
    job = Job('Saugen', 3)
    job.run(datetime.date(2016, 9, 7))


def _init_db():
    """Creates database if neccessary."""
    import os
    global db
    db = SQLAlchemy(app)
    from . import model
    #if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
    db.drop_all()
    db.create_all()


def _create_app():
    """Create the statuslist Flask app."""
    global app
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    _init_db()

    _create_test_data()

    from . import views


def run():
    """Run the statuslist Flask app."""
    app.run()


_create_app()
