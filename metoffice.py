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

# Start FireFox in headless mode
def main():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    print ("Headless Firefox Initialized")
    driver.get("https://www.metoffice.gov.uk/public/weather/observation/map/gcx2t2dez#?zoom=9&lat=53.53&lon=-0.82&map=Rainfall")
    driver.find_element_by_class_name('as-oil__btn-optin').click()
    driver.execute_script("window.scrollTo(0, 530)")
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Saving %s.png to file" % time)
    driver.get_screenshot_as_file('met/%s.png' % time)
    print ("Quitting Firefox...")
    driver.quit()

schedule.every(10).minutes.do(main)
# main()
while True:
    schedule.run_pending()
    time.sleep(1)
