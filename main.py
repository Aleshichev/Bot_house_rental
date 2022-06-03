from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


MY_GOOGLE_URL = 'https://forms.gle/PD3REvVfsVtEdouB6'
MY_ZILLOW_URL = 'https://www.zillow.com/jacksonville-fl/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Jacksonville%2C%20FL%22%2C%22mapBounds%22%3A%7B%22west%22%3A-82.17509801953125%2C%22east%22%3A-81.20280798046875%2C%22south%22%3A30.00990853811457%2C%22north%22%3A30.674788745731608%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A25290%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'


header = {
        "User-Agent": 'USER_AGENT',
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8"
}
response = requests.get(MY_ZILLOW_URL, headers=header)

soup = BeautifulSoup(response.content, "html.parser")
# print(response)
price_list = []
price_data = soup.find_all("div", class_="list-card-price")

for price in price_data:
    if "+" in price.get_text():
        one_price = price.get_text().split("+")[0]
        price_list.append(one_price)
    elif "/" in price.get_text():
        one_price = price.get_text().split("/")[0]
        price_list.append(one_price)
print(len(price_list))

address_data = soup.find_all("address", class_="list-card-addr")
address_list = [address.get_text()for address in address_data ]
# print(address_list)

link_data = soup.find_all("a", class_="list-card-link list-card-link-top-margin list-card-img")
time.sleep(2)
link_list = []
for linkt in link_data:
        linkt = linkt.get('href')
        if 'www' not in linkt:
                linkt = 'https://www.zillow.com' + linkt
        link_list.append(linkt)
# print(link_list)

s = Service('C:\Web development\chromedriver_win32\chromedriver.exe')
driver = webdriver.Chrome(service=s)

for n in range(0, len(address_list)):
        driver.get(MY_GOOGLE_URL)
        time.sleep(2)

        enter_address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        enter_address.send_keys(address_list[n])

        enter_price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        enter_price.send_keys(price_list[n])

        enter_link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        enter_link.send_keys(link_list[n])

        enter_push = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
        enter_push.click()


driver.quit()
