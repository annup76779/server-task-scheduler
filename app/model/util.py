import os
import re
from functools import wraps
import signal
import smtplib
import subprocess
from threading import Thread
import time

class SchedulingTimeError(Exception):
    def __init__(self,timezone):
        self.timezone = timezone
    def __str__(self):
        return f"DateTime greater than current time. Our timezone - {self.timezone}"

class InvalidServiceRequest(Exception):
    def __init__(self,e):
        self.msg = e
    def __str__(self):
        return f"{self.msg}"

def is_valid_email(email: str):
    exp = re.compile(r"[a-z0-9]+(\.[a-z0-9]+)*@[a-z]+(\.[a-z]+)+")
    email = email.lower()
    match = re.match(exp, email)
    if match:
        return match.group() == email
    else:
        return False


def async_task(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
    return decorator


# scheduler functions
def emailNotification(job, sender, password):
    EMAIL_ADDRESS = sender
    EMAIL_PASS = password

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()  # identify ourselve with smtp server
        smtp.starttls()  # encrypt the traffic

        # now that we have encrypted the traffic we need to rerun
        # the identification with smtp server using ehlo
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASS)

        subject = f"Scan Completed - {job.tool_used}"
        body = "Hey,\n\tThis is to notify that your scan has been completed"\
            f"\nReference name: {job.ref_name}\nJob Id: {job.job_id}\nCompleted at: {job.completedOn.strftime('%Y-%m-%d %H:%M')}"

        msg = f"Subject: {subject}\n\n{body}"

        smtp.sendmail(EMAIL_ADDRESS, job.user, msg)

def processManager(command,path,wait=5):
    print(">>> starting process of process manager ... <<<")
    try:
        with open(path, "w") as f:
            p = subprocess.Popen(command, shell=True, stdout=f)
            time.sleep(wait)
            os.kill(p.pid + 1, signal.SIGINT)
    except KeyboardInterrupt:
        print("Process complete in LINUX.")

def scanServerNikto(job, path):
    processManager(str(job),path,5)
    
def scanWebsiteNikto(job,path):
    processManager(str(job),path,5)

def scanApiZap(job,path):
    print(str(job))
    os.system(str(job)+">"+path)