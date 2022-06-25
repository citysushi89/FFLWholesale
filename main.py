import os

import chardet
from flask import Flask, render_template, url_for, redirect, request, flash, session
from forms import WholesaleSelectorForm, RegisterForm, LoginForm, HomePageActionSelector, RunReportSelector, wholesalers_list
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, StringField, widgets, SubmitField, validators, FieldList, FormField, Form
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, logout_user, current_user, login_required
from flask_bootstrap import Bootstrap
from datetime import datetime
from functions import run_report_based_on_time, run_report_for_testing_purposes, combine_user_csvs


app = Flask(__name__)
bootstrap = Bootstrap(app)

# Backend functionality
# TODO: MGE - spitting "Our Price $xxx" and "Sale Price $xxx" into the same field in the CSV

# UI/Front End Functionality:
# TODO 2: Homepage
    # TODO 2.1: extend footer to other html files

# For launch
# TODO: launch actual site using free github to start

# TODO: NEED TO UPDATE TO SOMETHING REALLY SECRET LATER
SECRET_KEY = os.getenv("SECRET_KEY")
app.config["SECRET_KEY"] = SECRET_KEY

# CONNECT TO DB - Production
# uri = os.getenv("DATA_BASE_URL")
# print(uri)
# if uri.startswith("postgres://"):
#     uri = uri.replace("postgres://", "postgresql://", 1)
# app.config['SQLALCHEMY_DATABASE_URI'] = uri
sample = os.getenv("DATABASE_URL1")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATA_BASE_URL", "sqlite:///userdata.db")

print(sample)


# CONNECT To DB development - Production
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Creating Login functionality
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


##CONFIGURE TABLES
@app.before_first_request
def create_tables():
    db.create_all()


# Creating Databases
# Create the User Table
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    company = db.Column(db.String(100))

# TODO, update: when adding new wholesalers, need to update wholesaler login info on /wholesaleloginpage when
# Creating the Database of the login info
class WholesalerLoginInfo(db.Model):
    __tablename__ = "wholesaler_login_info"
    id = db.Column(db.Integer, primary_key=True)

    #Creates the foreign key, "users.id" the users refers to the tablename of User
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    wholesaler_name = db.Column(db.String(250), nullable=False)
    wholesaler_username = db.Column(db.String(250), nullable=False)
    wholesaler_password = db.Column(db.String(250), nullable=False)


class UserReportSelections(db.Model):
    __tablename__ = "user_report_selections"
    id = db.Column(db.Integer, primary_key=True)

    # Creates the foreign key, "users.id" the users refers to the tablename of User
    # TODO Before Launch, currently allows unlimited user_ids (foreign keys) inputted,
    #  need to reduce to one for base plan (tried unique key like email field in other db and didn't work)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    time_selected = db.Column(db.String(250), nullable=False)
    days_selected = db.Column(db.String(500), nullable=False)
    wholesalers_selected = db.Column(db.String(1000), nullable=False)

# Need these lines so that user_wholesalers can go from the route '/' to the form WholesalerLoginForm in forms.py
global grice_wholesale_username, grice_wholesale_password, mge_wholesale_username, mge_wholesale_password


# run_report_for_testing_purposes()
# Page to select to login or register
# Needs to stay above the wholesaler login and running report page
@app.route('/', methods=["POST", "GET"])
def home_page_selections():
    form = HomePageActionSelector()
    if request.form.get("submit_register") == "Register":
        return redirect(url_for("register"))
    if request.form.get("submit_login") == "Log In":
        return redirect(url_for("login"))
    return render_template("index.html", form=form, logged_in=current_user.is_authenticated)


# Page to Login
@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Find user by email entered
        user = User.query.filter_by(email=email).first()

        # If email does not exist in database
        if not user:
            flash("That email does not exist in our database, please try again.")
            return redirect(url_for("login"))

        # Check stored password has against entered password hashed.
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for("login"))

        # Email and password both exist and match:
        else:
            login_user(user)
            return redirect(url_for("run_report"))

    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)


# NOT USED ANYMORE
# Page to select which wholesalers you are partnered with ... see when registered then only if selected if logged in
@app.route('/wholesalerselectorpage', methods=["POST", "GET"])
def wholesale_selector_page():
    form = WholesaleSelectorForm()
    # if request.method == "POST":
    if form.validate_on_submit():
        user_wholesalers = request.form.getlist("user_wholesalers")
        print(user_wholesalers)
        return redirect(url_for("wholesale_login_page", form=form,  user_wholesalers=user_wholesalers))
    return render_template("wholesalerselectorpage.html", form=form, logged_in=current_user.is_authenticated)


# NOT CURRENTLY USED: Page to put in their username/password combos for the different wholesalers
@app.route('/wholesaleloginpage', methods=["POST", "GET"])
def wholesale_login_page():
    from forms import WholesalerLoginForm
    form = WholesalerLoginForm()

    # If user hits Save button
    if request.form.get("save_info") == "Save":
        # Send flash messsage
        flash(f"You submitted your information for {form.wholesale_selector.data}!")
        new_wholesaler_login_info = WholesalerLoginInfo(
            wholesaler_name=form.wholesale_selector.data,
            wholesaler_username=form.wholesale_username.data,
            wholesaler_password=form.wholesale_password.data,
            customer_id=current_user.id
        )
        db.session.add(new_wholesaler_login_info)
        db.session.commit()
        return redirect(url_for("wholesale_login_page", form=form))

    # If user hits Save and Run Report button
    if request.form.get("save_and_run") == "Save and Run Report":
        # Send flash messsage
        flash(f"You submitted your information for {form.wholesale_selector.data}!")
        new_wholesaler_login_info = WholesalerLoginInfo(
            wholesaler_name=form.wholesale_selector.data,
            wholesaler_username=form.wholesale_username.data,
            wholesaler_password=form.wholesale_password.data,
            customer_id=current_user.id
        )
        db.session.add(new_wholesaler_login_info)
        db.session.commit()
        return redirect(url_for("run_report", form=form))
    return render_template("wholesaleloginpage.html", form=form, logged_in=current_user.is_authenticated)


# Page to select run report or save
@app.route('/runreport', methods=["POST", "GET"])
# Marking with decorator that checks if they are a current user
@login_required
def run_report():
    # TODO: Most of this functionality should be obselete once report to run regularly is set up
    form = RunReportSelector()

    if request.form.get("run_report_now") == "Email me the report now":
        user_selected_wholesalers_for_report = []
        user_selected_wholesalers_for_report_string = ""
        for item in form.user_wholesalers_selected_by_check_boxes.data:
            user_selected_wholesalers_for_report.append(item)
            user_selected_wholesalers_for_report_string += item + ", "
        flash(f"You have selected: {user_selected_wholesalers_for_report_string} for your report. Please allow 5 minutes for the request to be processed and sent.")
        # Combining selected CSVs
        from functions import combine_user_csvs, send_email
        combine_user_csvs(user_selected_wholesalers_for_report)
        # Need to get user email to pass into send_email
        import sqlite3
        import re
        connection = sqlite3.connect("userdata.db")
        cursor = connection.cursor()
        this_user = str(current_user)
        result = re.findall(r'\d+', this_user)
        cursor.execute(f"SELECT * FROM users WHERE id == {result[0]}")
        results_from_db = cursor.fetchall()
        user_email = results_from_db[0][1]
        # Need to use try, except because reports only run for 6am-10pm send times
        # TODO later, need to use the actual user number to save and store and send file
        try:
            # Need to get the date to find the right document
            now = datetime.now()
            todays_date = now.strftime("%I%p_%d%b%y")
            filename = open(r"C:/Users/OwenDocuments/Personal Info/Independent Courses/Python Learning/fflwholesalerproductpps/Data/Users/1/wholesaler_data.csv", encoding="utf-8")
            send_email(filename, user_email)
        except FileNotFoundError:
            # Need to get the date to find the right document
            now = datetime.now()
            # picking the 10pm one so that it is the most up to date document as this will occur at night
            todays_date = now.strftime("10PM_%d%b%y")
            send_email(r"C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/fflwholesalerproductpps/Data/Users/1/wholesaler_data.csv", user_email)

    elif request.form.get("run_recurring_report") == "Set up recurring email report":
        time_user_selected = form.time_question.data
                # Adding to a list and a string of user selected wholesalers
        # Need the list for Python, need the string to input into the database
        user_selected_wholesalers_for_report = []
        user_selected_wholesalers_for_report_string = ""
        for item in form.user_wholesalers_selected_by_check_boxes.data:
            user_selected_wholesalers_for_report.append(item)
            user_selected_wholesalers_for_report_string += item + ", "
        flash(f"You have selected: {user_selected_wholesalers_for_report_string} for your report. "
              f"You will be emailed daily at {time_user_selected} with the most up-to-date wholesaler information.")
        # Combining selected CSVs
        from functions import combine_user_csvs
        combine_user_csvs(user_selected_wholesalers_for_report)
        # NEW 14June - Trying to actually add info to db


        # Adding data to the database
        # TODO Before Launch, currently allows unlimited user_ids (foreign keys) inputted,
        #  need to reduce to one for base plan
        new_user_recurring_preferences = UserReportSelections(
            customer_id=current_user.id,
            time_selected=form.time_question.data,
            # Days selected will be every day, will eventually add premium tier for certain days/times
            days_selected="Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday",
            wholesalers_selected=user_selected_wholesalers_for_report_string
        )
        db.session.add(new_user_recurring_preferences)
        db.session.commit()
        # TODO: Need to take inputs and add them to the database class UserReportSelections(db.Model):

    # Below searches list user_inputted, and filters through the list of individual wholeasler CSVs to compile
    # to a customer report for the user
    # import pandas as pd
    # # TODO, UPDATE: as new wholesalers are added, need to be included below
    # LIST_OF_WHOLESALE_CSVS = ["ChattanoogaShooting/chattanooga_shooting_data.csv",
    #         "SecondAmendmentWholesale/second_amendment_wholesale_data.csv",
    #         "MGEWholesale/mge_wholesale_data.csv",
    #         "GriceWholesale/grice_wholesale_data.csv",
    #         ]
    # list_specific_to_user_to_compile_csv_with = []
    #
    # for item in user_selected_wholesalers_for_report:
    #     if item in LIST_OF_WHOLESALE_CSVS:
    #         list_specific_to_user_to_compile_csv_with.append(item)
    #
    # for item in list_specific_to_user_to_compile_csv_with:
    #     data = pd.read_csv(item, encoding_errors='replace')
    #     data.to_csv("all_wholesaler_data.csv", index=False, header=False, mode="a")

    return render_template("runreport.html", form=form, logged_in=current_user.is_authenticated)


# Page to register a new user
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

       #If user's email already exists
       if User.query.filter_by(email=form.email.data).first():
           # Send flash messsage
           flash("You've already signed up with that email, log in instead!")
           # Redirect to /login route.
           return redirect(url_for("login"))

       hash_and_salted_password = generate_password_hash(
           form.password.data,
           method="pbkdf2:sha256",
           salt_length=8
       )

       new_user = User(
           email=form.email.data,
           name=form.name.data,
           password=hash_and_salted_password,
           company=form.company.data
       )
       db.session.add(new_user)
       db.session.commit()
       login_user(new_user)
       return redirect(url_for("wholesale_selector_page"))
    return render_template("register.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/about')
def about():
    return render_template("about.html", logged_in=current_user.is_authenticated)


@app.route('/contact')
def contact():
    return render_template("contact.html", logged_in=current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home_page_selections"))


# Needs to go at the bottom!
if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000)
