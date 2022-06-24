import csv
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.common.keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions

from functions import open_url, click_login_button, fill_in_login_boxes, click_firearms_tab, maximize_page_size, \
    convert_selenium_objects_to_list, convert_selenium_objects_to_list_of_links


def get_orion_wholesale_data():
    s = Service("C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/chromedriver")
    driver = webdriver.Chrome(service=s)
    a = ActionChains(driver)

    # Setting up connection to driver and site
    URL = "https://www.orionfflsales.com/"

    EMAIL = os.environ["EMAIL"]
    PASSWORD = os.environ["PASSWORD"]

    # Setting up the iterations, using formulas from functions.py
    open_url(URL, driver)
    time.sleep(.5)
    click_login_button(location="log-in-link", driver=driver)

    # Logging in
    email_field_id = "Email"
    password_field_id = "Password"
    sign_in = "login-button"
    fill_in_login_boxes(EMAIL, PASSWORD, email_field_id, password_field_id, sign_in, driver)

    # Clicking the GUNS on the header
    guns_tab_xpath = "/html/body/div[2]/div/div[2]/div/nav/div/div[2]/ul/li[1]/a"
    click_firearms_tab(guns_tab_xpath, guns_tab_xpath, driver)

    # Clicking the Handguns under GUNS on the header
    handguns_xpath = "/html/body/div[2]/div/div[2]/div/nav/div/div[2]/ul/li[1]/div/div/ul/li[1]/a"
    click_firearms_tab(handguns_xpath, handguns_xpath, driver)
    time.sleep(2)

    # Getting page size to 500 per page
    TIME_TO_SLEEP_MAX_PAGE_SIZE = 55
    PAGE_RELOAD_SLEEP = 25
    per_page_500_xpath = "/html/body/div[2]/div/div[3]/div[3]/main/div[2]/table/tbody/tr/td/div/div[3]/span[2]/a[5]"
    maximize_page_size(per_page_500_xpath, per_page_500_xpath, driver, "")
    time.sleep(TIME_TO_SLEEP_MAX_PAGE_SIZE)


    # Setting up the master list and iteration counter
    global master_list_handguns
    master_list_handguns = []

    # Setting up the iteration items, can adjust later, or just leave if try/except works
    iteration = 0

    # Loop currently only set up for 2 iterations, 500 items per page
    while iteration < 2:
        time.sleep(PAGE_RELOAD_SLEEP)
        # Gets firearm_type, converts into a list
        try:
            firearm_type = driver.find_elements(By.CLASS_NAME, "Name")
            firearm_type_list = convert_selenium_objects_to_list(input_list=firearm_type)
        except selenium.common.exceptions.StaleElementReferenceException:
            time.sleep(4)
            firearm_type = driver.find_elements(By.CLASS_NAME, "Name")
            firearm_type_list = convert_selenium_objects_to_list(input_list=firearm_type)

        # Gets Cost
        cost = driver.find_elements(By.CLASS_NAME, "variant-price")
        try:
            cost_list = convert_selenium_objects_to_list(input_list=cost)
        except selenium.common.exceptions.StaleElementReferenceException:
            time.sleep(5)
            cost_list = convert_selenium_objects_to_list(input_list=cost)

        # Gets link
        link_list = []
        for i in range(1, len(firearm_type_list) + 1):
            link = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div[3]/div[3]/main/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[{i}]/div/div[2]/a")
            try:
                actual_link = link.get_attribute("href")
            except selenium.common.exceptions.StaleElementReferenceException:
                time.sleep(4)
                actual_link = link.get_attribute("href")
            # except selenium.common.exceptions.StaleElementReferenceException:
            #     pass
            link_list.append(actual_link)
        time.sleep(3)


        # Gets Stock Status
        stock_status = driver.find_elements(By.CLASS_NAME, "add-to-cart")
        stock_status_list = convert_selenium_objects_to_list(input_list=stock_status)
        # Need to do the below because stock_status_list looks like ['Out of Stock', '0', 'Add to Cart', '10+'...
        new_stock_status_list = []
        for i in range(0, len(stock_status_list), 2):
            new_stock_status = stock_status_list[i] + " " + stock_status_list[i + 1]
            new_stock_status_list.append(new_stock_status)

        # Compiling into a master list:
        time.sleep(1)
        length_of_a_list = len(firearm_type_list)
        for i in range(0, length_of_a_list):
            place_holder_list = []
            place_holder_list.append(firearm_type_list[i])
            place_holder_list.append(cost_list[i])
            place_holder_list.append(link_list[i])
            place_holder_list.append(new_stock_status_list[i])
            master_list_handguns.append(place_holder_list)
        print(f"hg: {master_list_handguns}")
        print(len(master_list_handguns))
        # Below is necessary because the next page arrow moves based on what page you are on
        time.sleep(2)

        iteration += 1
        if iteration == 1:
            print("If handguns triggered")
            try:
                next_page_button = driver.find_element(By.XPATH,
                                                       "/html/body/div[2]/div/div[3]/div[3]/main/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/a[3]")
            except selenium.common.exceptions.NoSuchElementException:
                time.sleep(5)
                next_page_button = driver.find_element(By.XPATH,
                                                       "/html/body/div[2]/div/div[3]/div[3]/main/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/a[3]")
            time.sleep(3)
            next_page_button.click()
            time.sleep(TIME_TO_SLEEP_MAX_PAGE_SIZE)
        elif iteration >= 2:
            time.sleep(2)
            print(len(master_list_handguns))
            print("Elif hand guns triggered")
            break
        else:
            time.sleep(2)
            print(len(master_list_handguns))
            print("Else hand guns triggered")
            break

    # Clicking the GUNS on the header
    guns_tab_xpath = "/html/body/div[2]/div/div[2]/div/nav/div/div[2]/ul/li[1]/a"
    click_firearms_tab(guns_tab_xpath, guns_tab_xpath, driver)

    # Clicking the Handguns under GUNS on the header
    handguns_xpath = "/html/body/div[2]/div/div[2]/div/nav/div/div[2]/ul/li[1]/div/div/ul/li[2]/a"
    click_firearms_tab(handguns_xpath, handguns_xpath, driver)
    time.sleep(2)

    # Getting page size to 500 per page
    per_page_500_xpath = "/html/body/div[2]/div/div[3]/div[3]/main/div[2]/table/tbody/tr/td/div/div[3]/span[2]/a[5]"
    maximize_page_size(per_page_500_xpath, per_page_500_xpath, driver, "")
    time.sleep(TIME_TO_SLEEP_MAX_PAGE_SIZE)

    # Setting up the iteration items, can adjust later, or just leave if try/except works
    total_items = 1
    items_shown = 0
    iteration = 0

    global master_list_long_guns
    master_list_long_guns = []

    while iteration < 2:
        time.sleep(PAGE_RELOAD_SLEEP)
        # Gets firearm_type, converts into a list
        try:
            firearm_type = driver.find_elements(By.CLASS_NAME, "Name")
            firearm_type_list = convert_selenium_objects_to_list(input_list=firearm_type)
        except selenium.common.exceptions.StaleElementReferenceException:
            time.sleep(4)
            firearm_type = driver.find_elements(By.CLASS_NAME, "Name")
            firearm_type_list = convert_selenium_objects_to_list(input_list=firearm_type)

        # Gets Cost
        cost = driver.find_elements(By.CLASS_NAME, "variant-price")
        try:
            cost_list = convert_selenium_objects_to_list(input_list=cost)
        except selenium.common.exceptions.StaleElementReferenceException:
            time.sleep(5)
            cost_list = convert_selenium_objects_to_list(input_list=cost)

        # Gets link
        link_list = []
        for i in range(1, len(firearm_type_list) + 1):
            link = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div[3]/div[3]/main/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[{i}]/div/div[2]/a")
            try:
                actual_link = link.get_attribute("href")
            except selenium.common.exceptions.StaleElementReferenceException:
                time.sleep(6)
                actual_link = link.get_attribute("href")
            link_list.append(actual_link)
        time.sleep(3)

        # Gets Stock Status
        number_of_items_on_page = len(firearm_type_list)
        stock_status = driver.find_elements(By.CLASS_NAME, "add-to-cart")
        stock_status_list = convert_selenium_objects_to_list(input_list=stock_status)
        # Need to do the below because stock_status_list looks like ['Out of Stock', '0', 'Add to Cart', '10+'...
        new_stock_status_list = []
        for i in range(0, len(stock_status_list), 2):
            new_stock_status = stock_status_list[i] + " " + stock_status_list[i + 1]
            new_stock_status_list.append(new_stock_status)

        # Compiling into a master list:
        time.sleep(1)
        length_of_a_list = len(firearm_type_list)
        for i in range(0, length_of_a_list):
            place_holder_list = []
            place_holder_list.append(firearm_type_list[i])
            place_holder_list.append(cost_list[i])
            place_holder_list.append(link_list[i])
            place_holder_list.append(new_stock_status_list[i])
            master_list_long_guns.append(place_holder_list)
        # Below is necessary because the next page arrow moves based on what page you are on
        time.sleep(2)

        iteration += 1
        if iteration == 1:
            try:
                next_page_button = driver.find_element(By.XPATH,
                                                   "/html/body/div[2]/div/div[3]/div[3]/main/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/a[3]")
            except selenium.common.exceptions.NoSuchElementException:
                time.sleep(5)
                next_page_button = driver.find_element(By.XPATH,
                                                       "/html/body/div[2]/div/div[3]/div[3]/main/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/a[3]")
            time.sleep(3)
            next_page_button.click()
            time.sleep(TIME_TO_SLEEP_MAX_PAGE_SIZE)
        elif iteration >= 2:
            time.sleep(2)
            break
        else:
            driver.quit()
            break

    both_lists = [*master_list_handguns, *master_list_long_guns]


    # Setting up the headers to write into the CSV
    headers = ["firearm_type", "price", "link", "stock_status"]
    orion_file = "C:\\Users\\Owen\\Documents\\Personal Info\\Independent Courses\\Python Learning\\fflwholesalerproductpps\\Data\\WholesalerReports\\orion_wholesale_data_encoded.csv"
    new_orion_file = "C:\\Users\\Owen\\Documents\\Personal Info\\Independent Courses\\Python Learning\\fflwholesalerproductpps\\Data\\WholesalerReports\\orion_wholesale_data.csv"
    with open(orion_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(both_lists)

    with open(orion_file, 'r', encoding='cp1252') as inp, \
            open(new_orion_file, 'w', encoding='utf-8') as output_file_orion:
        for line in inp:
            output_file_orion.write(line)
    os.remove(orion_file)
