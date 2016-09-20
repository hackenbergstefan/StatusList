from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')

from . import views


def run():
    """Run the statuslist Flask app."""
    app.run()
