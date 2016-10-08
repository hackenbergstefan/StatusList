from . import db
import datetime


class Job(db.Model):
    """A Job."""

    __tablename__ = 'job'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    interval = db.Column(db.Integer)
    runs = db.relationship(
        'JobRuns',
        backref='job',
        order_by='desc(JobRuns.date)'
    )

    def __init__(self, description='', interval=0):
        self.description = description
        self.interval = interval
        db.session.add(self)

    def run(self, date: datetime.date=None):
        """Runs job.

        :param date: If not None, set run date to date.
        :type date: datetime
        """
        if date is None:
            date = datetime.date.today()
        run = JobRuns(self, date)

    @property
    def last_run(self):
        if len(self.runs) > 0:
            return self.runs[0].date
        return None

    @property
    def next_run(self):
        if self.last_run is not None:
            next_run = self.last_run + datetime.timedelta(days=self.interval)
            return next_run.date()
        return datetime.date.today()

    @property
    def days_left(self):
        """Days left until next run."""
        return (self.next_run - datetime.date.today()).days

    def __repr__(self):
        return "<Job id=%d description=%s interval=%d>" % (
            self.id,
            self.description,
            self.interval
        )



class JobRuns(db.Model):
    """Table holding information of Job executions."""

    __tablename__ = 'jobruns'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    job_id = db.Column(db.Integer, db.ForeignKey(Job.id))

    def __init__(self, job, date):
        self.date = date
        self.job_id = job.id
        db.session.add(self)

    def __repr__(self):
        return '<JobRuns job_id=%d date=%s>' % (self.job_id, self.date)
