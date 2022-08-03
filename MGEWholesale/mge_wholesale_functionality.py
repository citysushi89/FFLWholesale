import selenium.common.exceptions


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

    ### ALL FOR MGE Wholesale ###
    # Setting up the details for the login page
    # SILENCED SERVICE CODE BEFORE FOR PYTHON ANYWHERE
    s = Service("C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/chromedriver")
    driver = webdriver.Chrome(service=s)
    URL = "https://www.mgewholesale.com/ecommerce/account/login.cfm"

    # LOGIN DATA: using environment variables

    CUSTOMER_NUMBER = os.getenv("CUSTOMER_NUMBER")
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

    # Categories in all lists
    list_categories = ["firearm_type", "price", "link", "stock_status"]

    # Actually organizing the data into a dictionary
    previous_items_shown = 0
    for n in range(len(firearm_type)):
        firearm_home_page_list[n] = {
            "firearm_type": firearm_type[n].text,
            "price": cost[n].text,
            "link": links_to_firearms[n],
            "stock_status": stock_status_unorganized[n].text,
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

    # Actually organizing the data into a dictionary
    previous_items_shown = 0
    for n in range(len(firearm_type)):
        derringer_list[n] = {
            "firearm_type": firearm_type[n].text,
            "price": cost[n].text,
            "link": links_to_firearms[n],
            "stock_status": stock_status_unorganized[n].text,
        }
        previous_items_shown += 1

    # print(derringer_list)
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
    # print(f"The last page number is {last_page_number}")

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

        # Actually organizing the data into a dictionary
        for n in range(len(firearm_type)):
            pistol_list[n + (previous_run_throughs * ITEMS_PER_PAGE)] = {
                "firearm_type": firearm_type[n].text,
                "price": cost_pistol_text_fixed[n],
                "link": links_to_firearms[n],
                "stock_status": stock_status_unorganized[n].text,
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

    # Actually organizing the data into a dictionary
    previous_items_shown = 0
    for n in range(len(firearm_type)):
        pistol_frame_list[n] = {
            "firearm_type": firearm_type[n].text,
            "price": cost[n].text,
            "link": links_to_firearms[n],
            "stock_status": stock_status_unorganized[n].text,
        }
        previous_items_shown += 1

    # print(pistol_frame_list)


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

    # Actually organizing the data into a dictionary
    previous_items_shown = 0
    for n in range(len(firearm_type)):
        revolver_list[n] = {
            "firearm_type": firearm_type[n].text,
            "price": cost[n].text,
            "link": links_to_firearms[n],
            "stock_status": stock_status_unorganized[n].text,
        }
        previous_items_shown += 1

    # print(revolver_list)

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
    # print(f"The last page number is {last_page_number}")

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

        # Actually organizing the data into a dictionary
        for n in range(len(firearm_type)):
            rifle_list[n + (previous_items_shown * ITEMS_PER_PAGE)] = {
                "firearm_type": firearm_type[n].text,
                "price": cost_pistol_text_fixed[n],
                "link": links_to_firearms[n],
                "stock_status": stock_status_unorganized[n].text,
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

    # Actually organizing the data into a dictionary
    previous_items_shown = 0
    for n in range(len(firearm_type)):
        rifle_frame_list[n] = {
            "firearm_type": firearm_type[n].text,
            "price": cost[n].text,
            "link": links_to_firearms[n],
            "stock_status": stock_status_unorganized[n].text,
        }
        previous_items_shown += 1

    # print(f"This is the Rifle Frame List: {rifle_frame_list}")

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

    # Actually organizing the data into a dictionary
    previous_items_shown = 0
    for n in range(len(firearm_type)):
        shotgun_list[n] = {
            "firearm_type": firearm_type[n].text,
            "price": cost[n].text,
            "link": links_to_firearms[n],
            "stock_status": stock_status_unorganized[n].text,
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
    # print(f"The last page number is {last_page_number}")
    iteration = 0

    # Iterating through the california compliant pages and getting the data
    while iteration < last_page_number:
        iteration += 1
        # Getting Data from California Compliant Page
        firearm_type = driver.find_elements(By.CLASS_NAME, "boxtext")
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
                # print(f"The old price was {old_price}")
                sale_price = temp_list[1]
                # print(f"The sale price is {sale_price}")
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

        # Actually organizing the data into a dictionary
        for n in range(len(firearm_type)):
            california_compliant_list[n +(previous_items_shown * ITEMS_PER_PAGE)] = {
                "firearm_type": firearm_type[n].text,
                "price": cost_california_compliant_text_fixed[n],
                "link": links_to_firearms[n],
                "stock_status": stock_status_unorganized[n].text,
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

    # print(f"The California Compliant list is {california_compliant_list}")
    time.sleep(.5)
    driver.quit()

    # Setting up the headers to write into the CSV
    headers = list_categories
    # print(f"The headers are {headers}")

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

    # TODO need to adjust to write to table in userdata.db
    # Writing to DB
    import sqlite3

    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    import csv
    app = Flask(__name__)
    DB_NAME = "userdata.db"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)


    class ItemsTest(db.Model):
        __tablename__ = "mge"
        id = db.Column(db.Integer, primary_key=True, unique=True)
        item = db.Column(db.String(500), unique=False)
        price = db.Column(db.String(250), unique=False)
        quantity = db.Column(db.String(250), unique=False)
        link = db.Column(db.String(1000), unique=False)

    db.create_all()
    # Change path before deployment
    # TODO: remove reading from CSV in production, just go straight from the dict/list to writing to db
    with open(r"C:\Users\Owen\Documents\Personal Info\Independent Courses\Python Learning\fflwholesalerproductpps\Data\WholesalerReports\mge_wholesale_data.csv") as file:
        # reading the CSV file
        csvFile = csv.reader(file)
        headers = next(csvFile)
        counter = 0
        # accessing and deleting from the database
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM mge")
        connection.commit()
        connection.close()
        # Creating a list to check against to avoid unique attribute failed error
        items_in_db_already = []
        # Writing to the database
        for lines in csvFile:
            if lines[0] in items_in_db_already:
                continue
            else:
                items_in_db_already.append(lines[0])
                new_entry = ItemsTest(
                    item=lines[0],
                    price=lines[1],
                    quantity=lines[3],
                    link=lines[2]
                )
                counter +=1
                db.session.add(new_entry)
        print(counter)
        db.session.commit()


get_mge_wholesale_data()
