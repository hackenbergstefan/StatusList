from . import app, db
from .model import Job
from flask import render_template, request, abort, redirect, url_for
import logging



@app.route('/', methods=['GET', 'POST'])
def index():
    """Provides the route of this website."""
    if request.method == 'POST':
        return index_handle_request()

    jobs = Job.query.all()
    jobs = sorted(jobs, key=lambda job: job.days_left)

    return render_template(
        'index.html',
        jobs=jobs,
        job_class=job_class,
        job_width=job_width
    )


@app.route('/editjob', methods=['GET', 'POST'])
def editjob():
    """Page for editing jobs."""
    # If cancel in args, redirect to referrer and rollback db changes
    if 'cancel' in request.args:
        db.session.rollback()
        return redirect(request.args['cancel'])

    if 'id' in request.args and request.args['id'].isdigit():
        job = Job.query.filter_by(id=int(request.args['id'])).first()
    # If no arguments are given, create new job
    elif len(request.args) == 0:
        job = Job()

    # If commit in args, commit
    if 'commit' in request.args:
        if 'description' in request.args:
            job.description = request.args['description']
        if 'interval' in request.args:
            job.interval = int(request.args['interval'])
        db.session.commit()
        return redirect(url_for('index'))
    # If delete in args, delete job
    elif 'delete' in request.args:
        db.session.delete(job)
        db.session.commit()

        for job in Job.query.all():
            print(job)

        return redirect(url_for('index'))

    # if neither commit nor cancel in args, show job
    return render_template(
        'editjob.html',
        job=job
    )


def job_class(job: Job):
    """Returns the current status class for a given job.

    :param job: The job.
    :type job: Job
    :rtype: str
    """
    if job.days_left < 0:
        return 'red'
    elif job.days_left/job.interval < 0.1 or job.days_left == 0:
        return 'yellow'
    else:
        return 'green'


def job_width(job: Job):
    from math import exp
    return 100*exp(-0.1*job.days_left)


def index_handle_request():
    """Handles POST requests to index."""
    assert request.method == 'POST'

    req = request.form
    if 'do' in req:
        Job.query.filter_by(id=int(req['do'])).first().run()
        db.session.commit()
        return redirect(url_for('index'))
    elif 'add' in req:
        return redirect(url_for('editjob'))
