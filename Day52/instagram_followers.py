import time
from selenium import webdriver
from selenium.webdriver.ie.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException

CHROME_DRIVER_PATH = r"C:\Development\chromedriver-win64\chromedriver.exe"
EMAIL = "your_email@example.com"
username = "YOUR_INSTAGRAM_USERNAME"
passw = "YOUR_PASSWORD"
tester = "TARGET_ACCOUNT_USERNAME"

service = Service(executable_path=CHROME_DRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)



class InstaFollower:

    def __init__(self):
        self.driver = webdriver.Chrome(service=service, options=options)


    def login(self):
        self.driver.get("https://www.instagram.com/")

        time.sleep(3)

        user = self.driver.find_element(By.NAME, "username")
        user.click()
        user.send_keys(username)

        password = self.driver.find_element(By.NAME, "password")
        password.click()
        password.send_keys(passw)

        login = self.driver.find_element(By.XPATH, "//*[@id='loginForm']/div[1]/div[3]/button/div")
        # login.send_keys(Keys.ENTER)
        login.click()

    def find_followers(self):
        time.sleep(6)
        search_click = self.driver.find_elements(By.XPATH, "//a[contains(normalize-space(.), 'Search')]")  # this is a really good xpath format, didn't get it by copying
        time.sleep(2)
        for s in search_click:
            s.click()
            print("here")

        time.sleep(3)
        search = self.driver.find_element(By.XPATH, "//input[@placeholder='Search']")
        search.send_keys(tester)
        time.sleep(3)
        our_name = self.driver.find_element(By.XPATH, f"//a[contains(., '{tester}') and .//img]")
        time.sleep(3)
        our_name.send_keys(Keys.ENTER)

        time.sleep(2)

        followers = self.driver.find_element(By.XPATH, "//a[contains(@href, '/following/')]")
        followers.click()

        time.sleep(2)
        modal = self.driver.find_element(By.XPATH, "//div[@role='dialog']//div")
        for i in range(10):
            # In this case we're executing some Javascript, that's what the execute_script() method does.
            # The method can accept the script as well as a HTML element.
            # The modal in this case, becomes the arguments[0] in the script.
            # Then we're using Javascript to say: "scroll the top of the modal (popup) element by the height of the modal (popup)"
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)

            time.sleep(2)

    def follow(self):
        all_buttons = self.driver.find_elements(By.XPATH, "//button[contains(., 'Follow')]")
        for button in all_buttons:
            try:
                button.click()
                time.sleep(1)
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_elements(By.XPATH, "//button[contains(., 'Cancel')]")
                for cancel in cancel_button:
                    cancel.click()



bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()
