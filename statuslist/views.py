from . import app
from .model import Job
from flask import render_template, request, abort, redirect, url_for



@app.route('/', methods=['GET', 'POST'])
def index():
    """Provides the route of this website."""
    if request.method == 'POST':
        index_handle_request()
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
    print(request.form)
    if 'id' in request.args:
        job = Job.query.filter_by(id=int(request.args['id'])).first_or_404()

    try:
        return render_template(
            'editjob.html',
            job=job
        )
    except Exception:
        return render_template(
            'editjob.html',
            job=Job.query.filter_by(id=1).first_or_404()
        )
        return str(request.args)



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
