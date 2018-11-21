from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

# Start FireFox in headless mode
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

# Connect to login page
driver.get("http://172.17.55.8/cgi-bin/acn/")
print ("Headless Firefox Initialized")

# load credentials from file
with open('config/credentials.json') as cred:
    credentials = json.load(cred)

# Pass in login credentials
username = driver.find_element_by_name('username')
username.send_keys(credentials["username"])
password = driver.find_element_by_name('password')
password.send_keys(credentials["password"])
signInButton = driver.find_element_by_id('Apply')
signInButton.click()
# driver.get_screenshot_as_file('ignite.png')

# This var holds the base URL with the token needed for authentication
token_url = driver.current_url

# take the address of the script and a name to save as.
def get_json(addr, name):
    driver.get(token_url + addr)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    element = soup.get_text("div", {"id": "json"})
    # print(element)
    f = open('results/%s.json' % name, 'w')
    f.write(element)
    f.close()
    return json.loads(element)

# get dict for both 5ghz and 60ghz
sixty = get_json("/admin/status/connected_clients_metro?ifname=radio1&freq=60", "60ghz")
five = get_json("/admin/status/connected_clients?ifname=ath0", "5ghz")

# Need a separate json file for each mac
# Init the arrays
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


if (sixty_ghz_mac == {}):
    print(five_ghz_mac)

print(five["clients"][0]['mac'])
print(len(five["clients"]))

for i in five["clients"]:
    print(i)
    if i['mac'] in five_ghz_mac:
        print("exists!")
        five_ghz_mac[i['mac']] = 1

    else:
        print("not exists!")
        five_ghz_mac[i['mac']] = 2


print(five_ghz_mac)
print("but we continue")



# driver.get(token_url + "/admin/status/connected_clients_metro?ifname=radio1&freq=60")
# # driver.get_screenshot_as_file('ignite.png')
# soup = BeautifulSoup(driver.page_source, "html.parser")
# element = soup.get_text("div", {"id": "json"})
# print(element)
# f = open('60ghz.json', 'w')
# f.write(element)
# f.close()
#
# driver.get(token_url + "/admin/status/connected_clients?ifname=ath0")
# soup = BeautifulSoup(driver.page_source, "html.parser")
# element = soup.get_text("div", {"id": "json"})
# print(element)
# f = open('5ghz.json', 'w')
# f.write(element)
# f.close()

driver.quit()
