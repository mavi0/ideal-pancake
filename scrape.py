from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import os, errno, glob, sys, smtplib, ssl
import schedule
import time
import atexit
import logging
logging.basicConfig(format='[%(levelname)s] %(asctime)s %(message)s ',filename='IgniteNet.log',level=logging.INFO)


# take the address of the script and a name to save as.
def get_json(addr, name, driver, token_url):
    driver.get(token_url + addr)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    element = soup.get_text("div", {"id": "json"})
    f = open('results/%s.json' % name, 'w')
    f.write(element)
    f.close()
    return json.loads(element)

# Load macs into dictionary - check for existing macs.
# 0 = default state
# 1 = matched to mac in the loaded dictionary
# 2 = new mac discovered //not really used
def load_macs(macs_dictionary, current_dictionary):
    for i in current_dictionary["clients"]:
        if i['mac'] in macs_dictionary:
            macs_dictionary[i['mac']] = 1
        else:
            macs_dictionary[i['mac']] = 2

    return macs_dictionary

# zero macs ready for saving to file for next execution - default state
def zero_macs(macs_dictionary):
    for i in macs_dictionary:
        macs_dictionary[i] = 0

    return macs_dictionary

# save method for macs
def save_macs(macs_dictionary, file_name):
    with open('config/%s.json' % file_name, 'w') as json_file:
        json.dump(zero_macs(macs_dictionary), json_file)

# export method for separating client entries into separate JSON files for ZABBIX to parse
# iterate over the clients array and match with a mac in the list of macs loaded.
# If the mac is 0 then it doesn't exist at the moment (the connection has dropped), so delete the file
def export_json(macs_dictionary, current_dictionary):
    for i in current_dictionary["clients"]:
        for j in macs_dictionary:
            if macs_dictionary[j] > 0 and i['mac'] == j:
                with open('results/%s.json' % j, 'w') as json_file:
                    json.dump(i, json_file)

            if macs_dictionary[j] == 0:
                try:
                    os.remove("results/%s.json" % j)
                except OSError:
                    pass

def clear_results():
    files = glob.glob('results/*')
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


def main():
    main_errors = 0

    for main_errors in range (0, 3):
        logging.info("Program started")

        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        # print("precred")
        try:
        # Start FireFox in headless mode
            # load credentials from file
            with open('config/credentials.json') as cred:
                credentials = json.load(cred)

            driver.get("http://google.com")
            driver.get_screenshot_as_file("google.png")

            # print("http://" + credentials['hostname'] + "/cgi-bin/acn/")
            # Connect to login page
            driver.get("http://" + credentials['hostname'] + "/cgi-bin/acn/")
            logging.info("Headless Firefox Initialized")
            driver.get_screenshot_as_file('preauth.png')


            # Pass in login credentials
            username = driver.find_element_by_name('username')
            username.send_keys(credentials["username"])
            password = driver.find_element_by_name('password')
            password.send_keys(credentials["password"])
            signInButton = driver.find_element_by_id('Apply')
            signInButton.click()
            driver.get_screenshot_as_file('afterauth.png')

            # This var holds the base URL with the token needed for authentication
            token_url = driver.current_url
            logging.info("Token: " + token_url)

            for i in range(10):
                if 'stok' not in token_url:
                    logging.warning("URL does not contain a token. Retrying...")
                    time.sleep(2)
                    token_url = driver.current_url
                    logging.info("Token: " + token_url)
                    driver.get_screenshot_as_file('afterauth%s.png', i)
                else:
                    break



            logging.info("Token: " + token_url)


            # get dict for both 5ghz and 60ghz
            # with open('results/60ghz.json') as cred:
            #     sixty = json.load(cred)
            sixty = get_json("/admin/status/connected_clients_metro?ifname=radio1&freq=60", "60ghz", driver, token_url)
            logging.info("Loaded 60GHz JSON")
            five = get_json("/admin/status/connected_clients?ifname=ath0", "5ghz", driver, token_url)
            logging.info("Loaded 5GHz JSON")
            # Load MAC dictionaries
            # Init the arrays if null
            try:
                with open('config/5ghz_MAC.json') as five_ghz_mac_raw:
                    five_ghz_mac = json.load(five_ghz_mac_raw)
            except:
                five_ghz_mac = {}

            try:
                with open('config/60ghz_MAC.json', newline='') as sixty_ghz_mac_raw:
                    sixty_ghz_mac = json.load(sixty_ghz_mac_raw)
            except:
                sixty_ghz_mac = {}


            # Load 5GHz MACs into dictionary
            five_ghz_mac = load_macs(five_ghz_mac, five)
            # Load 60GHz MACs into dictionary
            sixty_ghz_mac = load_macs(sixty_ghz_mac, sixty)
            logging.info("Loaded MACs from JSON")
            logging.info("60GHz MACS:")
            logging.info(sixty_ghz_mac)
            logging.info("5GHz MACS:")
            logging.info(five_ghz_mac)

            # export the arrays of clients as separate JSON files for 5GHz
            export_json(five_ghz_mac, five)
            # and 60GHz
            export_json(sixty_ghz_mac, sixty)
            logging.info("Exported JSON to files")

            # save current macs to file
            save_macs(five_ghz_mac, "5ghz_MAC")
            save_macs(sixty_ghz_mac, "60ghz_MAC")
            logging.info("Exported MAC config files")

            logging.info("Quiting Firefox...")
            driver.quit()

            # if we got to here it was a successful execution (no error occured)
            break

        except:
            driver.quit()
            logging.error ("An unrecoverable error occured during the program execution.")
            logging.warning ("This is likely due to transient network issues.")
            logging.warning ("Results from this execution cycle will be discarded (if they exist)")
            main_errors += 1
            logging.info ("This was failiure %s of 3. At 3 failiures the program will exit." % main_errors)
            if main_errors >= 3:
                logging.critical("Something broke :/")
                sys.exit()
                mail("""\
                    Subject: IgniteNet Auckley Monitoring FAIL

                    CRITICAL FAIL

                    IgniteNet Auckley monitoring script has failed to obtain data from the radio. Action may be required to fix the issue""")
                clear_results()

main()

# schedule.every(1).minutes.do(main)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
