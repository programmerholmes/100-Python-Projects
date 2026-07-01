import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.ie.service import Service
from selenium.webdriver.common.by import By
# import lxml    ## sometimes html.parser doesn't work on some websites then we use lxml instead

CHROME_DRIVER_PATH = r"C:\Development\chromedriver-win64\chromedriver.exe"

service = Service(executable_path=CHROME_DRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)


driver = webdriver.Chrome(service=service, options=options)



form = "YOUR_GOOGLE_FORM_URL"

zillow = "https://www.zillow.com/los-angeles-ca/rent-houses/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-118.69161054563577%2C%22east%22%3A-118.0344907946592%2C%22south%22%3A33.829751404619266%2C%22north%22%3A34.28314360454924%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A12447%2C%22regionType%22%3A6%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22priorityscore%22%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A2%7D%2C%22baths%22%3A%7B%22min%22%3A2%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22usersSearchTerm%22%3A%22Los%20Angeles%20CA%22%2C%22mapZoom%22%3A11%7D"

headers = {
    "accept_language": "en-US,en;q=0.9",
    "user_agent":	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    #"accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "cookie": "YOUR_COOKIE_IF_NEEDED",
    "cache-control": "no-cache"

}

#driver.get(form)

response = requests.get(url=zillow, headers=headers)
zillow_webpage = response.text


soup = BeautifulSoup(zillow_webpage, "html.parser")
property_links = soup.select(".list-card-top a")
#print(property_links)


#print(soup.prettify())

"""So after working for hours and hours on this, it's not working, because zillow might've strickened their antiscrapping
policies, had they not been so strict, this could would have worked, now what i am going to do is, make a list manually
for the data, so i can still learn the next step of creating the sheets for practice"""

address_list = ["707 W 30th St, Los Angeles, CA 90007", "18138 Strathern St, Reseda, CA 91335",  "6929 1/2 Amigo Ave, Reseda, CA 91335"]
price_list = ["1500", "2000", "2700"]
link = ["https://www.zillow.com/homedetails/707-W-30th-St-Los-Angeles-CA-90007/2072583977_zpid/?utm_campaign=zillowwebmessage&utm_medium=referral&utm_source=txtshare" , "https://www.zillow.com/homedetails/18138-Strathern-St-Reseda-CA-91335/19903370_zpid/?utm_campaign=zillowwebmessage&utm_medium=referral&utm_source=txtshare" ,"https://www.zillow.com/homedetails/6929-1-2-Amigo-Ave-Reseda-CA-91335/353550609_zpid/?utm_campaign=zillowwebmessage&utm_medium=referral&utm_source=txtshare"]




for i in range(len(address_list)):
    driver.get(form)

    first_answer = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
    second_answer = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
    third_answer = driver.find_element(By.XPATH,"//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
    submit = driver.find_element(By.CLASS_NAME, "NPEfkd")

    time.sleep(2)

    first_answer.send_keys(address_list[i])
    second_answer.send_keys(price_list[i])
    third_answer.send_keys(link[i])
    submit.click()
    # another = driver.find_element(By.LINK_TEXT, "Submit another response")
    # another.click()