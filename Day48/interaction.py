from selenium import webdriver
from selenium.webdriver.ie.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_driver_path = r"C:\Development\chromedriver-win64\chromedriver.exe"

service = Service(executable_path=chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service= service, options= options)

driver.get("https://en.wikipedia.org/wiki/Main_Page")

count = driver.find_element(By.ID, "articlecount")
print(count.text)

count1 = driver.find_elements(By.CSS_SELECTOR, "#articlecount a")
for counti in count1:
    print(counti.text)

#count.click()                           # It clicks on the anything that is passed.

# driver.close()

# But clicking is such a common function that selenium actually has another easy way of doing it for simplicity
# find method for links, makes it all so easy for real. A click() works on anything, doesn't have to be a link
# specifically. But in order to use LINK_TEXT, it has to have a link, or it won't work

talk = driver.find_element(By.LINK_TEXT, "Talk")    # through link text
#talk.click()


# That was clicking on websites, now if you want to type on the website, to write some text on it, then we again
# first have to find the place where it is(typing area), no easy way here. but then the next line does it, so

search = driver.find_element(By.NAME, "search")

real_press = driver.find_element(By.LINK_TEXT, "Search")
real_press.click()


search.send_keys("Python")
search.send_keys(Keys.ENTER)


# Just for disclaimer, this send_keys wasn't working and now it is, didn't change anything, just worked 5 mins later
# own it's own, probably went crazy


