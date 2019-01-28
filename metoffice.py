from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os, errno
import schedule
import time
import logging
logging.basicConfig(format='[%(levelname)s] %(asctime)s %(message)s ',filename='met.log',level=logging.INFO)

# Start FireFox in headless mode
def main():
    try:
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        logging.info ("Headless Firefox Initialized")
        driver.get("https://www.metoffice.gov.uk/public/weather/observation/map/gcx2t2dez#?zoom=9&lat=53.53&lon=-0.82&map=Rainfall")
        logging.info ("Connected to 'https://www.metoffice.gov.uk/public/weather/observation/map/gcx2t2dez#?zoom=9&lat=53.53&lon=-0.82&map=Rainfall'")
        driver.find_element_by_class_name('as-oil__btn-optin').click()
        logging.info("Closed cookies")
        driver.execute_script("window.scrollTo(0, 530)")
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info("Saving %s.png to file" % time)
        driver.get_screenshot_as_file('met/%s.png' % time)
        logging.info ("Quitting Firefox...")
        driver.quit()
    except:
        print("An error occured, attempting to continue")

main()
