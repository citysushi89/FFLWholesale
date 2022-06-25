from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time, os
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions
import chardet

def open_url(URL, driver):
    driver.get(URL)
    time.sleep(.2)
    driver.maximize_window()
    time.sleep(1)


def click_login_button(location, driver):
    # Clicking Login
    try:
        login_button = driver.find_element(By.XPATH, location)
    except:
        login_button = driver.find_element(By.CLASS_NAME, location)
    login_button.click()
    time.sleep(.5)


def fill_in_login_boxes(EMAIL, PASSWORD, email_field_id, password_field_id, sign_in_button_id, driver):
    email_field = driver.find_element(By.ID, email_field_id)
    email_field.send_keys(EMAIL)
    time.sleep(1)
    password_field = driver.find_element(By.ID, password_field_id)
    password_field.send_keys(PASSWORD)
    time.sleep(1)
    try:
        sign_in_button = driver.find_element(By.ID, sign_in_button_id)
    except:
        sign_in_button = driver.find_element(By.CLASS_NAME, sign_in_button_id)
    sign_in_button.click()
    time.sleep(1)


def click_firearms_tab(tab_location, firearms_tab_click_location, driver):
    departments_tab = driver.find_element(By.XPATH, tab_location)
    a = ActionChains(driver)
    a.move_to_element(departments_tab).perform()
    time.sleep(.5)
    # Clicking to go to the firearms page
    firearms_tab = driver.find_element(By.XPATH, firearms_tab_click_location)
    firearms_tab.click()
    time.sleep(.5)


def maximize_page_size(drop_down_location_id, max_option_x_path, driver, a):
    # quantity_shown_per_page_dropdown = driver.find_element(By.ID, drop_down_location_id)
    a = ActionChains(driver)
    # a.move_to_element(quantity_shown_per_page_dropdown).perform()
    time.sleep(1)
    # Clicking to go to 100 per page
    max_per_page = driver.find_element(By.XPATH, max_option_x_path)
    max_per_page.click()
    time.sleep(1)


def convert_selenium_objects_to_list(input_list):
    output_list = []
    for item in input_list:
        item_text = item.text
        # Below is for Second Amendment Wholesale, but shouldn't interfere with others, if it does just do in the .py
        # for Second
        if "Special Price" in item_text:
            new_string = item_text.split("\n")
            item_text = new_string[1]
        output_list.append(item_text)
        if item_text == "":
            output_list.remove(item_text)
    return output_list

def convert_selenium_objects_to_list_zanders_cost(input_list):
    output_list = []
    # compiles everything into the output list, then filtires the output list (as it is now in text)
    # to get ride of regular/sale price for same item
    for item in input_list:
        item_text = item.text
        output_list.append(item_text)
        if item == "":
            output_list.remove(item_text)
    for item in output_list:
        if "Special Price" in item:
            item_index = output_list.index(item)
            old_price = output_list[item_index + 1]
            output_list.remove(old_price)
            # Sale price currently looks like this: "Special Price $114.95"
            # whereas normal price is "$114.95"
            # TODO: Should I remove the text special price?
    return output_list

def convert_selenium_objects_to_list_of_links(input_list):
    output_list = []
    for item in input_list:
        new_link = item.get_attribute("href")
        output_list.append(new_link)
        try:
            if "None" in new_link:
                output_list.remove(item)
        except TypeError:
            pass
    return output_list


def get_current_user():
    pass
    # SHOULD NOT NEED DUE TO:
    # from flask_login import UserMixin, login_user, LoginManager, logout_user, current_user,
    #
    # import sqlite3
    # import re
    #
    # # TODOL
    # # Accessing the db to display the info the user has existing in the system
    # connection = sqlite3.connect("userdata.db")
    # cursor = connection.cursor()
    # # TODO Before Launch: Change the below getting user id to actually get user ID
    # # Getting the user id
    # current_user = "<User 1>"
    # this_user = str(current_user)
    # return this_user


def send_email(filename, to_address):
    from datetime import datetime
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.application import MIMEApplication
    import os
    from os.path import basename


    # Setting up time for email subject
    now = datetime.now()

    hour_formatted = now.strftime("%I%p")
    date_formatted = now.strftime("%x")

    subject = f"Subject: Wholesaler Helper Report on {date_formatted} at {hour_formatted} "
    content = "Please see attached for your customized report."
    from_address = "bepisorconkconsumer@gmail.com"
    # TODO Need to get to email from database probably??
    PASSWORD = "tpalqirtcxuctnhw"

    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["Subject"] = subject
    body = MIMEText(content, "plain")
    msg.attach(body)

    # TODO: Below may need changing if send_email is called too long after the report is ran...
    #  unsure rn how else to refer to the specific file name as it changes
    date_report_saved = now.strftime("%I%p_%d%b%y")

    # TODO: uncomment below, the second filename_csv is just for testing
    # filename_csv = f"Data/Users/all_wholesaler_data_{date_report_saved}.csv"
    # TODO: Below is just for testing, remove later

    filename_csv = filename
    with open(filename_csv, "r") as f_csv:
        attachment_csv = MIMEApplication(f_csv.read(), Name=basename(filename_csv))
        attachment_csv["Content-Disposition"] = "attachment; filename={}".format(basename(filename_csv))
    msg.attach(attachment_csv)


    server = smtplib.SMTP("smtp.gmail.com", port=587)
    server.starttls()
    server.login(from_address, password=PASSWORD)
    server.send_message(msg, from_addr=from_address, to_addrs=to_address)

# Converts current_user from "<User 1>" to "1"
def get_just_user_decimal():
    from main import current_user
    string_current_user = str(current_user)
    current_user_list = []
    for item in string_current_user:
        if item == "<":
            pass
        elif item == "U":
            pass
        elif item == "s":
            pass
        elif item == "e":
            pass
        elif item == "r":
            pass
        elif item == " ":
            pass
        elif item == ">":
            pass
        else:
            current_user_list.append(item)
    user_number = current_user_list[0]
    return user_number

def combine_user_csvs(user_selected_wholesalers_for_report):
    import pandas as pd
    # Converting customer_id into a form (just the digits)that will store in a file
    user_number = get_just_user_decimal()

    list_specific_to_user_to_compile_csv_with = []
    # TODO, UPDATE: as new wholesalers are added, need to be included below the for loop
    # TODO Before Launch: Change the below getting user id to actually get user ID and store in a folder for that user
    test_list = []
    # Grabbing the CSVs of the selected wholesalers
    for item in user_selected_wholesalers_for_report:
        if item == "Grice Wholesale":
            grice_new_file = "C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/fflwholesalerproductpps/Data/WholesalerReports/grice_wholesale_data.csv"
            grice_read_file = pd.read_csv(grice_new_file)
            test_list.append(grice_read_file)
        elif item == "MGE Wholesale":
            mge_new_file = "C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/fflwholesalerproductpps/Data/WholesalerReports/mge_wholesale_data.csv"
            mge_read_file = pd.read_csv(mge_new_file)
            test_list.append(mge_read_file)
        elif item == "Chattanooga Shooting":
            chattanooga_new_file = "C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/fflwholesalerproductpps/Data/WholesalerReports/chattanooga_shooting_data.csv"
            chattanooga_read_file = pd.read_csv(chattanooga_new_file)
            test_list.append(chattanooga_read_file)
        elif item == "Second Amendment Wholesale":
            second_new_file = "C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/fflwholesalerproductpps/Data/WholesalerReports/second_amendment_wholesale_data.csv"
            second_read_file = pd.read_csv(second_new_file)
            test_list.append(second_read_file)
        elif item == "Orion Wholesale":
            orion_new_file = "C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/fflwholesalerproductpps/Data/WholesalerReports/orion_wholesale_data.csv"
            orion_read_file = pd.read_csv(orion_new_file)
            test_list.append(orion_read_file)
        elif item == "Zanders":
            zanders_new_file = r"C:\Users\Owen\Documents\Personal Info\Independent Courses\Python Learning\fflwholesalerproductpps\Data\WholesalerReports\zanders_data.csv"
            zanders_read_file = pd.read_csv(zanders_new_file)
            test_list.append(zanders_read_file)
        elif item == "Select All":
            grice_new_file = "C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/fflwholesalerproductpps/Data/WholesalerReports/grice_wholesale_data.csv"
            grice_read_file = pd.read_csv(grice_new_file)
            test_list.append(grice_read_file)

            mge_new_file = "C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/fflwholesalerproductpps/Data/WholesalerReports/mge_wholesale_data.csv"
            mge_read_file = pd.read_csv(mge_new_file)
            test_list.append(mge_read_file)

            chattanooga_new_file = "C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/fflwholesalerproductpps/Data/WholesalerReports/chattanooga_shooting_data.csv"
            chattanooga_read_file = pd.read_csv(chattanooga_new_file)
            test_list.append(chattanooga_read_file)

            second_new_file = "C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/fflwholesalerproductpps/Data/WholesalerReports/second_amendment_wholesale_data.csv"
            second_read_file = pd.read_csv(second_new_file)
            test_list.append(second_read_file)

            orion_new_file = "C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/fflwholesalerproductpps/Data/WholesalerReports/orion_wholesale_data.csv"
            orion_read_file = pd.read_csv(orion_new_file)
            test_list.append(orion_read_file)

            zanders_new_file = r"C:\Users\Owen\Documents\Personal Info\Independent Courses\Python Learning\fflwholesalerproductpps\Data\WholesalerReports\zanders_data.csv"
            zanders_read_file = pd.read_csv(zanders_new_file)
            test_list.append(zanders_read_file)

    this_user = get_current_user()
    # Getting datetime for filename so it does not keep appending itself
    from datetime import datetime
    now = datetime.now()
    date_report_saved = now.strftime("%d%b%y")

    print(this_user)
    data = pd.concat(test_list)
    data.to_csv(rf"C:\Users\Owen\Documents\Personal Info\Independent Courses\Python Learning\fflwholesalerproductpps\Data\Users\{user_number}\wholesaler_data{date_report_saved}.csv", index=False)


    # return f"Data/Users/{user_number}/all_wholesaler_data_{date_report_saved}.csv"
    # return f"Data/Users/1/all_wholesaler_data_{date_report_saved}.csv"


def run_report_for_testing_purposes():
    from MGEWholesale.mge_wholesale_functionality import get_mge_wholesale_data
    get_mge_wholesale_data()
    from GriceWholesale.grice_wholesale_functionality import get_grice_wholesale_data
    get_grice_wholesale_data()
    from ChattanoogaShooting.chattanooga_shooting_functionality import get_chattanooga_shooting_data
    get_chattanooga_shooting_data()
    from SecondAmendmentWholesale.second_amendment_wholesale_functionality import get_second_amendment_wholesale_data
    get_second_amendment_wholesale_data()
    from OrionWholesale.orion_wholesale_functionality import get_orion_wholesale_data
    get_orion_wholesale_data()
    from Zanders.zanders_functionality import get_zanders_data
    get_zanders_data()


def run_report_based_on_time():
    from datetime import datetime
    # Getting the current time and formatting to test
    now = datetime.now()
    # Getting the time in the correct format
    now_formatted_hour_and_minutes = now.strftime("%I:%M")
    minute_digits_to_run_report = 40
    hour_digit_to_run_report = []
    for i in range(5, 22):
        i_string = str(i)
        new_digit = i_string.zfill(2)
        hour_digit_to_run_report.append(new_digit)

    # Connecting each hour and minute to run report
    list_of_times_to_run_program = []
    for i in range(0, len(hour_digit_to_run_report)):
        list_of_times_to_run_program.append(str(hour_digit_to_run_report[i]) + ":" + str(minute_digits_to_run_report))

    # TODO update: with new wholesalers as added
    # If time.now is in the list, runs the reports
    if now_formatted_hour_and_minutes in list_of_times_to_run_program:
        from MGEWholesale.mge_wholesale_functionality import get_mge_wholesale_data
        get_mge_wholesale_data()
        from GriceWholesale.grice_wholesale_functionality import get_grice_wholesale_data
        get_grice_wholesale_data()
        from ChattanoogaShooting.chattanooga_shooting_functionality import get_chattanooga_shooting_data
        get_chattanooga_shooting_data()
        from SecondAmendmentWholesale.second_amendment_wholesale_functionality import get_second_amendment_wholesale_data
        get_second_amendment_wholesale_data()
        from OrionWholesale.orion_wholesale_functionality import get_orion_wholesale_data
        get_orion_wholesale_data()
        from Zanders.zanders_functionality import get_zanders_data
        get_zanders_data()