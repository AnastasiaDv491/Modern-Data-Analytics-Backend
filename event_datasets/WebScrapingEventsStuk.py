import requests
from bs4 import BeautifulSoup
import pandas as pd
import unittest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import time

names = []
datetime = []
addresses = []
locations =[]

# Selenium driver  is used to scroll beyond "more" button and get all the info
URL = "https://www.stuk.be/nl/agenda/archief/2022" # link to scrape
driver = webdriver.Chrome('chromedriver.exe') # initialization of the driver form this repo
try:
    # execute javascript to remove cookies banner and overlay
    driver.get(URL)
    driver.execute_script("""
    var element = document.querySelector(".cookiebanner");
    var overlay = document.querySelector(".cookie-overlay");
    if (element)
        element.parentNode.removeChild(element);

    if (overlay)
        overlay.parentNode.removeChild(overlay);

    """)
    # Include waiting for the driver to avoid overload of the website 
    wait = WebDriverWait(driver, 10)
    while True:
        # get the "more" button and click on it if it exists
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id= 'js-load-more']")))
        element.click()
        # include waiting of 10 sec between button clicks
        time.sleep(10)

# if there is no button element or timeout error then do
except (TimeoutException,NoSuchElementException):
    # creating an instance of BeautifulSoup to scrape overview page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # get HTML elements of the page and scrape data
    EventsStuk = soup.find_all('div', class_= 'card__body')
    for event in EventsStuk:
        name = event.h3.text.strip()
        meta_divs = event.find_all('div', class_='post-item__meta')
        address = 'Naamsestraat 96, 3000 Leuven'  
        organizer = "Stuk"
        eventtype = "Other"
        names.append(name)
        addresses.append(address)

    # get URL per card event on overview page & scrape the page behind it
    for url in soup.find_all('a', class_ = "card--link"):
        live_url = url["href"]
        # creating an instance of BeautifulSoup to scrape detailed page
        soup2 = BeautifulSoup(requests.get(live_url).content,'html.parser')
        for meta in soup2.find_all('div', class_ = "card__main"):
            if meta.find('div', class_="spacer") != None:
                locations.append(meta.find('div', class_="spacer").text.strip())
        
        
        if soup2.find("div", class_ ="text") != None:
            datetime.append(soup2.find("div", class_ ="text").text.strip())
    
    # create and save dataframe with scraped elements
    df = pd.DataFrame({'Name': names, 'Address': addresses, 'Date': datetime, "Location": locations, "Organizer" : organizer, "Event type": eventtype})
    df.to_csv('df_stuk.csv',index=False)

    # quit driver to avoid MultiEntries error
    driver.quit()
finally:
    driver.quit()

