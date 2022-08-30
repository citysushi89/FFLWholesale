import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.common.keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions
import os
from functions import open_url, click_login_button, fill_in_login_boxes, click_firearms_tab, maximize_page_size, \
    convert_selenium_objects_to_list, convert_selenium_objects_to_list_of_links, clean_firearm_type, clean_stock_grice


def get_second_amendment_wholesale_data():
    s = Service("C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/chromedriver")
    driver = webdriver.Chrome(service=s)
    a = ActionChains(driver)

    # Setting up connection to driver and site
    URL = "https://www.2ndamendmentwholesale.com/"

    # Getting login info using environment variables
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")

    # Setting up the iterations, using formulas from functions.py
    open_url(URL, driver)
    time.sleep(.5)
    click_login_button(location="/html/body/div[2]/header/div[2]/div/div[4]/ul/li[2]/a", driver=driver)


    # Logging in
    email_field_id = "email"
    password_field_id = "pass"
    sign_in_id = "send2"
    fill_in_login_boxes(EMAIL, PASSWORD, email_field_id, password_field_id, sign_in_id, driver)

    # Navigating to the firearms tab
    tab_location = "/html/body/div[2]/header/div[2]/div/div[2]/nav/ul/li[1]/a"
    firearms_tab_click_location = "/html/body/div[2]/header/div[2]/div/div[2]/nav/ul/li[1]/a/span[2]"
    time.sleep(2)
    click_firearms_tab(tab_location, firearms_tab_click_location, driver)
    time.sleep(1)

    # Maximizing Page size
    drop_down_location_id = "limiter"
    max_option_x_path = "/html/body/div[2]/main/div[6]/div[1]/div[3]/div[3]/div[3]/div/select/option[4]"
    maximize_page_size(drop_down_location_id, max_option_x_path, driver, a)
    time.sleep(1)

    time.sleep(1)
    total_items = int(driver.find_element(By.XPATH, "/html/body/div[2]/main/div[6]/div[1]/div[3]/div[1]/p/span[3]").text)
    items_shown_so_far = int(driver.find_element(By.XPATH,
                                             "/html/body/div[2]/main/div[6]/div[1]/div[3]/div[1]/p/span[2]").text)

    global master_list, iteration
    master_list = []
    iteration = 0

    while items_shown_so_far < total_items:
        time.sleep(1)

        # Below uses function from functions.py to convert into a list
        firearm_type = driver.find_elements(By.CLASS_NAME, "product-item-link")
        firearm_type_list = convert_selenium_objects_to_list(input_list=firearm_type)
        # Below remoces ^tm from the names of firearms, was causing encoding errors in CSVs
        for item in firearm_type:
            item_text = item.text
            item_index = firearm_type_list.index(item_text)
            if "™" in item_text:
                new_item = item_text.replace("™", "")
                firearm_type_list.remove(item_text)
                firearm_type_list.insert(item_index, new_item)
        # clean firearm type
        brand_list, model_list = clean_firearm_type(firearm_type_list)

        # Gets Cost
        cost = driver.find_elements(By.CLASS_NAME, "price-box")
        cost_list = convert_selenium_objects_to_list(input_list=cost)

        # Gets link
        links = driver.find_elements(By.CLASS_NAME, "product-item-link")
        link_list = convert_selenium_objects_to_list_of_links(input_list=links)

        # Gets Stock Status
        number_of_items_on_page = len(firearm_type_list)
        stock_status_temp_list = []
        # for i in range(1, number_of_items_on_page + 1):
        stock_status = driver.find_elements(By.CLASS_NAME, "actions-primary")
        stock_status_list = convert_selenium_objects_to_list(input_list=stock_status)
        clean_stock_status_list = clean_stock_grice(stock_status_list)

        time.sleep(1)
        # Going to the bottom of the page and clicking the next page button
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # next_page_button = driver.find_element(By.CLASS_NAME, "next")


        def click_next_page():
            next_page_button = driver.find_element(By.XPATH,
                                                "/html/body/div[2]/main/div[6]/div[1]/div[3]/div[3]/div[2]/ul/li[6]/a")
            next_page_button.click()

        length_of_a_list = len(firearm_type_list)

        # Organizing all into one list in order: 0) type 1) cost 2) link 3) Stock Status
        for i in range(0, length_of_a_list):
            place_holder_list = []
            # TODO Add brand, model and vendor
            place_holder_list.append(brand_list[i])
            place_holder_list.append(model_list[i])
            place_holder_list.append(cost_list[i])
            place_holder_list.append(link_list[i])
            place_holder_list.append(clean_stock_status_list[i])
            place_holder_list.append('Second Amendment Wholesale')
            master_list.append(place_holder_list)

        # Checking again how many items are shown - NEEDS TO BE LAST THING BEFORE NEXT PAGE CLICK
        time.sleep(1)
        iteration += 1
        items_shown_so_far = iteration + 96

        time.sleep(.5)
        try:
            click_next_page()
            time.sleep(.5)
        except selenium.common.exceptions.NoSuchElementException:
            time.sleep(2)
            driver.quit()
            break

    # Setting up the headers to write into the CSV
    second_file = r"C:\Users\Owen\Documents\Personal Info\Independent Courses\Python Learning\fflwholesalerproductpps\Data\WholesalerReports\second_amendment_wholesale_data_encoded.csv"
    new_second_file = r"C:\Users\Owen\Documents\Personal Info\Independent Courses\Python Learning\fflwholesalerproductpps\Data\WholesalerReports\second_amendment_wholesale_data.csv"
    headers = ["brand", "model", "price", "link", "stock_status", "vendor"]
    with open(second_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(master_list)

    with open(second_file, 'r', encoding='cp1252') as inp, \
            open(new_second_file, 'w', encoding='ascii') as output_file_second:
        for line in inp:
            # Below required or whole document fails to write to csv properly
            # NOTES: missing a few items due to the try/except just below, but at time of testing just 9 out of 950 items
            try:
                output_file_second.write(line)
            except UnicodeEncodeError:
                pass
    os.remove(second_file)

get_second_amendment_wholesale_data()


# TODO
# clean stock status
# Add vendor
# separate brand and model - use first space