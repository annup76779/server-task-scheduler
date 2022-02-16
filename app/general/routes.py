# app
import os
import time

from sqlalchemy import select, insert
from app import current_app, db, PATH
from app.general import api
from app.model import Jobs
from app.model.util import SchedulingTimeError, async_task, scanServerNikto, scanWebsiteNikto, scanApiZap
from datetime import datetime

from sqlalchemy.orm import sessionmaker, Session

# flask imports
from flask import redirect, request, url_for, jsonify, flash
from flask_login import login_required, current_user


OUTPUT_PATH = os.path.join(PATH, api.static_folder)

def updateDatabase(engine, job_id, Jobs, path):
    with Session(engine) as session:
        query = select(Jobs).where(Jobs.job_id == job_id)
        res = session.execute(query, (job_id,))
        job = res.first()[0]
        job.setCompleted(path)
        session.commit()

@async_task
def start_active(job,engine, Jobs, path):
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
        updateDatabase(engine, job.job_id, Jobs, path)


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

        start_active(job, db.engine, Jobs, os.path.join(OUTPUT_PATH, f"{job.job_id}.txt"))
        flash("Job added successfully.", "success scheduler_alert_box")
        return redirect(url_for("user.dashboard"))

    except SchedulingTimeError as e:
        flash(f"{e}", "danger scheduler_alert_box")
        return redirect(url_for("user.dashboard"))
        
    except Exception as e:
        print(e)
        flash("Something went wrong.", "danger scheduler_alert_box")
        return redirect(url_for("user.dashboard"))