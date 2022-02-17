from app import db, current_app
from . import user_bp
from flask_login import login_required, login_user, logout_user
from flask import render_template, redirect, url_for, request, flash
from datetime import timedelta

# app.model
from app.model import User

# sqlalchemy
from sqlalchemy.exc import IntegrityError

@user_bp.route("/login")
def login():
    return render_template("login.html")

@user_bp.route("/authenticate", methods=["POST"])
def authenticate():
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        remember = request.form.get("remember")
        next_ = request.args.get("next", "")
        user = User.query.get(email) # loading the user
        if user:
            if user.verify_password(password):
                login_user(user, remember=True if remember=="1" else False, duration=timedelta(days=5))
                if next_ and next!= "":
                    return redirect(next_)
                return redirect(url_for("user.dashboard"))
            else:
                flash(u"Password verification failed.", "danger")
        else:
            flash(u"User not found", 'danger')
        return redirect(url_for("user.login"))
    except:
        flash(u"An error occurred!", "danger")
        return redirect(url_for("user.login"))


@user_bp.route("/signup")
def signup():
    return render_template("signup.html")


@user_bp.route('/register', methods = ["POST"])
def register():
    try:
        name = request.form.get("full_name")
        email = request.form.get("email") 
        password = request.form.get("password")
        user = User(email, name, password)
        db.session.add(user)
        db.session.commit()
        # return to login page with success message
        flash(u'Your account has been registered.', "success")
        return redirect(url_for("user.login"))

    except IntegrityError:
        db.session.rollback()
        flash(u'This email is already registered.', "danger")
        return redirect(request.url)
    
    except Exception as e:
        print(e)
        flash(u'An error occurred!', "danger")
        return redirect(url_for("user.login"))


@user_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("scheduler.html")


@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.login"))