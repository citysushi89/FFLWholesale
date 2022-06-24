from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, StringField, widgets, SubmitField, validators, SelectField, FormField, \
    PasswordField, DateTimeField, DateField, TimeField
from wtforms.validators import DataRequired, Length, URL
import sqlite3
import re
from flask_login import current_user
# Doing this so it can be imported to mani.py and /runreport to decide which wholesalers to run report for
global list_of_wholesalers_selected_by_checkboxes, user_wholesalers_in_db


# Wholesalers who we currently offer functionality for:
# TODO, Update: with more wholesalers when added
wholesalers_list = ["Grice Wholesale", "MGE Wholesale", "Chattanooga Shooting", "Second Amendment Wholesale", "Orion Wholesale", "Zanders"]
TIMES_THE_REPORT_CAN_BE_SENT = ["06:00AM", "07:00AM", "08:00AM", "09:00AM", "10:00AM", "11:00AM", "12:00PM", "01:00PM",
                                "02:00PM", "03:00PM", "04:00PM", "05:00PM", "06:00PM", "07:00PM", "08:00PM", "09:00PM",
                                "10:00PM",]


class MultiCheckBoxField(SelectMultipleField):
    widget = widgets.TableWidget()
    option_widget = widgets.CheckboxInput()


class WholesaleSelectorForm(FlaskForm):
    user_wholesalers = MultiCheckBoxField(choices=wholesalers_list)
    submit = SubmitField("Submit")


class WholesalerLoginForm(FlaskForm):
    wholesale_selector = SelectField("Select the Wholesaler you would like to add", choices=wholesalers_list)
    wholesale_username = StringField(f"Enter your username for selected wholesaler")
    wholesale_password = PasswordField(f"Enter your password for selected wholesaler")

    save_info = SubmitField("Save")
    save_and_run = SubmitField("Save and Run Report")


class RegisterForm(FlaskForm):
   email = StringField("Email", validators=[DataRequired()])
   password = PasswordField("Password", validators=[DataRequired()])
   name = StringField("Name", validators=[DataRequired()])
   company = StringField("Company", validators=[DataRequired()])
   submit = SubmitField("Sign Up")


class HomePageActionSelector(FlaskForm):
    submit_register = SubmitField("Register")
    submit_login = SubmitField("Log In")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


# IP June 4th
class RunReportSelector(FlaskForm):
    # Accessing the db to display the info the user has existing in the system
    connection = sqlite3.connect("userdata.db")
    cursor = connection.cursor()
    # TODO Before Launch: Change the below getting user id to actually get user ID
    # Getting the user id
    current_user = "<User 1>"
    this_user = str(current_user)
    result = re.findall(r'\d+', this_user)
    # Below is required to display the list of wholeaslers, grabs from the db that I used to put in PPs info
    cursor.execute(f"SELECT * FROM wholesaler_login_info WHERE customer_id == {result[0]}")
    results_from_db = cursor.fetchall()
    # Getting count of wholesaler partnership for the user
    number_of_wholesalers_currently_in_system = len(results_from_db)
    # Getting just the wholesaler name into a list to display
    list_of_wholesalers_selected_by_checkboxes = []
    for item in results_from_db:
        list_of_wholesalers_selected_by_checkboxes.append(item[2])
    # Adding an option at the bottom to select All
    list_of_wholesalers_selected_by_checkboxes.append("Select All")

    # Populating check boxes
    #
    user_wholesalers_selected_by_check_boxes = MultiCheckBoxField("Select which wholesalers to include in the report",
                                                choices=list_of_wholesalers_selected_by_checkboxes,
                                                render_kw={'style': 'height: 15px; margin: 10px; width: 65%; list-style: none;'})


    run_report_now = SubmitField("Email me the report now")

    # time_question = TimeField("Select the time you would like to receive the report")
    time_question = wholesale_selector = SelectField("Choose when you would like the report to be sent: ",
                                                     choices=TIMES_THE_REPORT_CAN_BE_SENT)


    run_recurring_report = SubmitField("Set up recurring email report")

