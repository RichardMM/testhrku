
from os import walk
from pathlib import Path
from mimetypes import guess_type
from functools import wraps
from flask import render_template, request,session,Blueprint, redirect, url_for, current_app, send_file, send_from_directory
from myapp import mail,models, db
from flask_mail import Message
from sqlalchemy.exc import OperationalError
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import Email, InputRequired
from flask_login import login_required, login_manager

warehouse_mod = Blueprint('warehouse', import_name=__name__, template_folder='templates')

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

# try implementing this decorator later
def check_db_connection():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func()
            except OperationalError:
                return "We could not connect to the database"
        return wrapper
    return decorator

def check_if_logged_in():
    def decorator(func):
        @wraps(func)
        def login_wrapper(*args, **kwargs):
            if session.get("logged_in", False):
                return func(*args, **kwargs)
            else:
                return redirect(url_for("warehouse.login"))
        return login_wrapper
    return decorator


@warehouse_mod.route('/login/', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method=="GET":
        return render_template("warehouse/login.html", form=login_form)
    elif request.method=="POST":
        if login_form.validate_on_submit():
            session["username"] = login_form.email.data
            session["password"] = login_form.password.data
            user = models.WarehouseUsers.query.filter_by(user_email=session["username"], user_password=session["password"] ).first()

            if session["password"] is None or session["username"] is None or user is None: 
                session["logged_in"] = False
                return "Unauthorised"
            else:
                session["logged_in"] = True
                session["approval_rights"] = user.user_approver_rights
                session["empcode"] = user.user_empcode
                return redirect(url_for("warehouse.home"))
        else:
            return render_template("warehouse/login.html", form=login_form)

@warehouse_mod.route('/', methods=['GET'])
@check_if_logged_in()
def home():
    requisitions = models.WarehouseReqs.query.all()
    return render_template("warehouse/home.html", requisitions=requisitions)

