from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import os, errno
import schedule
import time

# Start FireFox in headless mode
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

# load credentials from file
with open('config/credentials.json') as cred:
    credentials = json.load(cred)

# Connect to login page
driver.get("http://172.17.83.2/gws")
print ("Headless Firefox Initialized")

# Pass in login credentials
username = driver.find_element_by_name('username')
username.send_keys("admin")
password = driver.find_element_by_name('password')
password.send_keys("quick007")
signInButton = driver.find_element_by_id('login')
signInButton.click()
for i in range(20):
    print(i)
    driver.get_screenshot_as_file('6h-%s.png' % i)
