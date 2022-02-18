import time
from app import db, crypt, UserMixin, current_app
from app.model.util import is_valid_email, SchedulingTimeError, InvalidServiceRequest
from datetime import datetime as dt
from uuid import uuid4
import os
import pytz
import time


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(225), primary_key=True)
    name = db.Column(db.String(225), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    reg_date = db.Column(db.DateTime, nullable=False)
    all_job = db.relationship("Jobs", backref="belongs_to", cascade="all, delete-orphan", uselist = True, lazy="dynamic")

    def __init__(self, email, full_name, password):
        if is_valid_email(email):
            self.email = email
        self.name = full_name
        self.password = crypt.generate_password_hash(password)
        self.reg_date = dt.now() # current datetime of the server

    def get_id(self):
        return self.email
    
    def verify_password(self, password: str) -> bool:
        return crypt.check_password_hash(self.password, password)


class Jobs(db.Model):
    __tablename__ = 'jobs'

    job_id = db.Column(db.String(36), primary_key=True) # uuid id
    user = db.Column(db.String(225), db.ForeignKey("user.email", ondelete="CASCADE"), nullable=False)
    ref_name = db.Column(db.UnicodeText)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Time, nullable=False)

    command_used = db.Column(db.UnicodeText, nullable=False)

    # scheduled on is refered as 's' in attribute names starting
    syear = db.Column(db.Integer, nullable=False)
    smonth = db.Column(db.Integer, nullable=False)
    sday = db.Column(db.Integer, nullable=False)
    stime = db.Column(db.Time, nullable=False)

    completedOn = db.Column(db.DateTime)
    tool_used = db.Column(db.String(30), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    description = db.Column(db.UnicodeText)

    @property
    def micro(self):
        type_ = self.tool_used.split()[-1]
        return dict(id = self.job_id, type_=type_, tool_used=self.tool_used, ref_name = self.ref_name,
            date_ = f'{self.year}-{self.month}-{self.day}', time_= self.time.strftime("%H:%M"), status = self.status
        )


    def __init__(self, user, ref_name, scheduled_for, command_used, tool_used):
        self.tool_used = current_app.config["TOOLS"].get(tool_used)
        if tool_used is not None: # if tool requested is available
            self.user = user.email
            self.ref_name = ref_name
            self.job_id = str(uuid4())
            self.command_used = command_used

            # rest to do
            print(current_app.config["TIMEZONE"])
            timezone = current_app.config["TIMEZONE"]

            k = dt.strptime(scheduled_for, "%Y-%m-%d %H:%M")
            given_time = dt(k.year, k.month, k.day, k.hour, k.minute, tzinfo=timezone)
            
            c = dt.now(timezone)
            current_time = dt(c.year, c.month, c.day, c.hour, c.minute, tzinfo=timezone)

            if current_time > given_time:
                raise SchedulingTimeError(time.tzname[time.daylight])
            
            self.year, self.syear = given_time.year, current_time.year
            self.month, self.smonth = given_time.month, current_time.month
            self.day, self.sday = given_time.day, current_time.day
            self.time, self.stime = given_time.time(), current_time.time()

            self.status = 0
        else:
            raise InvalidServiceRequest("Invalid schedule request")

    def __str__(self):
        return self.command_used

    def __repr__(self):
        return f'{self.job_id} |{self.ref_name} |-> {self}'

    @property
    def get_wait_time(self):
        gtime = self.time
        stime = self.stime
        given_dt = dt(self.year, self.month, self.day, gtime.hour, gtime.minute)
        job_dt = dt(self.syear, self.smonth, self.sday,  stime.hour, stime.minute)
        time_diff = given_dt - job_dt
        return time_diff.total_seconds()

    @property
    def get_current_wait_time(self):
        c = dt.now(current_app.config["TIMEZONE"])
        current_time = dt(c.year, c.month, c.day, c.hour, c.minute, tzinfo=current_app.config["TIMEZONE"])
        gtime = self.time
        given_dt = dt(self.year, self.month, self.day, gtime.hour, gtime.minute, tzinfo=current_app.config["TIMEZONE"])
        if given_dt > current_time:
            time_diff = given_dt - current_time
            print((time_diff.total_seconds()))
            return (time_diff.total_seconds())
        else:
            return 0


    def setCompleted(self, output_path):
        self.status = 1
        self.completedOn = dt.now() # current time
        if os.path.exists(output_path):
            with open(output_path) as f:
                output = f.read()
                self.description = output
            os.remove(output_path)

