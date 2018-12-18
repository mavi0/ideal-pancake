from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import os, errno, glob, sys
import schedule
import time
import atexit

main_errors = 0

def main():
    try:
        connData = json.loads(check_output(["curl", "-s", "http://172.17.83.2/cgi-bin/gws/monitor?1"]))

        tx = connData["Station"][0]["sta1tx"].split()
        rx = connData["Station"][0]["sta1rx"].split()

        connData["Station"][0]["tx_speed"] = tx[0]
        connData["Station"][0]["tx_MCS"] = tx[3]
        connData["Station"][0]["tx_pkts"] = tx[-2]

        connData["Station"][0]["rx_speed"] = rx[0]
        connData["Station"][0]["rx_MCS"] = rx[3]
        connData["Station"][0]["rx_pkts"] = rx[-2]

        print(connData)
    except:
        print ("An error occured trying to capture the data from the BTS")
        print ("This was error %d of 3. After 3 attempts, credentials authentication will be tried")


def exit_safe():
    print ("An unrecoverable error occured. Clearing up results directory.")
    files = glob.glob('results_6H/*')
    for f in files:
        os.remove(f)

# run every 1 minute

atexit.register(exit_safe)
schedule.every(1).minutes.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)



# r = requests.get("http://172.17.83.2/cgi-bin/gws/monitor?1")
# r.json()
# print(r)



# Start FireFox in headless mode
# options = Options()
# options.headless = True
# driver = webdriver.Firefox(options=options)
#
# # load credentials from file
# with open('config/credentials.json') as cred:
#     credentials = json.load(cred)
#
# # Connect to login page
# driver.get("http://172.17.83.2/gws")
# print ("Headless Firefox Initialized")
#
# # Pass in login credentials
# username = driver.find_element_by_name('username')
# username.send_keys("admin")
# password = driver.find_element_by_name('password')
# password.send_keys("quick007")
# signInButton = driver.find_element_by_id('login')
# signInButton.click()
# for i in range(20):
#     print(i)
#     driver.get_screenshot_as_file('6h-%s.png' % i)
