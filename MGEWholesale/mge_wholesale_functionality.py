import selenium.common.exceptions
from functions import clean_price

def get_mge_wholesale_data():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    import time
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    import csv
    import os

    # installing the drivers
    # driver = webdriver.Chrome(ChromeDriverManager().install())

    # Setting up the details for the login page
    s = Service("C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/chromedriver")
    driver = webdriver.Chrome(service=s)
    URL = "https://www.mgewholesale.com/ecommerce/account/login.cfm"

    # LOGIN DATA: using environment variables

    # TODO remove this framework and just use env variables later
    # try:
    CUSTOMER_NUMBER = os.getenv("CUSTOMER_NUMBER")
    # except:

    if type(CUSTOMER_NUMBER) == "<class 'NoneType'>":
        CUSTOMER_NUMBER = os.environ['CUSTOMER_NUMBER']


    PASSWORD = os.getenv("PASSWORD")


    # # Loading the webpage
    # driver = webdriver.Chrome(service=s)
    driver.get(URL)
    time.sleep(2)

    # Filling in the email and passwords
    customer_number_field = driver.find_element(By.NAME, "cust_id")
    customer_number_field.send_keys(CUSTOMER_NUMBER)
    time.sleep(1)
    password_field = driver.find_element(By.NAME, "login_pass")
    password_field.send_keys(PASSWORD)
    time.sleep(1)

    # Clicking the Sign In Button
    sign_in_button = driver.find_element(By.NAME, "login_submit")
    sign_in_button.click()
    time.sleep(.5)

    # Clicking on the Firearms Tab
    def click_firearms_tab():
        time.sleep(1.5)
        shop_tab = driver.find_element(By.CLASS_NAME, "dropdown-toggle")
        a = ActionChains(driver)
        a.move_to_element(shop_tab).perform()
        time.sleep(1)
        #   Second clicks on firearms tab
        firearms_tab = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div[2]/ul/li[2]/ul/li[4]/a")
        firearms_tab.click()
        time.sleep(.5)

    # HOME PAGE FIREARMS
    click_firearms_tab()

    # Setting up the master dictionary
    firearm_home_page_list = {}

    # Getting data from the firearms on the firearms home page
    firearm_type = driver.find_elements(By.CLASS_NAME, "boxtext")
    cost = driver.find_elements(By.CLASS_NAME, "price-sales")
    cost_text = [item.text for item in cost]
    link_to_firearm_unorganized = driver.find_elements(By.CLASS_NAME, "col-centered")
    stock_status_unorganized = driver.find_elements(By.CLASS_NAME, "quantity")
    for item in stock_status_unorganized:
        if item.text == "Quantity:":
            stock_status_unorganized.remove(item)
    time.sleep(.5)

    # Organizing List of Dictionaries Dictionary of Details, Price, and Links
    links_to_firearms = []
    for links in link_to_firearm_unorganized:
        new_link = links.find_element(By.TAG_NAME, "a")
        new_link_text = new_link.get_attribute("href")
        links_to_firearms.append(new_link_text)

    # Cleaning Price verbiage
    price_list = []
    new_item = ''
    for item in cost_text:
        for letter in item:
            if letter.isdigit() or letter == '$' or letter == '.':
                new_item += letter
        price_list.append(new_item)
        new_item = ''


    # Cleaning stock status verbiage
    stock_status_list = []
    for item in stock_status_unorganized:
        text = item.text
        new_item = ''
        for item in text:
            if item.isdigit():
                new_item += item
        if new_item:
            stock_status_list.append(new_item)
        else:
            stock_status_list.append('Out of Stock')

    # Separating the model and brand
    brand_list = []
    model_list = []
    for item in firearm_type:
        text = item.text
        brand, model = text.split(' ', 1)
        brand_list.append(brand)
        model_list.append(model)

    # Categories in all lists
    list_categories = ["brand", "model", "price", "link", "stock_status", "vendor"]

    # Actually organizing the data into a dictionary
    previous_items_shown = 0
    for n in range(len(firearm_type)):
        firearm_home_page_list[n] = {
            "brand": brand_list[n],
            "model": model_list[n],
            "price": price_list[n],
            "link": links_to_firearms[n],
            "stock_status": stock_status_list[n],
            "vendor": "MGE Wholesale"
        }
        previous_items_shown += 1


    # DERRINGER
    # Clicking on the Derringer page
    derringer_page = driver.find_element(By.XPATH, "/html/body/div[2]/div[7]/div/div[1]/ul/li[1]/a")
    derringer_page.click()
    time.sleep(.5)

    # Setting up the master dictionary
    derringer_list = {}

    # Getting Data from Derringer page
    firearm_type = driver.find_elements(By.CLASS_NAME, "boxtext")
    cost = driver.find_elements(By.CLASS_NAME, "price-sales")
    cost_text = [item.text for item in cost]
    link_to_firearm_unorganized = driver.find_elements(By.CLASS_NAME, "col-centered")
    stock_status_unorganized = driver.find_elements(By.CLASS_NAME, "quantity")
    for item in stock_status_unorganized:
        if item.text == "Quantity:":
            stock_status_unorganized.remove(item)
    time.sleep(.5)


    # Organizing List of Dictionaries Dictionary of Details, Price, and Links
    links_to_firearms = []
    for links in link_to_firearm_unorganized:
        new_link = links.find_element(By.TAG_NAME, "a")
        new_link_text = new_link.get_attribute("href")
        links_to_firearms.append(new_link_text)

    # Cleaning Price verbiage
    price_list = []
    new_item = ''
    for item in cost_text:
        for letter in item:
            if letter.isdigit() or letter == '$' or letter == '.':
                new_item += letter
        price_list.append(new_item)
        new_item = ''



    # Cleaning stock status verbiage
    stock_status_list = []
    for item in stock_status_unorganized:
        text = item.text
        new_item = ''
        for item in text:
            if item.isdigit():
                new_item += item
        if new_item:
            stock_status_list.append(new_item)
        else:
            stock_status_list.append('Out of Stock')

    # Separating the model and brand
    brand_list = []
    model_list = []
    for item in firearm_type:
        text = item.text
        brand, model = text.split(' ', 1)
        brand_list.append(brand)
        model_list.append(model)

    # Actually organizing the data into a dictionary
    previous_items_shown = 0
    for n in range(len(firearm_type)):
        derringer_list[n] = {
            "brand": brand_list[n],
            "model": model_list[n],
            "price": price_list[n],
            "link": links_to_firearms[n],
            "stock_status": stock_status_list[n],
            "vendor": "MGE Wholesale"
        }
        previous_items_shown += 1

    time.sleep(.5)


    # PISTOL
    # Going back to firearms tab to then click pistol
    click_firearms_tab()

    # Clicking on the Pistol page
    time.sleep(.5)
    pistol_page = driver.find_element(By.XPATH, "/html/body/div[2]/div[7]/div/div[1]/ul/li[2]/a")
    pistol_page.click()
    time.sleep(.5)

    # Setting up the master dictionary
    pistol_list = {}
    ITEMS_PER_PAGE = 99
    previous_run_throughs = 0
    iteration = 1

    # Finding the last page based on the list (using the last number next to the next arrow, thinking that however many
    # pages they have that they will always show how many are there), then using that as the stopping point
    last_page = driver.find_element(By.XPATH, "/html/body/div[2]/div[7]/div/div[2]/div[2]/div[1]/div/ul/li[6]/a")
    last_page_number = int(last_page.text) + 1

    # Iterating through the pistol pages and getting the data
    while iteration < last_page_number:
        time.sleep(1)
        # Getting Data from Pistol page
        firearm_type = driver.find_elements(By.CLASS_NAME, "boxtext")
        cost_pistol = driver.find_elements(By.CLASS_NAME, "price-sales")
        link_to_firearm_unorganized = driver.find_elements(By.CLASS_NAME, "col-centered")
        stock_status_unorganized = driver.find_elements(By.CLASS_NAME, "quantity")
        for item in stock_status_unorganized:
            if item.text == "Quantity:":
                stock_status_unorganized.remove(item)

        time.sleep(1)
        # Below Code: Fixed IndexError when "Our Price" and "Sale Price" are shown,
        # 1 time each for a single firearm leads to
        # an error when compiling the dictionary later on List looked like: "Our Price 499$" "our Price 500\nSale Price 525"
        cost_pistol_text = [item.text for item in cost_pistol]


        time.sleep(1)
        cost_pistol_text_fixed = []
        counter = 0
        sale_counter = 0
        for item in cost_pistol_text:
            if "Sale" in item:
                pass
                temp_list = item.splitlines()
                sale_price = temp_list[1]
                cost_pistol_text_fixed.append(sale_price)
                sale_counter += 1
                counter += 1
            else:
                cost_pistol_text_fixed.append(item)
                counter += 1
        time.sleep(.5)

        # Organizing List of Dictionaries Dictionary of Details, Price, and Links
        links_to_firearms = []
        for links in link_to_firearm_unorganized:
            new_link = links.find_element(By.TAG_NAME, "a")
            new_link_text = new_link.get_attribute("href")
            links_to_firearms.append(new_link_text)

        # Cleaning Price verbiage
        price_list = []
        new_item = ''
        print(cost_pistol_text)
        print(cost_pistol_text_fixed)
        for item in cost_pistol_text_fixed:
            for letter in item:
                # print(letter)
                if letter.isdigit() or letter == '$' or letter == '.':
                    new_item += letter
                    print(new_item)
            price_list.append(new_item)
            new_item = ''
        print(price_list)


        # Cleaning stock status verbiage
        stock_status_list = []
        for item in stock_status_unorganized:
            text = item.text
            new_item = ''
            for item in text:
                if item.isdigit():
                    new_item += item
            if new_item:
                stock_status_list.append(new_item)
            else:
                stock_status_list.append('Out of Stock')

        # Separating the model and brand
        brand_list = []
        model_list = []
        for item in firearm_type:
            text = item.text
            try:
                brand, model = text.split(' ', 1)
            except ValueError:
                brand = "N/A"
                model = text
            brand_list.append(brand)
            model_list.append(model)

        # Actually organizing the data into a dictionary
        for n in range(len(firearm_type)):
            pistol_list[n + (previous_run_throughs * ITEMS_PER_PAGE)] = {
                "brand": brand_list[n],
                "model": model_list[n],
                "price": price_list[n],
                "link": links_to_firearms[n],
                "stock_status": stock_status_list[n],
                "vendor": "MGE Wholesale"
            }
            previous_run_throughs += 1
        time.sleep(1)

        # deciding which element to find and click as the next arrow
        if iteration == 1:
            next_page = driver.find_element(By.XPATH,
                                            f"/html/body/div[2]/div[7]/div/div[2]/div[2]/div[1]/div/ul/li[7]/a")
            iteration += 1
            time.sleep(.5)
            next_page.click()
        elif iteration > 1:
            try:
                time.sleep(.5)
                next_page = driver.find_element(By.XPATH,
                                                f"/html/body/div[2]/div[7]/div/div[2]/div[2]/div[1]/div/ul/li[8]/a")
                iteration += 1
                time.sleep(.5)
                next_page.click()
            except selenium.common.exceptions.NoSuchElementException:
                break

        time.sleep(.5)


    time.sleep(.75)

    # PISTOL FRAME
    click_firearms_tab()

    # Clicking on the PISTOL FRAME page
    pistol_frame_page = driver.find_element(By.XPATH, "/html/body/div[2]/div[7]/div/div[1]/ul/li[3]/a")
    pistol_frame_page.click()
    time.sleep(.5)

    # Setting up the master dictionary
    pistol_frame_list = {}

    # Getting Data from PISTOL FRAME page
    firearm_type = driver.find_elements(By.CLASS_NAME, "boxtext")
    cost = driver.find_elements(By.CLASS_NAME, "price-sales")
    cost_text = [item.text for item in cost]
    link_to_firearm_unorganized = driver.find_elements(By.CLASS_NAME, "col-centered")
    stock_status_unorganized = driver.find_elements(By.CLASS_NAME, "quantity")
    for item in stock_status_unorganized:
        if item.text == "Quantity:":
            stock_status_unorganized.remove(item)
    time.sleep(.5)


    # Organizing List of Dictionaries Dictionary of Details, Price, and Links
    links_to_firearms = []
    for links in link_to_firearm_unorganized:
        new_link = links.find_element(By.TAG_NAME, "a")
        new_link_text = new_link.get_attribute("href")
        links_to_firearms.append(new_link_text)

    # Cleaning Price verbiage
    price_list = []
    new_item = ''
    for item in cost_text:
        for letter in item:
            if letter.isdigit() or letter == '$' or letter == '.':
                new_item += letter
        price_list.append(new_item)
        new_item = ''


    # Cleaning stock status verbiage
    stock_status_list = []
    for item in stock_status_unorganized:
        text = item.text
        new_item = ''
        for item in text:
            if item.isdigit():
                new_item += item
        if new_item:
            stock_status_list.append(new_item)
        else:
            stock_status_list.append('Out of Stock')

    # Separating the model and brand
    brand_list = []
    model_list = []
    for item in firearm_type:
        text = item.text
        brand, model = text.split(' ', 1)
        brand_list.append(brand)
        model_list.append(model)

    # Actually organizing the data into a dictionary
    previous_items_shown = 0
    for n in range(len(firearm_type)):
        pistol_frame_list[n] = {
            "brand": brand_list[n],
            "model": model_list[n],
            "price": price_list[n],
            "link": links_to_firearms[n],
            "stock_status": stock_status_list[n],
            "vendor": "MGE Wholesale"
        }
        previous_items_shown += 1

    # REVOLVER
    # Moving from pistol frame to revolver page
    click_firearms_tab()

    # Clicking on the Revolver
    revolver_page = driver.find_element(By.XPATH, "/html/body/div[2]/div[7]/div/div[1]/ul/li[4]/a")
    revolver_page.click()
    time.sleep(.5)

    # Setting up the master dictionary
    revolver_list = {}

    # Getting Data from Revolver page
    firearm_type = driver.find_elements(By.CLASS_NAME, "boxtext")
    cost = driver.find_elements(By.CLASS_NAME, "price-sales")
    cost_text = [item.text for item in cost]
    link_to_firearm_unorganized = driver.find_elements(By.CLASS_NAME, "col-centered")
    stock_status_unorganized = driver.find_elements(By.CLASS_NAME, "quantity")
    for item in stock_status_unorganized:
        if item.text == "Quantity:":
            stock_status_unorganized.remove(item)
    time.sleep(.5)


    # Organizing List of Dictionaries Dictionary of Details, Price, and Links
    links_to_firearms = []
    for links in link_to_firearm_unorganized:
        new_link = links.find_element(By.TAG_NAME, "a")
        new_link_text = new_link.get_attribute("href")
        links_to_firearms.append(new_link_text)

    # Cleaning Price verbiage
    price_list = []
    new_item = ''
    for item in cost_text:
        for letter in item:
            if letter.isdigit() or letter == '$' or letter == '.':
                new_item += letter
        price_list.append(new_item)
        new_item = ''



    # Cleaning stock status verbiage
    stock_status_list = []
    for item in stock_status_unorganized:
        text = item.text
        new_item = ''
        for item in text:
            if item.isdigit():
                new_item += item
        if new_item:
            stock_status_list.append(new_item)
        else:
            stock_status_list.append('Out of Stock')

    # Separating the model and brand
    brand_list = []
    model_list = []
    for item in firearm_type:
        text = item.text
        brand, model = text.split(' ', 1)
        brand_list.append(brand)
        model_list.append(model)

    # Actually organizing the data into a dictionary
    previous_items_shown = 0
    for n in range(len(firearm_type)):
        revolver_list[n] = {
            "brand": brand_list[n],
            "model": model_list[n],
            "price": price_list[n],
            "link": links_to_firearms[n],
            "stock_status": stock_status_list[n],
            "vendor": "MGE Wholesale"
        }
        previous_items_shown += 1

    # RIFLE
    # Moving from Revolver to Rifle
    click_firearms_tab()

    # Clicking on the Rifle Page
    rifle_page = driver.find_element(By.XPATH, "/html/body/div[2]/div[7]/div/div[1]/ul/li[5]/a")
    rifle_page.click()
    time.sleep(.5)

    # Setting up the master dictionary
    rifle_list = {}
    previous_items_shown = 0
    iteration = 1

    # Finding the last page based on the list (using the last number next to the next arrow, thinking that however many
    # pages they have that they will always show how many are there), then using that as the stopping point
    # THIS ONLY WORKS WHEN THERE ARE EXACTLY 4 PAGES, IF IT INCREASES USE THE SYSTEM FOR PISTOLS,
    # IF IT DECREASES IT HAS TO CHANGE, LIKELY TO li[3] or less
    last_page = driver.find_element(By.XPATH, "/html/body/div[2]/div[7]/div/div[2]/div[2]/div[1]/div/ul/li[6]/a")
    last_page_number = int(last_page.text)

    # Iterating through the pistol pages and getting the data
    while iteration < last_page_number + 1:

        # Getting Data from Rifle page
        firearm_type = driver.find_elements(By.CLASS_NAME, "boxtext")
        cost_pistol = driver.find_elements(By.CLASS_NAME, "price-sales")
        link_to_firearm_unorganized = driver.find_elements(By.CLASS_NAME, "col-centered")
        stock_status_unorganized = driver.find_elements(By.CLASS_NAME, "quantity")
        for item in stock_status_unorganized:
            if item.text == "Quantity:":
                stock_status_unorganized.remove(item)

        # Below Code: Fixed IndexError when "Our Price" and "Sale Price" are shown,
        # 1 time each for a single firearm leads to
        # an error when compiling the dictionary later on List looked like: "Our Price 499$" "our Price 500\nSale Price 525"
        cost_pistol_text = [item.text for item in cost_pistol]

        cost_pistol_text_fixed = []
        for item in cost_pistol_text:
            if "Sale" in item:
                temp_list = item.splitlines()
                old_price = temp_list[0]
                sale_price = temp_list[1]
                cost_pistol_text_fixed.append(sale_price)
            else:
                cost_pistol_text_fixed.append(item)
        time.sleep(.5)


        # Organizing List of Dictionaries Dictionary of Details, Price, and Links
        links_to_firearms = []
        for links in link_to_firearm_unorganized:
            new_link = links.find_element(By.TAG_NAME, "a")
            new_link_text = new_link.get_attribute("href")
            links_to_firearms.append(new_link_text)

        # Cleaning Price verbiage
        price_list = []
        new_item = ''
        for item in cost_pistol_text_fixed:
            # text = item.text
            if item.isdigit() or item == '$' or item == '.':
                new_item += item
            price_list.append(new_item)
            new_item = ''


        # Cleaning stock status verbiage
        stock_status_list = []
        for item in stock_status_unorganized:
            text = item.text
            new_item = ''
            for item in text:
                if item.isdigit():
                    new_item += item
            if new_item:
                stock_status_list.append(new_item)
            else:
                stock_status_list.append('Out of Stock')

        # Separating the model and brand
        brand_list = []
        model_list = []
        for item in firearm_type:
            text = item.text
            brand, model = text.split(' ', 1)
            brand_list.append(brand)
            model_list.append(model)

        # Actually organizing the data into a dictionary
        for n in range(len(firearm_type)):
            rifle_list[n + (previous_items_shown * ITEMS_PER_PAGE)] = {
                "brand": brand_list[n],
                "model": model_list[n],
                "price": price_list[n],
                "link": links_to_firearms[n],
                "stock_status": stock_status_list[n],
                "vendor": "MGE Wholesale"
            }
            previous_items_shown += len(firearm_type)
        time.sleep(1)

        # deciding which element to find and click as the next arrow
        if iteration == 1:
            try:
                next_page = driver.find_element(By.XPATH, f"/html/body/div[2]/div[7]/div/div[2]/div[2]/div[1]/div/ul/li[5]/a")
            except selenium.common.exceptions.NoSuchElementException:
                next_page = driver.find_element(By.XPATH,"/html/body/div[2]/div[7]/div/div[2]/div[2]/div[1]/div/ul/li[7]/a")
            next_page.click()
        elif iteration > 1:
            time.sleep(1)
            try:
                time.sleep(.5)
                next_page = driver.find_element(By.XPATH,
                                                f"/html/body/div[2]/div[7]/div/div[2]/div[2]/div[1]/div/ul/li[8]/a")
                iteration += 1
                time.sleep(.5)
                next_page.click()
            except selenium.common.exceptions.NoSuchElementException:
                break
        iteration += 1
        time.sleep(.5)
    time.sleep(2)


    # RIFLE FRAME
    click_firearms_tab()

    # Clicking on the Rifle Frame
    rifle_frame_page = driver.find_element(By.XPATH, "/html/body/div[2]/div[7]/div/div[1]/ul/li[3]/a")
    rifle_frame_page.click()
    time.sleep(.5)

    # Setting up the master dictionary
    rifle_frame_list = {}

    # Getting Data from Rifle Frame page
    firearm_type = driver.find_elements(By.CLASS_NAME, "boxtext")
    cost = driver.find_elements(By.CLASS_NAME, "price-sales")
    cost_text = [item.text for item in cost]
    link_to_firearm_unorganized = driver.find_elements(By.CLASS_NAME, "col-centered")
    stock_status_unorganized = driver.find_elements(By.CLASS_NAME, "quantity")
    for item in stock_status_unorganized:
        if item.text == "Quantity:":
            stock_status_unorganized.remove(item)
    time.sleep(.5)


    # Organizing List of Dictionaries Dictionary of Details, Price, and Links
    links_to_firearms = []
    for links in link_to_firearm_unorganized:
        new_link = links.find_element(By.TAG_NAME, "a")
        new_link_text = new_link.get_attribute("href")
        links_to_firearms.append(new_link_text)

    # Cleaning Price verbiage
    price_list = []
    new_item = ''
    for item in cost_text:
        for letter in item:
            if letter.isdigit() or letter == '$' or letter == '.':
                new_item += letter
        price_list.append(new_item)
        new_item = ''


    # Cleaning stock status verbiage
    stock_status_list = []
    for item in stock_status_unorganized:
        text = item.text
        new_item = ''
        for item in text:
            if item.isdigit():
                new_item += item
        if new_item:
            stock_status_list.append(new_item)
        else:
            stock_status_list.append('Out of Stock')

    # Separating the model and brand
    brand_list = []
    model_list = []
    for item in firearm_type:
        text = item.text
        brand, model = text.split(' ', 1)
        brand_list.append(brand)
        model_list.append(model)

    # Actually organizing the data into a dictionary
    previous_items_shown = 0
    for n in range(len(firearm_type)):
        rifle_frame_list[n] = {
            "brand": brand_list[n],
            "model": model_list[n],
            "price": price_list[n],
            "link": links_to_firearms[n],
            "stock_status": stock_status_list[n],
            "vendor": "MGE Wholesale"
        }
        previous_items_shown += 1

    # SHOTGUN
    # Moving from Rifle Frame to Shotgun page
    click_firearms_tab()

    # Clicking on the Shotgun
    shotgun_page = driver.find_element(By.XPATH, "/html/body/div[2]/div[7]/div/div[1]/ul/li[7]/a")
    shotgun_page.click()
    time.sleep(.5)

    # Setting up the master dictionary
    shotgun_list = {}

    # Getting Data from Shotgun
    firearm_type = driver.find_elements(By.CLASS_NAME, "boxtext")
    cost = driver.find_elements(By.CLASS_NAME, "price-sales")
    cost_text = [item.text for item in cost]
    link_to_firearm_unorganized = driver.find_elements(By.CLASS_NAME, "col-centered")
    stock_status_unorganized = driver.find_elements(By.CLASS_NAME, "quantity")
    for item in stock_status_unorganized:
        if item.text == "Quantity:":
            stock_status_unorganized.remove(item)
    time.sleep(.5)


    # Organizing List of Dictionaries Dictionary of Details, Price, and Links
    links_to_firearms = []
    for links in link_to_firearm_unorganized:
        new_link = links.find_element(By.TAG_NAME, "a")
        new_link_text = new_link.get_attribute("href")
        links_to_firearms.append(new_link_text)

    # Cleaning Price verbiage
    price_list = []
    new_item = ''
    for item in cost_text:
        for letter in item:
            if letter.isdigit() or letter == '$' or letter == '.':
                new_item += letter
        price_list.append(new_item)
        new_item = ''


    # Cleaning stock status verbiage
    stock_status_list = []
    for item in stock_status_unorganized:
        text = item.text
        new_item = ''
        for item in text:
            if item.isdigit():
                new_item += item
        if new_item:
            stock_status_list.append(new_item)
        else:
            stock_status_list.append('Out of Stock')

    # Separating the model and brand
    brand_list = []
    model_list = []
    for item in firearm_type:
        text = item.text
        brand, model = text.split(' ', 1)
        brand_list.append(brand)
        model_list.append(model)

    # Actually organizing the data into a dictionary
    previous_items_shown = 0
    for n in range(len(firearm_type)):
        shotgun_list[n] = {
            "brand": brand_list[n],
            "model": model_list[n],
            "price": price_list[n],
            "link": links_to_firearms[n],
            "stock_status": stock_status_list[n],
            "vendor": "MGE Wholesale"
        }
        previous_items_shown += 1



    # CALIFORNIA COMPLIANT
    # Moving from shotgun to California Compliant page
    click_firearms_tab()

    # Clicking on the Pistol page
    # Trouble finding the california compliant page, giving it extra time to load
    time.sleep(.5)
    california_compliant_page = driver.find_element(By.XPATH, "/html/body/div[2]/div[7]/div/div[1]/ul/li[8]/a")
    california_compliant_page.click()
    time.sleep(.5)

    # Setting up the master dictionary
    california_compliant_list = {}
    previous_items_shown = 0

    # Finding the last page based on the list (using the last number next to the next arrow, thinking that however many
    # pages they have that they will always show how many are there), then using that as the stopping point
    # THIS ONLY WORKS WHEN THERE ARE EXACTLY 4 PAGES, IF IT INCREASES USE THE SYSTEM FOR PISTOLS,
    # IF IT DECREASES IT HAS TO CHANGE, LIKELY TO li[3] or less
    last_page = driver.find_element(By.XPATH, "/html/body/div[2]/div[6]/div/div[2]/div/div[2]/div[1]/div/ul/li[2]/a")
    last_page_number = int(last_page.text)
    iteration = 0

    # Iterating through the california compliant pages and getting the data
    while iteration < last_page_number:
        iteration += 1
        # Getting Data from California Compliant Page
        firearm_type = driver.find_elements(By.CLASS_NAME, "boxtext")
        firearm_type_text = [item.text for item in firearm_type]
        print(f"firearm_type_text: {firearm_type_text}")
        cost_california_compliant = driver.find_elements(By.CLASS_NAME, "price-sales")
        link_to_firearm_unorganized = driver.find_elements(By.CLASS_NAME, "col-centered")
        stock_status_unorganized = driver.find_elements(By.CLASS_NAME, "quantity")
        for item in stock_status_unorganized:
            if item.text == "Quantity:":
                stock_status_unorganized.remove(item)

        # Below Code: Fixed IndexError when "Our Price" and "Sale Price" are shown,
        # 1 time each for a single firearm leads to
        # an error when compiling the dictionary later on List looked like: "Our Price 499$" "our Price 500\nSale Price 525"
        cost_california_compliant_text = [item.text for item in cost_california_compliant]

        cost_california_compliant_text_fixed = []
        for item in cost_california_compliant_text:
            if "Sale" in item:
                temp_list = item.splitlines()
                old_price = temp_list[0]
                sale_price = temp_list[1]
                cost_california_compliant_text_fixed.append(sale_price)
            else:
                cost_california_compliant_text_fixed.append(item)
        time.sleep(.5)

        # Organizing List of Dictionaries Dictionary of Details, Price, and Links
        links_to_firearms = []
        for links in link_to_firearm_unorganized:
            new_link = links.find_element(By.TAG_NAME, "a")
            new_link_text = new_link.get_attribute("href")
            links_to_firearms.append(new_link_text)

        # Cleaning Price verbiage
        price_list = []
        new_item = ''
        for item in cost_california_compliant_text_fixed:
            for letter in item:
                if letter.isdigit() or letter == '$' or letter == '.':
                    new_item += letter
            price_list.append(new_item)
            new_item = ''

        # Cleaning stock status verbiage
        stock_status_list = []
        for item in stock_status_unorganized:
            text = item.text
            new_item = ''
            for item in text:
                if item.isdigit():
                    new_item += item
            if new_item:
                stock_status_list.append(new_item)
            else:
                stock_status_list.append('Out of Stock')

        # Separating the model and brand
        brand_list = []
        model_list = []
        for item in firearm_type_text:
            brand, model = item.split(' ', 1)
            brand_list.append(brand)
            model_list.append(model)

        # Actually organizing the data into a dictionary
        for n in range(len(firearm_type)):
            california_compliant_list[n +(previous_items_shown * ITEMS_PER_PAGE)] = {
                "brand": brand_list[n],
                "model": model_list[n],
                "price": price_list[n],
                "link": links_to_firearms[n],
                "stock_status": stock_status_list[n],
                "vendor": "MGE Wholesale"
            }
            previous_items_shown += len(firearm_type)
        time.sleep(1)

        # deciding which element to find and click as the next arrow
        if iteration == 1:
            next_page = driver.find_element(By.XPATH, f"/html/body/div[2]/div[6]/div/div[2]/div/div[2]/div[1]/div/ul/li[3]/a")
            next_page.click()
            time.sleep(.5)
        # Below is not used becuase as of May 2022 only two pages, so only one next page click is required
        elif iteration > 1:
            pass
        time.sleep(.5)

    time.sleep(.5)
    driver.quit()

    # Setting up the headers to write into the CSV
    headers = list_categories

    # Removing the annoying 0 in the dictionaries to make them true dictionaries
    new_derringer_list = [value for value in derringer_list.values()]
    new_pistol_list = [value for value in pistol_list.values()]
    new_pistol_frame_list = [value for value in pistol_frame_list.values()]
    new_revolver_list = [value for value in revolver_list.values()]
    new_rifle_list = [value for value in rifle_list.values()]
    new_rifle_frame_list = [value for value in rifle_frame_list.values()]
    new_shotgun_list = [value for value in shotgun_list.values()]
    new_california_compliant_list = [value for value in california_compliant_list.values()]

    # Connecting all the above dictionaries into a single list of dictionaries
    master_list = [*new_derringer_list, *new_pistol_list, *new_pistol_frame_list, *new_revolver_list, *new_rifle_list,
                   *new_rifle_frame_list, *new_shotgun_list, *new_california_compliant_list]

    # TODO: remove in products
    filename = "/mge_wholesale_data.csv"
    with open(rf"C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/fflwholesalerproductpps/Data/WholesalerReports{filename}", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(master_list)



get_mge_wholesale_data()
