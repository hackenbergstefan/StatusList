from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = None
db = None

def _create_test_data():
    """Creates test data."""
    import datetime
    from .model import Job
    job = Job('Hasen ausmisten', 3)
    db.session.commit()
    job.run(datetime.date(2016, 9, 30))
    db.session.commit()
    job = Job('Einkaufen', 10)
    db.session.commit()
    job.run(datetime.date.today() - datetime.timedelta(days=1))
    db.session.commit()
    job = Job('Fenster putzen', 150)
    db.session.commit()
    job.run(datetime.date.today() - datetime.timedelta(days=100))
    db.session.commit()
    job = Job('Saugen', 3)
    db.session.commit()
    job.run(datetime.date(2016, 9, 7))
    db.session.commit()
    job = Job('Hasen ausmisten Klos', 3)
    db.session.commit()
    job.run(datetime.date(2016, 10, 1))
    db.session.commit()
    job = Job('Kühlschrank sauber machen', 30)
    db.session.commit()
    job.run(datetime.date.today() - datetime.timedelta(days=0))
    db.session.commit()


def _init_db():
    """Creates database if neccessary."""
    import os
    import re
    global db
    db = SQLAlchemy(app)

    from . import model

    match = re.match(r'^sqlite:///(.*)$', app.config['SQLALCHEMY_DATABASE_URI'])
    if match and not os.path.exists(match.group(1)):
        db.create_all()

    # Example configuration
    #db.drop_all()
    #_create_test_data()


def _create_app():
    """Create the statuslist Flask app."""
    global app
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    _init_db()

    from . import views


def run():
    """Run the statuslist Flask app."""
    app.run(host='0.0.0.0', port='8001')


_create_app()
