from selenium import webdriver
from selenium.webdriver.ie.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


chrome_driver_path = r"C:\Development\chromedriver-win64\chromedriver.exe"

service = Service(executable_path=chrome_driver_path)

options = webdriver.ChromeOptions()

options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=service, options=options)

driver.get("http://orteil.dashnet.org/experiments/cookie/")

# buyCurser = driver.find_element(By.CSS_SELECTOR, "#buyCursor b")
# print(buyCurser.text.split('-')[1].strip())                      # strip is to remove the spaces, if any!
# curser_value = int(buyCurser.text.split('-')[1].strip())

# all_points = [None] * 8    # This because with an empty list, it was giving out of range error, so we specified the
#                             # size. But why didn't we add values from the beginning? Well i tried that, you can see it
#                             # later on down in the code, but then i couldn't replace the value from the function,
#                             # that's why this option seemed better, though there are other ways too. But this works
#                             # for now
#
# def buy_curser():
#     buyCurser = driver.find_element(By.CSS_SELECTOR, "#buyCursor b")
#     buyCurser.click()
#     curser_value1 = buyCurser.text.split('-')[1].strip()
#     curser_value = curser_value1.replace(',', '')
#     all_points[0] = int(curser_value)
#     print(curser_value)
#     return int(curser_value)
#
# # buyGrandma = driver.find_element(By.CSS_SELECTOR, "#buyGrandma b")
# # print(buyGrandma.text.split('-')[1].strip())
# # grandma_value = int(buyGrandma.text.split('-')[1].strip())
#
# def buy_grandma():
#     buyGrandma = driver.find_element(By.CSS_SELECTOR, "#buyGrandma b")
#     buyGrandma.click()
#     grandma_value1 = buyGrandma.text.split('-')[1].strip()
#     grandma_value = grandma_value1.replace(',', '')
#     all_points[1] = int(grandma_value)
#     return int(grandma_value)
#
#
# # buyFactory = driver.find_element(By.CSS_SELECTOR, "#buyFactory b")
# # print(buyFactory.text.split('-')[1].strip())
# # factory_value = int(buyFactory.text.split('-')[1].strip())
#
#
# def buy_factory():
#     buyFactory = driver.find_element(By.CSS_SELECTOR, "#buyFactory b")
#     buyFactory.click()
#     factory_value1 = buyFactory.text.split('-')[1].strip()
#     factory_value = factory_value1.replace(',', '')
#     print(factory_value)
#     all_points[2] = int(factory_value)
#    # all_points.append(int(factory_value))
#     return int(factory_value)
#
#
#
# # buyMine = driver.find_element(By.CSS_SELECTOR, "#buyMine b")
# # print(buyMine.text.split('-')[1].strip())
# # mine_value1 = (buyMine.text.split('-')[1].strip())
# # mine_value = int(mine_value1.replace(',', ''))              # These upcoming values have commas(,) in them
#                                                                     # so they can't be converted into ints, i.e why
#                                                                     # i need to replace the commas with no space.
#                                                                     # learning a lot
#
# def buy_mine():
#     buyMine = driver.find_element(By.CSS_SELECTOR, "#buyMine b")
#     buyMine.click()
#     mine_value1 = buyMine.text.split('-')[1].strip()
#     mine_value = mine_value1.replace(',', '')
#     all_points[3] = int(mine_value)
#     return int(mine_value)
#
#
# # buyShipment = driver.find_element(By.CSS_SELECTOR, "#buyShipment b")
# # print(buyShipment.text.split('-')[1].strip())
# # shipment_value1 = buyShipment.text.split('-')[1].strip()
# # shipment_value = int(shipment_value1.replace(',', ''))
#
#
# def buy_shipment():
#     buyShipment = driver.find_element(By.CSS_SELECTOR, "#buyShipment b")
#     buyShipment.click()
#     shipment_value1 = buyShipment.text.split('-')[1].strip()
#     shipment_value = shipment_value1.replace(',', '')
#     all_points[4] = int(shipment_value)
#     return int(shipment_value)
#
#
# # buyAlchemy_lab = driver.find_element(By.ID, "buyAlchemy lab")  # for some reason css selector doesn't work with
# # print(buyAlchemy_lab.text.split()[3])                                            # this one , so i have to use By.ID
# # alchemy_value1 = buyAlchemy_lab.text.split()[3]
# # alchemy_value = int(alchemy_value1.replace(',', ''))
#
# def buy_alchemy_lab():
#     buyAlchemy_lab = driver.find_element(By.ID, "buyAlchemy lab")
#     buyAlchemy_lab.click()
#     alchemy_lab_value1 = buyAlchemy_lab.text.split()[3]
#     alchemy_lab_value = alchemy_lab_value1.replace(',', '')
#     all_points[5] = int(alchemy_lab_value)
#     return int(alchemy_lab_value)
#
#
# # buyPortal = driver.find_element(By.CSS_SELECTOR, "#buyPortal b")
# # print(buyPortal.text.split('-')[1].strip())
# # portal_value1 = buyPortal.text.split('-')[1].strip()
# # portal_value = int(portal_value1.replace(',', ''))
#
# def buy_portal():
#     buyPortal = driver.find_element(By.CSS_SELECTOR, "#buyPortal b")
#     buyPortal.click()
#     portal_value1 = buyPortal.text.split('-')[1].strip()
#     portal_value = portal_value1.replace(',', '')
#     all_points[6] = int(portal_value)
#     return int(portal_value)
#
#
# # buyTime_machine = driver.find_element(By.ID, "buyTime machine")      # Same with this one, so have to do the same
# # print(buyTime_machine.text.split()[3])                                       # i think it's because of the space in the
# # time_machine_value1 = buyTime_machine.text.split()[3]                            # name of both of them
# # time_machine_value = int(time_machine_value1.replace(',', ''))
#
#
# def buy_time_machine():
#     buyTime_machine = driver.find_element(By.ID, "buyTime machine")
#     buyTime_machine.click()
#     time_machine_value1 = buyTime_machine.text.split()[3]
#     time_machine_value = time_machine_value1.replace(',', '')
#     all_points[7] = int(time_machine_value)
#     return int(time_machine_value)
#
#
# all_points[0] = buy_curser()
# all_points[1] = buy_grandma()
# all_points[2] = buy_factory()
# all_points[3] = buy_mine()
# all_points[4] = buy_shipment()
# all_points[5] = buy_alchemy_lab()
# all_points[6] = buy_portal()
# all_points[7] = buy_time_machine()
#
#
#
# # because the following was giving index out of range error, because we started with an empty list
#
# # all_points.append(buy_curser())
# # all_points.append(buy_grandma())
# # all_points.append(buy_factory())
# # all_points.append(buy_mine())
# # all_points.append(buy_shipment())
# # all_points.append(buy_alchemy_lab())
# # all_points.append(buy_portal())
# # all_points.append(buy_time_machine())
#
#
#
# #all_points = [buy_curser(), buy_grandma(), buy_factory(), buy_mine(), buy_shipment(), buy_alchemy_lab(), buy_portal(), buy_time_machine()]
#
# # Yeah, the above wasn't working, i mean it was, but not for our case of changing values. So had to change it.
#
# print(all_points)
#
#
#
#
# money = driver.find_element(By.ID, "money")
# print(money.text)
#
# my_money = 0
# cookie = driver.find_element(By.ID, "cookie")
# x = 0
# new_list = [None]
#
# timeout = time.time() + 2
# five_min = time.time() + 60*5 # 5minutes
#
# while True:
#     cookie.click()
#     my_money = money.text.replace(',', '')
#     total = int(my_money) + 1
#     print(total)
#     x += 1
#     print("x is: ", x)
#     time.sleep(0.5)
#     print("first here!")
#
#
#     if time.time() > timeout:
#         print("second here here!")
#
#         for i in range(len(all_points)):
#             if time.time() > timeout:
#                 if total >= all_points[i]:
#                     new_list[0] = i
#                     print("3rd here")
#
#             print("The value is: ", new_list)
#
#         # I just wanted to try switch cases here so
#
#                 #print("4th hereeeeeee")
#             if time.time() > timeout:
#                 match new_list:
#                     case [0]:
#                         buy_curser()
#
#                     case [1]:
#                         buy_grandma()
#
#                     case [2]:
#                         buy_factory()
#
#                     case [3]:
#                         buy_mine()
#
#                     case [4]:
#                         buy_shipment()
#
#                     case [5]:
#                         buy_alchemy_lab()
#
#                     case [6]:
#                         buy_portal()
#
#                     case [7]:
#                         buy_time_machine()
#
#         print("5th here")
#
#     print("6th here")


#all_points[chosen_index]()







"""
I had a different approach, even though i was pretty close, but i couldn't get it. Even my logic was exactly the
same but my approach was very different and i got stuck literally at the end, below is the code i copied and 
it works, better luck next time!
"""


# cookie = driver.find_element(By.ID, "cookie")
#
# # Get upgrade item ids.
# items = driver.find_elements(By.CSS_SELECTOR, "#store div")
# item_ids = [item.get_attribute("id") for item in items]
# print(item_ids)
#
# timeout = time.time() + 5
# five_min = time.time() + 60 * 5  # 5minutes
#
# while True:
#     cookie.click()
#
#     # Every 5 seconds:
#     if time.time() > timeout:
#
#         # Get all upgrade <b> tags
#         all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
#         #for prices in all_prices:
#             #print(prices.text)
#         item_prices = []
#
#         # Convert <b> text into an integer price.
#         for price in all_prices:
#             element_text = price.text
#             #print(element_text)
#             if element_text != "":
#                 cost = int(element_text.split("-")[1].strip().replace(",", ""))
#                 #print(cost)
#                 item_prices.append(cost)
#                 #print(item_prices)
#
#         # Create dictionary of store items and prices
#         cookie_upgrades = {}
#         for n in range(len(item_prices)):
#             cookie_upgrades[item_prices[n]] = item_ids[n]
#             #print(cookie_upgrades)
#
#         # Get current cookie count
#         money_element = driver.find_element(By.ID, "money").text
#         if "," in money_element:
#             money_element = money_element.replace(",", "")
#         cookie_count = int(money_element)
#
#         # Find upgrades that we can currently afford
#         affordable_upgrades = {}
#         for cost, id in cookie_upgrades.items():
#             if cookie_count > cost:
#                 affordable_upgrades[cost] = id
#
#         # Purchase the most expensive affordable upgrade
#         highest_price_affordable_upgrade = max(affordable_upgrades)
#         print(highest_price_affordable_upgrade)
#         to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]
#
#         driver.find_element(By.ID, to_purchase_id).click()
#
#         # Add another 5 seconds until the next check
#         timeout = time.time() + 5
#
#     # After 5 minutes stop the bot and check the cookies per second count.
#     if time.time() > five_min:
#         cookie_per_s = driver.find_element(By.ID, "cps").text
#         print(cookie_per_s)
#         break
#

# I'll give it another try, this time like the given code.


cookie = driver.find_element(By.ID, "cookie")
items = driver.find_elements(By.CSS_SELECTOR, "#store div")   # Another thing i found, we should go with the CSS
# items = driver.find_elements(By.ID, "store")                      # selector instead of the ID, because an ID only
items_id = []                                                       # gives us that unique ID in the attributes (even in
for item in items:                                                  # the loop), whereas the CSS selector gives us the
    #print(item.get_attribute("id"))                              # whole div, more flexible, which is what we need here
    items_id.append(item.get_attribute("id"))
print(items_id)

timeout = time.time() + 5               # 5 secs
five_min = time.time() +  60 * 5        # 5 min

while True:
    cookie.click()

    if time.time() > timeout:
        print("its been 5 seconds")

        # price list
        prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        price_list = []
        for price in prices:
            element_text = price.text

            if element_text != "":
                cost = int(element_text.split("-")[1].strip(" ").replace(",", ""))
                price_list.append(cost)

        print(price_list)

        # cookie dictionary
        cookie_upgrades = {}
        for i in range(len(price_list)):
            cookie_upgrades[price_list[i]] = items_id[i]


        print(cookie_upgrades)

        # money
        money_element = driver.find_element(By.ID, "money").text
        if ',' in money_element:
            money_element = money_element.replace(',', '')
        cookie_count = int(money_element)

        print(cookie_count)

        # affordable_upgrade = []
        #
        # for i in range(len(price_list)):
        #     if cookie_count > price_list[i]:
        #         affordable_upgrade.append(price_list[i])
        #         highest_price_affordable_upgrade = max(affordable_upgrade)

        # I did the affordable_upgrade with a list, and it works, now i'm gonna try to do it with a dictionary,
        # just cuz i can.

        affordable_upgrade = {}
        for key, value in cookie_upgrades.items():
            if cookie_count > key:
                affordable_upgrade[key] = value

        highest_price_affordable_upgrade = max(affordable_upgrade)
        print(affordable_upgrade)
        print(highest_price_affordable_upgrade)

        # Just to clarify, when you apply max function, it gives the highest of the keys and ignores the values by
        # default which is why are numbers(prices) are in keys and not values, if you're curious


        #if highest_price_affordable_upgrade in cookie_upgrades:        No need for this line as the greatest value is obviously in that dictionary
        to_purchase_id = cookie_upgrades[highest_price_affordable_upgrade]
        driver.find_element(By.ID, to_purchase_id).click()

        timeout = time.time() + 5

    if time.time() > five_min:
        cookie_per_s = driver.find_element(By.ID, "cps")
        print(cookie_per_s.text)
        break


