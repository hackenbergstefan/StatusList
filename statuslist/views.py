from . import app, db
from .model import Job, Category
import time


def test():
    job = Job(500, 'Hasen ausmisten')
    job.run()
    job.run()
    for job in Job.query.all():
        app.logger.info(job.next_run)


@app.route('/')
def index():
    test()
    return 'Hello World'
