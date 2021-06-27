import requests
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ======================================== PIXELA ACCOUNT DETAILS ======================================================

# You will input your pixela details below
USERNAME = ""
TOKEN = ""
GRAPH_ID = ""

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

headers = {
    "X-USER-TOKEN": TOKEN
}

# ========================================== SELENIUM SETTINGS ========================================================


URL = f"https://pixe.la/v1/users/{USERNAME}/graphs/{GRAPH_ID}.html"

# You will need to add your chromedriver path here, download - https://chromedriver.chromium.org/downloads
# Reference - 100 days of code - Day 49 - Class 412
# Example DRIVER_PATH = "C:\development\chromedriver.exe"
DRIVER_PATH = ""

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(DRIVER_PATH, options=chrome_options)


def scrape(number):
    """Use selenium to scrape PIXELA and get the data for today, overall and total recorded days"""
    driver.get(URL)
    today_time = driver.find_element_by_id("stats-todays-count-0").text
    total_time = driver.find_element_by_id("stats-total-0").text
    days_recorded = driver.find_element_by_id("stats-total-pixels-0").text

    # Data before update
    if number == 1:
        print(f"Currently you have coded a total of {total_time} minutes and recorded over {days_recorded} days of "
              f"coding")

    # Data after update
    else:
        print(f"{when} you coded {today_time} minutes, with a new total of {total_time} minutes and recorded over "
              f"{days_recorded} days of coding")


# ======================================== CREATE PIXEL AT PIXELA =====================================================


start = input(f"Hi {USERNAME}, Would you like to start Habit Tracker with PIXELA? Yes or No? : ").lower()

if start == "yes":
    today = None
    scrape(1)

    process = input("What would you like to do? Add, Amend or Delete? : ").lower()
    if process == "add":
        when = input(f"When would you like to {process}? Today, Yesterday or Backdate? : ").lower()
        if when == "today":
            today = datetime.now()
        elif when == "yesterday":
            today = datetime.now() - timedelta(days=1)
        elif when == "backdate":
            today = datetime(year=2021, month=int(input("Please add a month number (Exp: 8) : ")),
                             day=int(input("Please add a day number (Exp: 8) : ")))
        else:
            print("Not valid selection, please try again")

        pixel_creation_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"

        pixel_data = {
            "date": today.strftime("%Y%m%d"),
            "quantity": input(f"How many min did you code {when}? : ")
        }

        response = requests.post(url=pixel_creation_endpoint, json=pixel_data, headers=headers)
        print(response.text)

        see_graph = input("Would you like to see the graph? Yes or No : ").lower()

        if see_graph == "yes":
            driver = webdriver.Chrome(DRIVER_PATH)
            driver.get(URL)
        else:
            scrape(2)
            print(f"See you again tomorrow {USERNAME}!")

    elif process == "amend":
        today = datetime(year=2021, month=int(input("Please add a month number (Exp: 8) :  ")),
                         day=int(input("Please add a number (Exp: 8) :  ")))
        update_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}"

        new_pixel_data = {
            "quantity": input("How many min did you code? : ")
        }

        response = requests.put(url=update_endpoint, json=new_pixel_data, headers=headers)
        print(response.text)
        scrape(1)

    elif process == "delete":
        today = datetime(year=2021, month=int(input("Please add a month number (Exp: 8) :  ")),
                         day=int(input("Please add a day number (Exp: 8) :  ")))
        delete_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}"

        response = requests.delete(url=delete_endpoint, headers=headers)
        print(response.text)
        scrape(1)

    else:
        print("Something went wrong")

else:
    graph = input(f"Would you like to see the graph? Yes or No? : ").lower()
    if graph == "yes":
        driver = webdriver.Chrome(DRIVER_PATH)
        driver.get(URL)
