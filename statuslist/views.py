from . import app
from .model import Job
from flask import render_template



@app.route('/')
def index():
    jobs = Job.query.all()
    jobs = sorted(jobs, key=lambda job: job.days_left)
    return render_template('index.html', jobs=jobs)
