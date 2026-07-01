from selenium import webdriver
from selenium.webdriver.ie.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchWindowException
import time


chrome_driver_path = r"C:\Development\chromedriver-win64\chromedriver.exe"

service = Service(executable_path=chrome_driver_path)

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# These lines are for google sign up without checking the secure browser
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://tinder.com/app/recs")
driver.fullscreen_window()
time.sleep(2)

email_value = "YOUR_EMAIL@gmail.com"
passw = "YOUR_PASSWORD"
number = "1234567890"

login = driver.find_elements(By.LINK_TEXT, "Log in")
for log in login:
    log.click()


"""
An <iframe> (Inline Frame): This is a separate HTML document embedded within the main page. Because it's a completely
separate document, Selenium's focus is on the main document and cannot "see" the elements inside the <iframe> until
you explicitly tell it to switch.
"""



# If the login box is not a new tab but a small box on the same page, it might be an <iframe>.
# You must switch contexts before finding the element.

iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe"))) # Use a more specific selector if possible!
#iframe = driver.find_element(By.TAG_NAME, "iframe") # if you wanna use this one then add time.sleep(some seconds) to pick it up, they both work

# 2. Switch focus into the iframe
driver.switch_to.frame(iframe)

# 3. NOW you can find and click the 'Continue with Google' button inside the iframe
google_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='container-div']/div/div[2]/span[1]")))
google_button.click()


# 4. CRITICAL: Switch back to the main page after the login prompt
driver.switch_to.default_content()


"""
Here we use the other approach of the new window, when there is a new window and not a portion in the same frame,
then we are not going to use the <iframe>, but the following approach, for a new window altogether.
"""


# original_window = driver.current_window_handle
#
# # B. Wait for the new window/tab to open
# # The number_of_windows_to_be(2) condition waits until two windows are open.
# wait = WebDriverWait(driver, 10)
# wait.until(EC.number_of_windows_to_be(2))
#
# # C. Switch to the new window
# for window_handle in driver.window_handles:
#     if window_handle != original_window:
#         driver.switch_to.window(window_handle)
#         break # Stop iterating once the switch is successful
# D. To switch back to the original browser window:
#driver.switch_to.window(original_window)

"""
The one on top worked, but it was only in case of one pop up window, e.g the email in our case, but if we have
more than one pop up windows, in that case the one on top doesn't work and need a little change in the code, we
need all the handlers now(handlers are just all the pop up windows), first there was only one so we didn't need to worry
but now it's 2 so, we need all of them. Here is the updated code now
"""

# 1. Store the handle of the ORIGINAL window (if you didn't already)
# This is the handle of the main browser window where you started the login.
original_window = driver.current_window_handle

# Get a list of all current window handles
all_handles = driver.window_handles

# Assume the current focus is still on the (now closed/transitioned) email pop-up.
# We need to find the one that is NOT the main window.
# The new password pop-up should be the only remaining secondary window.

# 2. Switch to the NEW pop-up window (the password screen)
wait = WebDriverWait(driver, 10)
wait.until(EC.number_of_windows_to_be(2))  # Wait until there are exactly 2 windows again

# Find the handle that is not the original one and switch to it.
for window_handle in all_handles:
    # IMPORTANT: You may need to adapt this logic if the number of windows changes.
    # A safer method is to switch to ALL handles and check the page title/URL
    # until you find the one for the password field.

    # For a simple two-window flow:
    if window_handle != original_window:
        driver.switch_to.window(window_handle)
        break  # Focus is now on the password pop-up


email = driver.find_element(By.ID, "identifierId")
print(email.send_keys(email_value))


next_click = driver.find_elements(By.XPATH, "//*[@id='identifierNext']/div/button/span")
for n in next_click:
    n.click()

wait.until(EC.number_of_windows_to_be(2))

# # Step B: Loop through a FRESH list of handles (THIS IS THE FIX)
# # We must call driver.window_handles AGAIN to get the handle of the NEW password pop-up.
# for handle in driver.window_handles:
#     # Check if the current handle is NOT the main Tinder window
#     if handle != original_window:
#         # Switch the driver's focus to the new pop-up
#         driver.switch_to.window(handle)
#
#         # We assume success and break the loop.
#         # (The element verification from before is the safer way, but let's try this simple switch first)
#         break

""" We are keeping the above because When the window the driver is focused on suddenly closes, the WebDriver 
(Selenium/Chromedriver) doesn't just crash; it automatically attempts to switch focus to the next available window 
(usually the main, surviving window—your ORIGINAL_WINDOW_HANDLE). So In summary: You got lucky! The automatic cleanup 
and element tracking of the modern WebDriver saved you from needing the second explicit loop.
Why the Explicit Loop is Still Best Practice
While your code is working perfectly now, relying on this "automatic switch" behavior is dangerous 
because it can fail unpredictably, If it fails, then we can use this extra loop
"""


"""
The Scenario Where Two Loops Are Mandatory
Your counter-scenario is precisely why the reusable switch function and a second loop are best practice:

Scenario: If the email pop-up had not closed (leaving 3 windows: Tinder, Email, Password), the single loop would fail 
to guarantee success.
"""

password_field = wait.until(EC.element_to_be_clickable((By.NAME, "Passwd")))
password_field.send_keys(passw)

next_click = driver.find_elements(By.XPATH, "//*[@id='passwordNext']/div/button/span")
for n in next_click:
    n.click()

time.sleep(5)

driver.switch_to.window(original_window)


phone = driver.find_element(By.ID, "phone_number")
phone.send_keys(number)

final_next = driver.find_element(By.XPATH, "//*[@id='o-886962194']/div/div[1]/div[2]/div/div[3]/button/div[2]/div[2]/div")
#final_next.send_keys(Keys.ENTER)
final_next.click()





# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service  # Corrected import for Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchWindowException
# import time
#
# # --- Configuration (Replace these placeholders) ---
# email_value = "YOUR_EMAIL@gmail.com"  # Use consistent naming
# passw = "YOUR_PASSWORD"
#
# # --- Selectors (CRITICAL: These must be 100% correct) ---
# # Main Page
# LOGIN_LINK_TEXT = "Log in"
# GOOGLE_BUTTON_XPATH = "//*[@id='container-div']/div/div[2]/span[1]"  # Your previous iframe selector (Keep if it works)
#
# # Google Pop-up
# EMAIL_FIELD_ID = "identifierId"
# PASSWORD_FIELD_NAME = "Passwd"  # Google uses 'Passwd' for the input name
# NEXT_BUTTON_XPATH = "//*[@id='identifierNext']/div/button"  # Generic Next button on Google login
#
# # --- SETUP ---
# chrome_driver_path = r"C:\Development\chromedriver-win64\chromedriver.exe"
# service = Service(executable_path=chrome_driver_path)
#
# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
# # Options to bypass Google's secure browser check
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
#
# driver = webdriver.Chrome(service=service, options=options)
# driver.get("https://tinder.com/app/recs")
# driver.fullscreen_window()
# wait = WebDriverWait(driver, 15)
#
# # 1. Capture the handle of the main application window ONCE
# ORIGINAL_WINDOW_HANDLE = driver.current_window_handle
#
#
# # --- REUSABLE WINDOW SWITCHING FUNCTION ---
# def switch_to_new_window(original_handle, unique_locator):
#     """
#     Waits for a new window to open and switches to it.
#     It verifies the switch by checking for a unique element on the new page.
#     Returns the handle of the new window.
#     """
#     # Wait for the number of windows to be 2 (one original + one pop-up)
#     wait.until(EC.number_of_windows_to_be(2))
#
#     new_window_handle = None
#
#     # Get a FRESH list of handles every time this function is called
#     for handle in driver.window_handles:
#         if handle != original_handle:
#             try:
#                 driver.switch_to.window(handle)
#                 # Check for a unique element (like the email/password field)
#                 wait.until(EC.presence_of_element_located(unique_locator))
#                 new_window_handle = handle
#                 print(f"SUCCESS: Switched to new window containing {unique_locator}")
#                 return new_window_handle
#             except (TimeoutException, NoSuchWindowException):
#                 # If the element is not found, or the window closed, continue to the next handle
#                 continue
#
#     # If the loop completes without finding the expected window
#     raise Exception(f"Failed to find and switch to new window with locator: {unique_locator}")
#
#
# # --- START LOGIN PROCESS ---
# try:
#     # 2. Click "Log in"
#     print("Step 2: Clicking main 'Log in' link.")
#     login_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, LOGIN_LINK_TEXT)))
#     login_link.click()
#
#     # 3. IFRAME HANDLING (Switch into iframe to click 'Continue with Google')
#     print("Step 3: Switching to iframe.")
#     iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe")))
#     driver.switch_to.frame(iframe)
#
#     # 4. Click the 'Continue with Google' button inside the iframe
#     print("Step 4: Clicking 'Continue with Google' inside iframe.")
#     google_button = wait.until(EC.element_to_be_clickable((By.XPATH, GOOGLE_BUTTON_XPATH)))
#     google_button.click()
#
#     # 5. Switch back to the main page content BEFORE switching windows
#     driver.switch_to.default_content()
#
#     # =========================================================================
#     # PHASE 1: EMAIL POP-UP SWITCH AND ENTRY
#     # =========================================================================
#
#     print("\n--- STARTING PHASE 1: Email Entry ---")
#
#     # 6. Switch to the new pop-up window (Email screen)
#     # The new handle is returned but not strictly needed unless we need to refer to it later
#     email_pop_up_handle = switch_to_new_window(
#         ORIGINAL_WINDOW_HANDLE,
#         (By.ID, EMAIL_FIELD_ID)  # Unique element to check for
#     )
#
#     # 7. Locate and enter the email address
#     print(f"Step 7: Entering email: {email_value}")
#     email_field = wait.until(EC.element_to_be_clickable((By.ID, EMAIL_FIELD_ID)))
#     email_field.send_keys(email_value)
#
#     # 8. Click the 'Next' button on the email screen
#     print("Step 8: Clicking 'Next' on email screen (triggers new pop-up).")
#     next_button_email = wait.until(EC.element_to_be_clickable((By.XPATH, NEXT_BUTTON_XPATH)))
#     next_button_email.click()
#
#     # Pause briefly to allow the old pop-up to close and the new one to open
#     # This is often needed when one window is instantly replaced by another
#     time.sleep(1)
#
#     # =========================================================================
#     # PHASE 2: PASSWORD POP-UP SWITCH AND ENTRY (The FIX for your issue)
#     # =========================================================================
#
#     print("\n--- STARTING PHASE 2: Password Entry ---")
#
#     # 9. SWITCH AGAIN! The previous pop-up is closed, so we must find the new one.
#     password_pop_up_handle = switch_to_new_window(
#         ORIGINAL_WINDOW_HANDLE,
#         (By.NAME, PASSWORD_FIELD_NAME)  # Unique element to check for
#     )
#
#     # 10. Enter the password
#     print("Step 10: Entering password.")
#     # Use the NAME selector, which is reliable for Google's password field
#     password_field = wait.until(EC.element_to_be_clickable((By.NAME, PASSWORD_FIELD_NAME)))
#     password_field.send_keys(passw)
#
#     # 11. Click the final 'Next' button
#     print("Step 11: Clicking final 'Next' button.")
#     next_button_password = wait.until(EC.element_to_be_clickable((By.XPATH, NEXT_BUTTON_XPATH)))
#     next_button_password.click()
#
#     # =========================================================================
#     # PHASE 3: CLEANUP
#     # =========================================================================
#
#     # 12. Close the password pop-up window
#     print("Step 12: Closing pop-up window.")
#     driver.close()
#
#     # 13. Switch focus back to the original application window
#     driver.switch_to.window(ORIGINAL_WINDOW_HANDLE)
#     print("Step 13: Successfully returned to the main window and login process is complete.")
#
# except Exception as e:
#     print(f"\nFATAL ERROR: An error occurred during the login process: {e}")
#
# finally:
#     # time.sleep(10) # Uncomment to keep browser open for inspection
#     # driver.quit()  # Uncomment this to close the browser after the process is done
#     pass