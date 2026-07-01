from selenium import webdriver
from selenium.webdriver.ie.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


chrome_driver_path = r"C:\Development\chromedriver-win64\chromedriver.exe"

service = Service(executable_path=chrome_driver_path)

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=service, options=options)


driver.get("http://secure-retreat-92358.herokuapp.com/")
#print(driver.page_source)

fname = "haha"
lname = "hehe"
emaill = "hahahehe@hehehaha.com"

first_name = driver.find_element(By.NAME, "fName")
last_name = driver.find_element(By.NAME, "lName")
email = driver.find_element(By.NAME, "email")
#sign_up = driver.find_element(By.CLASS_NAME, "btn-block")
#or
sign_up = driver.find_element(By.CSS_SELECTOR, "form button")


first_name.send_keys(fname)
last_name.send_keys(lname)
email.send_keys(emaill)
# sign_up.send_keys(Keys.ENTER)
# or
sign_up.click()