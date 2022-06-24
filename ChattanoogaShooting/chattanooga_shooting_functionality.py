import csv
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time, os
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions


def get_chattanooga_shooting_data():
    # Setting up connection to driver and site
    URL = "https://chattanoogashooting.com/"
    s = Service("C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/chromedriver")
    driver = webdriver.Chrome(service=s)

    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")

    # Opening URL
    driver.get(URL)
    driver.maximize_window()
    time.sleep(1)

    # Clicking Login
    login_button = driver.find_element(By.XPATH, "/html/body/header/section[1]/div[2]/nav/span/a")
    login_button.click()
    time.sleep(.5)

    # Filling in the email and passwords
    email_field = driver.find_element(By.ID, "field-cred-username")
    email_field.send_keys(EMAIL)
    time.sleep(1)
    password_field = driver.find_element(By.ID, "field-cred-password")
    password_field.send_keys(PASSWORD)
    time.sleep(1)

    # Clicking to sign in
    sign_in_button = driver.find_element(By.ID, "field-submit-login-form")
    sign_in_button.click()

    # Hovering over the departments tab
    departments_tab = driver.find_element(By.XPATH, "/html/body/header/section[2]/div/div[1]/nav/span[2]/a[2]")
    a = ActionChains(driver)
    a.move_to_element(departments_tab).perform()
    time.sleep(.5)
    # Clicking to go to the firearms page
    try:
        firearms_tab = driver.find_element(By.XPATH,
                                           "/html/body/header/section[2]/div/div[1]/nav/span[2]/div/div/div/span[3]/a")
        firearms_tab.click()
    except selenium.common.exceptions.ElementNotInteractableException:
        time.sleep(5)
        firearms_tab = driver.find_element(By.XPATH,
                                           "/html/body/header/section[2]/div/div[1]/nav/span[2]/div/div/div/span[3]/a")
        firearms_tab.click()
    time.sleep(.5)

    # Expanding to show max per page
    # Hovering over the number to display tab
    quantity_shown_per_page_dropdown = driver.find_element(By.ID, "field-filters-per-page-top")
    a = ActionChains(driver)
    a.move_to_element(quantity_shown_per_page_dropdown).perform()
    time.sleep(1)
    # Clicking to go to 100 per page
    max_per_page = driver.find_element(By.XPATH,
                                       "/html/body/main/section/div/div[2]/section[2]/div/div[1]/div[1]/ul/li[1]/span/select/option[4]")
    max_per_page.click()
    time.sleep(1)


    # Seeing how many items are shown:
    # the "1-100 of 5,164 items" is in the html as one string, so treating it like a list to extract info
    items_on_screen = driver.find_element(By.XPATH,
                                          "/html/body/main/section/div/div[2]/section[2]/div/div[1]/div[1]/ul/li[2]")
    items_on_screen_text = items_on_screen.text
    # Keeping the below strings to they can be added together
    total_items_part_one = items_on_screen_text[9:10]
    total_items_part_two = items_on_screen_text[11:14]
    total_items = int(total_items_part_one + total_items_part_two)

    # Declaring lists so they can be made global and accessed outside of the loop
    master_firearm_type_list = []
    master_link_list = []
    master_cost_list = []
    master_stock_status_list = []

    # Below is what to cycle through to get the data

    global iteration, master_list
    master_list = []
    iteration = 0
    items_shown_so_far = iteration
    while items_shown_so_far < total_items:
        # Collect data - do straight now, make a function or nest in a loop of clicking pages
        time.sleep(.5)
        firearm_type = driver.find_elements(By.CLASS_NAME, "product-title")
        firearm_type_list = []
        for item in firearm_type:
            new_firearm = item.text
            firearm_type_list.append(new_firearm)

        # Getting links
        link_list = []
        for i in range(1, 5):
            for i in range(1, 26):
                link = driver.find_element(By.XPATH,
                                           f"/html/body/main/section/div/div[2]/section[2]/div/div[2]/section/div[{i}]/div[2]/div/div[1]/p[1]/a")
                new_link = link.get_attribute("href")
                link_list.append(new_link)

        # Getting cost, try gets regular price, except gets sale price if there is a sale
        cost_list = []
        time.sleep(.2)

        # NEW
        for i in range(1, 101):
            try:
                cost = driver.find_element(By.XPATH, f"/html/body/main/section/div/div[2]/section[2]/div/div[2]/section/div[{i}]/div[2]/div/div[2]/p[1]/span[2]")
                    # cost = driver.find_element(By.XPATH, f"/html/body/main/section/div/div[2]/section[2]/div/div[2]/section/div[{i}]/div[2]/div/div[2]/p[1]/span[2]")
                cost_list.append(cost.text)
            except selenium.common.exceptions.NoSuchElementException:
                try:
                    cost = driver.find_element(By.XPATH, f"/html/body/main/section/div/div[2]/section[2]/div/div[2]/section/div[{i}]/div[2]/div/div[2]/p[1]/span")
                    cost_list.append(cost.text)
                    # Below closes the program on the last page
                except selenium.common.exceptions.NoSuchElementException:
                    break
        # END NEW

        # try:
        # cost = driver.find_elements(By.CLASS_NAME, "price-data ")
        # for item in cost:
        #     cost_list.append(item.text)
        # # except selenium.common.exceptions.StaleElementReferenceException:
        # cost_sale_item = driver.find_elements(By.CLASS_NAME, "item-price-sale")
        # for item in cost:
        #     new_cost_sale = item.text
        #     cost_list.append(item.text)

        # Gets stock status
        stock_status = driver.find_elements(By.CLASS_NAME, "product-stock-status")
        stock_status_list = []
        for item in stock_status:
            new_stock_status = item.text
            stock_status_list.append(new_stock_status)

        def click_next_page():
            # Scrolling to bottom of page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            if iteration <= 3 or iteration > 49:
                try:
                    # Finding and clicking next page
                        next_page_button = driver.find_element(By.XPATH,
                                                               "/html/body/main/section/div/div[2]/section[2]/div/div[2]/div/div/div/ul/li[9]/a/span")

                        next_page_button.click()
                # Need the below because the li[#] changes in the last few options, then the last one quits
                except selenium.common.exceptions.NoSuchElementException:
                    try:
                        next_page_button = driver.find_element(By.XPATH,
                                                               "/html/body/main/section/div/div[2]/section[2]/div/div[2]/div/div/div/ul/li[8]/a/span")

                        next_page_button.click()
                    except selenium.common.exceptions.NoSuchElementException:
                        driver.quit()
            elif iteration > 3:
                next_page_button = driver.find_element(By.XPATH,
                                                       "/html/body/main/section/div/div[2]/section[2]/div/div[2]/div/div/div/ul/li[11]/a/span")
                next_page_button.click()
        time.sleep(.5)
        # Adding to master list
        master_firearm_type_list.append(firearm_type_list)
        master_link_list.append(link_list)
        master_cost_list.append(cost_list)
        master_stock_status_list.append(stock_status_list)


        # Checking again how many items are shown - NEEDS TO BE LAST THING BEFORE NEXT PAGE CLICK
        time.sleep(1)
        iteration += 1
        items_shown_so_far = iteration * 100

        length_of_a_list = len(master_firearm_type_list)

        # Organizing all into one list in order: 0) type 1) cost 2) link 3) Stock Status
        for i in range(0, length_of_a_list):
            place_holder_list = []
            place_holder_list.append(master_firearm_type_list[0][i])
            place_holder_list.append(master_cost_list[0][i])
            place_holder_list.append(master_link_list[0][i])
            place_holder_list.append(master_stock_status_list[0][i])
            master_list.append(place_holder_list)

        click_next_page()
        time.sleep(1)

    # END OF ITERATIONS

    # To close - REMOVE LATER
    time.sleep(2)
    driver.quit()

    # Writing to csv
    # Setting up the headers to write into the CSV
    chattanooga_file = "C:\\Users\\Owen\\Documents\\Personal Info\\Independent Courses\\Python Learning\\fflwholesalerproductpps\\Data\\WholesalerReports\\chattanooga_shooting_data_encoded.csv"
    # chattanooga_file = "C:\\Users\\Owen\\Documents\\Personal Info\\Independent Courses\\Python Learning\\fflwholesalerproductpps\\Data\\WholesalerReports\\chattanooga_shooting_data.csv"
    new_chattanooga_file = "C:\\Users\\Owen\\Documents\\Personal Info\\Independent Courses\\Python Learning\\fflwholesalerproductpps\\Data\\WholesalerReports\\chattanooga_shooting_data.csv"
    headers = ["firearm_type", "price", "link", "stock_status"]
    with open(chattanooga_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(master_list)

    with open(chattanooga_file, 'r', encoding='cp1252') as inp, \
            open(new_chattanooga_file, 'w', encoding='ascii') as output_file_chattanooga:
        for line in inp:
            output_file_chattanooga.write(line)
    os.remove(chattanooga_file)
