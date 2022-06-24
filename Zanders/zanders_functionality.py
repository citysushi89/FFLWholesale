from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.common.keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions
import csv, os
from functions import open_url, click_login_button, fill_in_login_boxes, click_firearms_tab, maximize_page_size, \
    convert_selenium_objects_to_list, convert_selenium_objects_to_list_of_links, \
    convert_selenium_objects_to_list_zanders_cost


def get_zanders_data():
    s = Service("C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/chromedriver")
    driver = webdriver.Chrome(service=s)
    a = ActionChains(driver)

    # Setting up connection to driver and site
    URL = "https://shop2.gzanders.com/"

    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")

    # Setting up the iterations, using formulas from functions.py
    open_url(URL, driver)
    time.sleep(.5)
    click_login_button(location="/html/body/div[1]/header/div[1]/div[3]/ul/li[6]/a", driver=driver)

    # Logging in
    email_field_id = "email"
    password_field_id = "pass"
    sign_in_id = "send2"
    fill_in_login_boxes(EMAIL, PASSWORD, email_field_id, password_field_id, sign_in_id, driver)
    iteration = 0
    master_list = []
    # Navigating to the firearms tab
    tab_location = "/html/body/div[1]/header/div[2]/div[1]/div/div[2]/div[1]/div[1]/a"
    firearms_tab_click_location = "//html/body/div[1]/header/div[2]/div[1]/div/div[2]/div[2]/div/ul/li[1]/span/a/span"
    time.sleep(2)
    click_firearms_tab(tab_location, firearms_tab_click_location, driver)
    time.sleep(1)
    # Already at max items shown per page

    while True:
        # total_items = int(driver.find_element(By.XPATH,
        # "/html/body/div[1]/main/div[4]/div[3]/div[5]/div[1]/div[1]/p/span[3]"))
        iteration += 1
        # Getting Firearm Type
        firearm_type = driver.find_elements(By.CLASS_NAME, "product-item-link")
        firearm_type_list = convert_selenium_objects_to_list(firearm_type)
        time.sleep(.2)
        items_per_page = len(firearm_type_list)

        # Getting Price
        cost = driver.find_elements(By.CLASS_NAME, "price-container")
        # IF a sale: removing the previous price and just displaying the sale price
        # cannot use functions.py convert selenium objects to list because there is something for that already
        cost_list = convert_selenium_objects_to_list_zanders_cost(input_list=cost)
        time.sleep(.2)

        # Getting Link
        links = []
        for i in range(1, 61):
            try:
                links.append(driver.find_element(By.XPATH,
                                                 f"/html/body/div[1]/main/div[4]/div[3]/div[5]/div[2]/ol/li[{i}]/div/div/strong/a"))
            except selenium.common.exceptions.NoSuchElementException:
                pass
        link_list = convert_selenium_objects_to_list_of_links(input_list=links)
        time.sleep(.2)

        # Getting Stock Status
        stock_status = driver.find_elements(By.CLASS_NAME, "actions-primary")
        stock_status_list = convert_selenium_objects_to_list(stock_status)
        # Starting out: stock status looked like: 'QTY:\nBACK ORDER'
        stock_status_list_formatted = []
        for item in stock_status_list:
            item_index = stock_status_list.index(item)
            if "\n" in item:
                new_string = item.split("\n")
                new_item = new_string[1]
                stock_status_list_formatted.insert(item_index, new_item)
            else:
                stock_status_list_formatted.append(item)
        time.sleep(.5)


        for i in range(0, len(firearm_type_list)):
            place_holder_list = []
            place_holder_list.append(firearm_type_list[i])
            place_holder_list.append(cost_list[i])
            place_holder_list.append(link_list[i])
            place_holder_list.append(stock_status_list_formatted[i])
            master_list.append(place_holder_list)
        total_length = len(master_list)
        print(f"Total items so far: {total_length}")
        time.sleep(.2)

        if iteration < 2:
            next_page_button = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div[3]/div[5]/div[1]/div[1]/div[2]/ul/li[6]/a/span[2]")
            next_page_button.click()
            time.sleep(1)
        elif iteration >= 2:
            try:
                next_page_button = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div[3]/div[5]/div[1]/div[1]/div[2]/ul/li[7]/a/span[2]")
                next_page_button.click()
                time.sleep(1)
            except selenium.common.exceptions.NoSuchElementException:
                break


    headers = ["firearm_type", "price", "link", "stock_status"]
    zanders_file = "C:\\Users\\Owen\\Documents\\Personal Info\\Independent Courses\\Python Learning\\fflwholesalerproductpps\\Data\\WholesalerReports\\zanders_data_encoded.csv"
    new_zanders_file = "C:\\Users\\Owen\\Documents\\Personal Info\\Independent Courses\\Python Learning\\fflwholesalerproductpps\\Data\\WholesalerReports\\zanders_data.csv"
    with open(zanders_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(master_list)

    with open(zanders_file, 'r', encoding='cp1252') as inp, \
            open(new_zanders_file, 'w', encoding='utf-8') as output_file_orion:
        for line in inp:
            output_file_orion.write(line)
    os.remove(zanders_file)

