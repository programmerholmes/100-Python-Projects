from selenium import webdriver
from selenium.webdriver.ie.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


chrome_driver_path = r"C:\Development\chromedriver-win64\chromedriver.exe"

service = Service(executable_path=chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.linkedin.com/jobs/search/?currentJobId=4331138248&f_AL=true&keywords=coding&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true")


username = "your_email@example.com"
passw = "YOUR_PASSWORD"



cross = driver.find_element(By.CLASS_NAME, "contextual-sign-in-modal__modal-dismiss-icon")
#cross = driver.find_element(By.CLASS_NAME, "modal__dismiss")

cross.click()

sign_up = driver.find_element(By.LINK_TEXT, "Sign in")
sign_up.click()


email = driver.find_element(By.NAME, "session_key")
email.send_keys(username)

password = driver.find_element(By.NAME,"session_password")
password.send_keys(passw)


sign_in = driver.find_element(By.CLASS_NAME, "login__form_action_container ")
sign_in.click()