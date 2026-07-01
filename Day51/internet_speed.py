import time
from selenium import webdriver
from selenium.webdriver.ie.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



PROMISED_DOWN = 150
PROMISED_UP = 10
CHROME_DRIVER_PATH = r"C:\Development\chromedriver-win64\chromedriver.exe"
TWITTER_EMAIL = "YOUR_EMAIL@gmail.com"
passw = "YOUR_PASSWORD"

service = Service(executable_path=CHROME_DRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

#driver = webdriver.Chrome(service=service, options=options)

class InternetSpeedTwitterBot:

    def __init__(self):
        self.driver = webdriver.Chrome(service=service, options=options)
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")

        time.sleep(3)
        go = self.driver.find_element(By.CLASS_NAME, "start-text")
        go.click()

        time.sleep(40)
        self.down = self.driver.find_element(By.XPATH, "//*[@id='container']/div[1]/div[3]/div/div/div/div[2]/div[2]/div/div[4]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span").text
        print("The download speed: ", self.down)

        self.up = self.driver.find_element(By.XPATH, "//*[@id='container']/div[1]/div[3]/div/div/div/div[2]/div[2]/div/div[4]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span").text
        print("The upload speed: ", self.up)


    def tweet_at_provider(self):
        self.driver.get("https://x.com/home")

        iframe = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe")))
        self.driver.switch_to.frame(iframe)
        google_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='container-div']/div/div[2]/span[1]")))
        google_button.click()
        self.driver.switch_to.default_content()

        original_window = self.driver.current_window_handle
        all_handles = self.driver.window_handles

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.number_of_windows_to_be(2))

        for window_handle in all_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break

        email = self.driver.find_element(By.ID, "identifierId")
        print(email.send_keys(TWITTER_EMAIL))

        next_click = self.driver.find_elements(By.XPATH, "//*[@id='identifierNext']/div/button/span")
        for n in next_click:
            n.click()

        wait.until(EC.number_of_windows_to_be(2))

        password_field = wait.until(EC.element_to_be_clickable((By.NAME, "Passwd")))
        password_field.send_keys(passw)

        next_click = self.driver.find_elements(By.XPATH, "//*[@id='passwordNext']/div/button/span")
        for n in next_click:
            n.click()

        time.sleep(5)

        self.driver.switch_to.window(original_window)



        writing = self.driver.find_element(By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div[1]/div")
        writing.click()
        writing.send_keys( f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?")


        post = self.driver.find_element(By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button")
        post.click()

bot = InternetSpeedTwitterBot()
# bot.get_internet_speed()
# bot.tweet_at_provider()

# if you want this code to work, just uncomment the 2 lines above.

