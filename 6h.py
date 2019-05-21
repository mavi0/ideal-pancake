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
logging.basicConfig(format='[%(levelname)s] %(asctime)s %(message)s ',filename='6h.log',level=logging.INFO)

def mail(content):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "a09.athena@gmail.com"  # Enter your address
    receiver_email = "ellie@mavieson.co.uk"  # Enter receiver address
    password = "@oMr^&pcS$rhCM85O#PaG7c&gT$Z2oWGgNsqRc#%"
    message = content

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def get_data(hostname, file):
    logging.info ("Connecting to 172.17.82.2")
    # subprocess.check_output(["curl", "-s", "https://172.17.83.2/cgi-bin/gws/monitor?1"])
    # curl -k -s https://172.17.83.10/gws/ -c cookiefile -d "user=admin&pass=quick007"
    # curl -k -s https://172.17.83.10/cgi-bin/gws/monitor?1 -b cookiefile
    
    connData = json.loads(subprocess.check_output(["curl", "-k", "-s", "https://172.17.83.2/cgi-bin/gws/monitor?1"]))

    tx = connData["Station"][0]["sta1tx"].split()
    rx = connData["Station"][0]["sta1rx"].split()
    snr = connData["Station"][0]["sta1snr"].split()

    connData["Station"][0]["tx_speed"] = tx[0]
    connData["Station"][0]["tx_MCS"] = tx[3].replace(",", "")
    connData["Station"][0]["tx_pkts"] = tx[-2]

    connData["Station"][0]["rx_speed"] = rx[0]
    connData["Station"][0]["rx_MCS"] = rx[3].replace(",", "")
    connData["Station"][0]["rx_pkts"] = rx[-2]

    connData["Station"][0]["rssi"] = snr[0]
    connData["Station"][0]["floor"] = snr[3]
    connData["Station"][0]["snr"] = snr[7]

    logging.info(connData)

    with open('results_6H/' + file, 'w') as json_file:
        json.dump(connData, json_file)

    main_errors = 0
    logging.info ("Completed witout errors.")

        

def six_harmonics(hostname, file):
    main_errors = 0
    for main_errors in range(0, 3):
        try:
            get_data(hostname, file)
            break

        except:
            logging.warning ("An error occured trying to capture the data from the BTS")
            try:
                os.remove("results/6h.json")
            except OSError:
                pass


            # mail("""\
            # Subject: 6H Bardney Monitoring WARNING

            # WARNING

            # 6H Bardney monitoring script is failing, action may be required""")

            logging.info ("This was error %s of 3. After 3 attempts, credentials authentication will be tried" % main_errors)

            if ( main_errors  > 2 ):
                logging.info ("Attempting to authenticate with BTS...")
                try:
                    # Start FireFox in headless mode
                    options = Options()
                    options.headless = True
                    driver = webdriver.Firefox(options=options)

                    logging.info("FireFox Initialized")
                    driver.get("http://" + hostname + "/gws")
                    logging.info ("Connected to BTS")

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

                    logging.info("Authentication was successful!")
                    logging.info("Attempting to get data from BTS one final time")
                    get_data()
                    main_errors = 0
                except:
                    logging.critical ("Couldn't connect to BTS. Program will exit.")
                    mail("""\
                    Subject: 6H Bardney Monitoring FAIL

                    CRITICAL FAIL

                    6H Bardney monitoring script has failed, action is required now""")
                    files = glob.glob('results_6H/*')
                    for f in files:
                        os.remove(f)
                    sys.exit()


def main():
    try:
        with open('6h.json') as hosts_file:
            hosts = json.load(hosts_file)
    except:
        hosts = {}

    try:
        for i in hosts["radios"]:
            six_harmonics(i["ip"], i["file"])
    except:
        print("Main loop exception")

main()


