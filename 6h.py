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

main_errors = 0

def main():
    global main_errors
    try:
        print ("Connecting to 172.17.82.2")
        connData = json.loads(subprocess.check_output(["curl", "-s", "http://172.17.83.2/cgi-bin/gws/monitor?1"]))

        tx = connData["Station"][0]["sta1tx"].split()
        rx = connData["Station"][0]["sta1rx"].split()

        connData["Station"][0]["tx_speed"] = tx[0]
        connData["Station"][0]["tx_MCS"] = tx[3].replace(",", "")
        connData["Station"][0]["tx_pkts"] = tx[-2]

        connData["Station"][0]["rx_speed"] = rx[0]
        connData["Station"][0]["rx_MCS"] = rx[3].replace(",", "")
        connData["Station"][0]["rx_pkts"] = rx[-2]

        print(connData)

        with open('results_6H/6h.json', 'w') as json_file:
            json.dump(connData, json_file)

        main_errors = 0
        print("Completed witout errors.")

    except:
        print ("An error occured trying to capture the data from the BTS")
        mail("""\
        Subject: 6H Bardney Monitoring WARNING

        WARNING

        6H Bardney monitoring script is failing, action may be required""")
        main_errors += 1
        print ("This was error %d of 3. After 3 attempts, credentials authentication will be tried", main_errors)
        if ( main_errors  > 3 ):
            print("Attempting to authenticate with BTS...")
            try:
                # Start FireFox in headless mode
                options = Options()
                options.headless = True
                driver = webdriver.Firefox(options=options)

                # load crededtials from file
                #with open('config/credentials.json') as cred:
                #    credentials = json.load(cred)

                # Connect to login page
                print("Made it to pre get")
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

                main_errors = 0
            except:
                print("Couldn't connect to BTS. Program will exit.")
                mail("""\
                Subject: 6H Bardney Monitoring FAIL

                CRITICAL FAIL

                6H Bardney monitoring script has failed, action is required now""")
                sys.exit()

def exit_safe():
    print ("An unrecoverable error occured. Clearing up results directory.")
    files = glob.glob('results_6H/*')
    for f in files:
        os.remove(f)

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


# run every 1 minute

atexit.register(exit_safe)
schedule.every(1).minutes.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
