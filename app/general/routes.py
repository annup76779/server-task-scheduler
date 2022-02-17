# app
import os
import re
import time

from sqlalchemy import select, insert
from app import current_app, db, PATH
from app.general import api
from app.model import Jobs, User
from app.model.util import (SchedulingTimeError, async_task, scanServerNikto, InvalidServiceRequest, 
scanWebsiteNikto, scanApiZap, emailNotification)
from datetime import datetime

from sqlalchemy.orm import sessionmaker, Session

# flask imports
from flask import abort, redirect, render_template, request, url_for, jsonify, flash
from flask_login import login_required, current_user


OUTPUT_PATH = os.path.join(PATH, api.static_folder)

def updateDatabase(engine, job_id, Jobs, path):
    with Session(engine) as session:
        query = select(Jobs).where(Jobs.job_id == job_id)
        res = session.execute(query, (job_id,))
        job = res.first()[0]
        job.setCompleted(path)
        session.commit()
        job.user
        return job

@async_task
def start_active(job,engine, Jobs, path, email, password):
    print(path, job, engine)
    check = True
    print(job.get_wait_time)
    time.sleep(job.get_wait_time)
    if job.tool_used == "Nikto Server":
        scanServerNikto(job, path)
    elif job.tool_used == "Nikto Website":
        scanWebsiteNikto(job, path)
    elif job.tool_used == "Zap API":
        scanApiZap(job, path)
    else:
        print("False")
        check = False
    if check: 
        job = updateDatabase(engine, job.job_id, Jobs, path)
        if isinstance(job, Jobs):
            emailNotification(job, email, password)


@api.route('/add_job', methods=["POST"])
@login_required
def add_job():
    try:
        scheduled_for = request.form.get('date') + " " + request.form.get("time")
        ref_name = request.form.get("ref_name")
        command =  request.form.get("command")
        tool_used = request.form.get("job_type")
        job = Jobs(current_user,ref_name, scheduled_for, command, tool_used)
        db.session.add(job)
        db.session.commit()

        start_active(job, db.engine, Jobs, os.path.join(OUTPUT_PATH, f"{job.job_id}.txt"), current_app.config["APP_EMAIL"], current_app.config["EMAIL_PASS"])
        flash("Job added successfully.", "success scheduler_alert_box")
        return redirect(url_for("user.dashboard"))

    except SchedulingTimeError as e:
        flash(f"{e}", "danger scheduler_alert_box")
        return redirect(url_for("user.dashboard"))
    
    except InvalidServiceRequest as e:
        flash(f"{e}","danger scheduler_alert_box")
        return redirect(url_for("user.dashboard"))
        
    except Exception as e:
        print(e)
        flash("Something went wrong.", "danger scheduler_alert_box")
        return redirect(url_for("user.dashboard"))


@api.route("/get_job_by_date", methods = ["GET"])
@login_required
def get_job_by_date():
    try:
        date_  = request.args.get("scheduledFor") # date
        print(date_)
        page = request.args.get("page", 1)
        if  date_ is not None:
            date_ = datetime.strptime(date_, "%Y-%m-%d") # convert
            print(date_)
        user = current_user #User.query.filter_by(email = email).first()
        jobs = user.all_job.filter_by(year = date_.year, month = date_.month, day = date_.day).all() # filter
        return jsonify(status = True, jobs = [job.micro for job in jobs],
        )
    except ValueError:
        return jsonify(status = False, msg= "Inavalid date format, YYYY-MM-DD required")
    except:
        return jsonify(status = False, msg="Something went wrong.")

@api.route("/get_all_jobs", methods = ["GET"])
@login_required
def get_all_jobs():
    try:
        page = request.args.get("page", 1)
        user = current_user #User.query.filter_by(email = email).first()
        jobs = user.all_job.all() # filter
        return jsonify(status = True, jobs = [job.micro for job in jobs],
        )
    except Exception as e:
        print(e)
        return jsonify(status = False, msg="Something went wrong.")


@api.route("/job/<uuid:id>")
@login_required
def load_job_result(id):
    try:
        job = Jobs.query.filter_by(job_id = str(id)).first()
        return render_template("show_result.html", job = job)
    except Exception as e:
        print(e) 
        abort(404)