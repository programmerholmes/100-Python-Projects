from selenium import webdriver
from selenium.webdriver.ie.service import Service
from selenium.webdriver.common.by import By



chrome_driver_path = r"C:\Development\chromedriver-win64\chromedriver.exe"


service = Service(executable_path= chrome_driver_path)
options = webdriver.ChromeOptions()                             # cuz we're using chrome
options.add_experimental_option("detach", True)  # for the browser to not close after running the py script
driver = webdriver.Chrome(service=service, options=options)



driver.get("https://www.python.org/")
page_source = driver.page_source
#print(page_source)

# price = driver.find_element("id", "title")
# print(price.text)

# search_bar = driver.find_element("name", "q")
# print(search_bar.tag_name)
# print(search_bar.get_attribute("placeholder"))
#
# logo = driver.find_element(By.CLASS_NAME, "python-logo")
# print(logo.size)
#
# documentation_link = driver.find_element(By.CSS_SELECTOR, ".documentation-banner a")
# print(documentation_link.text)
#
# any = driver.find_element(By.ID, "content")
# print(any.text)
#
# bug_link = driver.find_element(By.XPATH, '//*[@id="site-map"]/div[2]/div/ul/li[3]/a')
# print(bug_link.text)

#  All of the above has another class elements, and works on all, and gives everything



#  The event dates

date_list = []
name_list = []
dates = driver.find_elements(By.CSS_SELECTOR, ".event-widget time")
names = driver.find_elements(By.CSS_SELECTOR, ".event-widget li a")
for date in dates:
    #print(date.get_attribute('datetime'))          # We don't need the attribute here, it's here for fun
    print(date.text)
    # date_list.append(date.text)    # We didn't even need to append it, as dates and names variables were already list


for name in names:
    print(name.text)
   # name_list.append(name.text)     # We didn't even need to append it, as dates and names variables were already list


events = {}

for i in range(0, 5):
    events[i] = {
       # 'time': date_list[i],           # if we remove the appends up there, then we have to add these .text
       # 'name': name_list[i],           # because the original dates and names are in different list forms

        'time': dates[i].text,
        'name': names[i].text,
    }

print(events)

#  This above process can also be done with dictionary comprehension, but that for another time hehe




driver.close()   #close closes the active tab
driver.quit()    # quit quits the entire browser