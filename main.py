import os
import chardet
from flask import Flask, render_template, url_for, redirect, request, flash, session, send_file, send_from_directory
from forms import WholesaleSelectorForm, RegisterForm, LoginForm, HomePageActionSelector, RunReportSelector, \
    wholesalers_list, RunReportDownload
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, StringField, widgets, SubmitField, validators, FieldList, FormField, Form
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, logout_user, current_user, login_required
from flask_bootstrap import Bootstrap
from functions import run_report_based_on_time, run_report_for_testing_purposes, combine_user_csvs, \
    download_file_from_bucket
# Below imports a module that outputs more info in Heroku logs
import logging

app = Flask(__name__)
bootstrap = Bootstrap(app)

try:
    SECRET_KEY = os.getenv("SECRET_KEY")
except:
    SECRET_KEY = os.environ["SECRET_KEY"]
app.config["SECRET_KEY"] = SECRET_KEY

# CONNECT TO DB - Production
# uri = os.getenv("DATA_BASE_URL")
# print(uri)
# if uri.startswith("postgres://"):
#     uri = uri.replace("postgres://", "postgresql://", 1)
# app.config['SQLALCHEMY_DATABASE_URI'] = uri
sample = os.getenv("DATABASE_URL1")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATA_BASE_URL", "sqlite:///userdata.db")

# CONNECT To DB development - Production
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Setting up the logger to get more detailer info from Heroku logs
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


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

# Creating the Database of the login info
class WholesalerLoginInfo(db.Model):
    __tablename__ = "wholesaler_login_info"
    id = db.Column(db.Integer, primary_key=True)

    #Creates the foreign key, "users.id" the users refers to the tablename of User
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    wholesaler_name = db.Column(db.String(250), nullable=False)
    wholesaler_username = db.Column(db.String(250), nullable=False)
    wholesaler_password = db.Column(db.String(250), nullable=False)


# Need these lines so that user_wholesalers can go from the route '/' to the form WholesalerLoginForm in forms.py
global grice_wholesale_username, grice_wholesale_password, mge_wholesale_username, mge_wholesale_password

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
    import sqlite3
    # OLD BROKEN IN HEROKU EMAIL FORM
    # form = RunReportSelector()
    # NEW FORM TO JUST DOWNLOAD
    form = RunReportDownload()

    # NEW aug 2
    connection = sqlite3.connect("wholesaler_data.db")
    cursor = connection.cursor()
    print("Connected to the database")

    # Get data from table "mge"
    cursor.execute("SELECT * FROM mge")
    answer = cursor.fetchall()
    number_of_rows_in_answer = len(answer)
    print(number_of_rows_in_answer)
    # End New


    if request.form.get("download_report") == "Download Report":
        user_selected_wholesalers_for_report = []
        user_selected_wholesalers_for_report_string = ""
        for item in form.user_wholesalers_selected_by_check_boxes.data:
            user_selected_wholesalers_for_report.append(item)
            user_selected_wholesalers_for_report_string += item + ", "
        flash(f"You have selected: {user_selected_wholesalers_for_report_string} for your report, it will download shortly.")
        # Accessing the google cloud
        # TODO, may need to change below to the other environ
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "google_service_key.json"

        # Getting the date the report is saved to files do not overlap
        from datetime import datetime
        now = datetime.now()
        date_report_saved = now.strftime("%d%b%y")

        # TODO before upload: make users in filenaming convention the actual user (uncomment 2 below lines and delete the third)
        # from functions import get_current_user
        # this_user = get_current_user()
        user_number = 1
        # user_reports needs to stay, it will keep the user reports in a folder with folders for individual users
        file_name = f"user_reports/{user_number}/wholesaler_data{date_report_saved}.csv"
        destination_blob_name = f"user_reports/{user_number}/wholesaler_data{date_report_saved}.csv"

        list_of_report_data = []
        # Appending the list of report data based on user input
        for item in user_selected_wholesalers_for_report:
            if item == "Grice Wholesale":
                grice_filename = "wholesale_reports/grice_wholesale_data.csv"
                list_of_report_data.append(grice_filename)
            elif item == "MGE Wholesale":
                # connecting to the database
                connection = sqlite3.connect("wholesaler_data.db")
                cursor = connection.cursor()
                print("Connected to the database")

                # Get data from table "mge"
                cursor.execute("SELECT * FROM mge")
                answer = cursor.fetchall()

                mge_filename = "wholesale_reports/mge_wholesale_data.csv"
                list_of_report_data.append(mge_filename)
            elif item == "Chattanooga Shooting":
                chattanooga_filename = "wholesale_reports/chattanooga_shooting_data.csv"
                list_of_report_data.append(chattanooga_filename)
            elif item == "Second Amendment Wholesale":
                second_filename = "wholesale_reports/second_amendment_wholesale_data.csv"
                list_of_report_data.append(second_filename)
            elif item == "Orion Wholesale":
                orion_filename = "wholesale_reports/orion_wholesale_data.csv"
                list_of_report_data.append(orion_filename)
            elif item == "Zanders":
                zanders_filename = "wholesale_reports/zanders_data.csv"
                list_of_report_data.append(zanders_filename)
            # For the select all function
            elif item == "Select All":
                grice_filename = "wholesale_reports/grice_wholesale_data.csv"
                list_of_report_data.append(grice_filename)

                mge_filename = "wholesale_reports/mge_wholesale_data.csv"
                list_of_report_data.append(mge_filename)

                chattanooga_filename = "wholesale_reports/chattanooga_shooting_data.csv"
                list_of_report_data.append(chattanooga_filename)

                second_filename = "wholesale_reports/second_amendment_wholesale_data.csv"
                list_of_report_data.append(second_filename)

                orion_filename = "wholesale_reports/orion_wholesale_data.csv"
                list_of_report_data.append(orion_filename)

                zanders_filename = "wholesale_reports/zanders_data.csv"
                list_of_report_data.append(zanders_filename)


    return render_template("runreport.html",
                           form=form,
                           logged_in=current_user.is_authenticated,
                           answer=answer,
                           count=number_of_rows_in_answer)


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

# @app.route('/download')
# def download_report():
#         return send_file(new_download, attachment_filename="Wholesaler Report.csv")
#
#     return render_template("runreport.html", form=form, logged_in=current_user.is_authenticated)


# Needs to go at the bottom!
if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000)
