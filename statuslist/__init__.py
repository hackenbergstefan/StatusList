from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = None
db = None


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

    from . import views


def run():
    """Run the statuslist Flask app."""
    app.run()


_create_app()
