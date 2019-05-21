from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import os, errno, glob, sys, smtplib, ssl
import schedule, subprocess
import time
import atexit
import logging
logging.basicConfig(format='[%(levelname)s] %(asctime)s %(message)s ',filename='test.log',level=logging.DEBUG)


def main():
    # Start FireFox in headless mode
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    print("FireFox Initialized")
    driver.get("http://google.com")
    print("connected to google")
    driver.get_screenshot_as_file('google.png')
    # Pass in login credentials



main()
