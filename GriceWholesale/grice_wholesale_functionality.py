import selenium.common.exceptions
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import csv
import os
global master_list


def get_grice_wholesale_data():
    from flask_login import current_user
    URL = "https://gricewholesale.com/customer/account/login/"
    # Loading the webpage
    s = Service("C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/chromedriver")
    chrome_driver_path = "C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/chromedriver"

    # Getting login info using environment variables
    EMAIL = os.getenv("EMAIL_SECOND")
    PASSWORD = os.getenv("PASSWORD")

    driver = webdriver.Chrome(service=s)
    driver.get(URL)
    driver.maximize_window()
    time.sleep(1)

    # Filling in the email and passwords
    email_field = driver.find_element(By.NAME, "login[username]")
    email_field.send_keys(EMAIL)
    time.sleep(1)
    password_field = driver.find_element(By.NAME, "login[password]")
    password_field.send_keys(PASSWORD)
    time.sleep(1)

    # Clicking the Sign In Button
    sign_in_button = driver.find_element(By.XPATH,
                                         "/html/body/div[3]/main/div[3]/div/div[2]"
                                         "/div[1]/div[2]/form/fieldset/div[6]/div[1]/button/span")
    sign_in_button.click()

    # Random sleep to mess with getting denied
    import random
    random.randint(1, 9)
    time.sleep(.5)

    # Clicking on the Firearms Tab
    time.sleep(2)
    try:
        firearms_tab = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div/div[2]/nav/ul/li[1]/a/span[2]")
        firearms_tab.click()
    except selenium.common.exceptions.NoSuchElementException:
        time.sleep(6)
        firearms_tab = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div/div[2]/nav/ul/li[1]/a/span[2]")
        firearms_tab.click()
    time.sleep(.5)

    # Setting up the master dictionary
    master_dict = {}

    # INTERATION FROM HERE DOWN TO GET THE DATA
    # Creating loop, if the total number of items <= items shown, proceed
    total_items = int(driver.find_element(By.XPATH, "/html/body/div[3]/main/div/div[1]/div[2]/p/span[3]").text)
    items_shown = int(driver.find_element(By.XPATH, "/html/body/div[3]/main/div/div[1]/div[2]/p/span[2]").text)

    # Need to use next toward the bottom of the loop, n is to allow dictionary to scale above 12
    global next_page
    previous_items_shown = 0
    n = 1

    # Iterating through the pages to get the data
    while total_items > items_shown:
        if total_items == items_shown:
            driver.quit()
        time.sleep(.2)

        try:
            items_shown = int(driver.find_element(By.XPATH, "/html/body/div[3]/main/div/div[1]/div[2]/p/span[2]").text)
        # Adding the items_show line to make sure the while loop ends
        # Otherwise, the errors hit and it retries again
        except selenium.common.exceptions.NoSuchElementException:
            driver.quit()
            break
            # Below is old way to end the loop
            # items_shown += 1, 000, 000
        except selenium.common.exceptions.InvalidSessionIdException:
            driver.quit()
            break
            # Below is old way to end the loop
            # items_shown += 1, 000, 000
        except AttributeError:
            items_shown += 12
            break
            # Below is old way to end the loop
            # items_shown += 1, 000, 000
        except TimeoutError:
            driver.quit()
            print("Timeout Error, driver quit")
            break
            # Below is old way to end the loop
            # items_shown += 1, 000, 000
        except ConnectionRefusedError:
            driver.quit()
            print("ConnectionRefusedError, driver quit")
            break
            # Below is old way to end the loop
            # items_shown += 1, 000, 000
        # except selenium.common.exceptions.

        # Print statement a test, delete later
        iteration = items_shown / 12

        # Getting each item (Details, Price, Link, Stock Status) and putting into lists to pair weapon with price
        name_caliber_and_type = driver.find_elements(By.CSS_SELECTOR, ".product-item-name")
        cost = driver.find_elements(By.CLASS_NAME, "price")
        link_to_firearm_unorganized = driver.find_elements(By.CLASS_NAME, "product-item-info")
        stock_status_unorganized = driver.find_elements(By.CSS_SELECTOR, ".actions-primary")

        # Organizing stock statuses
        stock_status = []
        for status in stock_status_unorganized:
            new_status = status.text
            if new_status != "":
                stock_status.append(new_status)
            else:
                stock_status.append("Not Avaliable")

        # Organizing Links
        links_to_firearms = []
        for links in link_to_firearm_unorganized:
            new_link = links.find_element(By.TAG_NAME, "a")
            new_link_text = new_link.get_attribute("href")
            links_to_firearms.append(new_link_text)

        # Categories in all lists
        list_categories = ["firearm_type", "price", "link", "stock_status"]

        # Organizing Dictionary of Details, Price, and Links
        # Was rewriting over the same 12 parts of the dictionary, had to create another loop to add to the initial key
        # previous_items_shown is the iteration multiplier, added to below
        for n in range(len(name_caliber_and_type)):
            try:
                master_dict[n + previous_items_shown] = {
                    "firearm_type": name_caliber_and_type[n].text,
                    "price": cost[n].text,
                    "link": links_to_firearms[n],
                    "stock_status": stock_status[n],
                }
            except IndexError:
                master_dict[n + previous_items_shown] = {
                    "firearm_type": "Firearm Type Unavaliable",
                    "price": "Price Unavaliable",
                    "link": "Link Unavaliable",
                    "stock_status": "Stock Status Unavaliable",
                }
            except selenium.common.exceptions.StaleElementReferenceException:
                time.sleep(4)
                master_dict[n + previous_items_shown] = {
                    "firearm_type": name_caliber_and_type[n].text,
                    "price": cost[n].text,
                    "link": links_to_firearms[n],
                    "stock_status": stock_status[n],
                }

        # Using this as a counter
        previous_items_shown = int((iteration * 12))
        if iteration == 1:
            next_page = driver.find_element(By.XPATH, f"/html/body/div[3]/main/div/div[1]/div[2]/div[4]/ul/li[6]/a")
            time.sleep(.5)
            next_page.click()
            time.sleep(.5)
        elif iteration > 1:
            try:
                next_page = driver.find_element(By.XPATH, f"/html/body/div[3]/main/div/div[1]/div[2]/div[4]/ul/li[7]/a")
                time.sleep(.5)
                next_page.click()
                time.sleep(.5)
            # The below prevents an exception from crashing the program after the last page has been reached,
            # then closes the selenium program
            except selenium.common.exceptions.NoSuchElementException:
                driver.quit()
            except ConnectionRefusedError:
                driver.quit()


    # Converting the dicts of dicts to a list of dicts
    master_list = [value for value in master_dict.values()]

    # Preping to Write
    headers = list_categories

    with open(r"C:\Users\Owen\Documents\Personal Info\Independent Courses\Python Learning\fflwholesalerproductpps\Data\WholesalerReports\grice_wholesale_data.csv", "w", newline="") as file:
        csv_writer = csv.DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        csv_writer.writerows(master_list)


