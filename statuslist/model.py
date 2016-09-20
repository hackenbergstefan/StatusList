from . import db
import datetime


class Category(db.Model):
    """Category of a Job."""

    __tablename__ = 'category'
    name = db.Column(db.String(50), primary_key=True)
    """Name of this Category."""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %s>' % self.name


class Job(db.Model):
    """A Job."""

    __tablename__ = 'job'
    id = db.Column(db.Integer, primary_key=True)
    interval = db.Column(db.Integer)
    description = db.Column(db.String(500))
    runs = db.relationship(
        'JobRuns',
        backref='job',
        order_by='desc(JobRuns.date)'
    )

    def __init__(self, interval, description):
        self.interval = interval
        self.description = description
        db.session.add(self)
        db.session.commit()

    def run(self):
        run = JobRuns(self, datetime.datetime.today())
        db.session.add(run)
        db.session.commit()

    @property
    def last_run(self):
        if len(self.runs) > 0:
            return self.runs[0].date
        return None

    @property
    def next_run(self):
        if self.last_run is not None:
            next_run = self.last_run + datetime.timedelta(seconds=self.interval)
            return next_run
        return datetime.datetime.today()


class JobRuns(db.Model):
    """Table holding information of Job executions."""

    __tablename__ = 'jobruns'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    job_id = db.Column(db.Integer, db.ForeignKey(Job.id))

    def __init__(self, job, date):
        self.date = date
        self.job_id = job.id

    def __repr__(self):
        return '<JobRuns job_id=%d date=%s>' % (self.job_id, self.date)
