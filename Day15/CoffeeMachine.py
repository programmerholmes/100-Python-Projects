MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

resources["money"] = 0

quarter = 0.25
dime = 0.10
nickle = 0.05
pennie = 0.01

start = True
while start != False:

    coins = 0

    drink = input("What would you like? (espresso/latte/cappuccino): ").lower()

    if drink == "espresso":
        if resources["water"] >= MENU["espresso"]["ingredients"]["water"] and \
           resources["coffee"] >= MENU["espresso"]["ingredients"]["coffee"]:
            print("Please enter coins.")
            quarters = float(input("How many quarters?: "))
            quarters = quarters * quarter
            dimes = float(input("How many dimes?: "))
            dimes = dimes * dime
            nickles = float(input("How many nickles?: "))
            nickles = nickles * nickle
            pennies = float(input("How many pennies?: "))
            pennies = pennies * pennie
            coins = quarters + dimes + nickles + pennies
            cost = MENU["espresso"]["cost"]
            if coins >= cost:
                coins = coins - cost
                coins = round(coins, 2)
                resources["money"] += cost
                resources["water"] -= MENU["espresso"]["ingredients"]["water"]
                resources["coffee"] -= MENU["espresso"]["ingredients"]["coffee"]
                print(f"Here is ${coins} in change.")
                print("Here is your Espresso ☕️! Enjoy")
            else:
                print("Sorry that's not enough money. Money refunded.")
        else:
            if resources["water"] < MENU["espresso"]["ingredients"]["water"]:
                print("Sorry there is not enough water.")
            if resources["coffee"] >= MENU["espresso"]["ingredients"]["coffee"]:
                print("Sorry there is not enough coffee.")

    elif drink == "latte":
        if resources["water"] >= MENU["latte"]["ingredients"]["water"] and \
           resources["milk"] >= MENU["latte"]["ingredients"]["milk"] and \
           resources["coffee"] >= MENU["latte"]["ingredients"]["coffee"]:
            print("Please enter coins.")
            quarters = float(input("How many quarters?: "))
            quarters = quarters * quarter
            dimes = float(input("How many dimes?: "))
            dimes = dimes * dime
            nickles = float(input("How many nickles?: "))
            nickles = nickles * nickle
            pennies = float(input("How many pennies?: "))
            pennies = pennies * pennie
            coins = quarters + dimes + nickles + pennies
            cost = MENU["latte"]["cost"]
            if coins >= cost:
                coins = coins - cost
                coins = round(coins, 2)
                resources["money"] += cost
                resources["water"] -= MENU["latte"]["ingredients"]["water"]
                resources["milk"] -= MENU["latte"]["ingredients"]["milk"]
                resources["coffee"] -= MENU["latte"]["ingredients"]["coffee"]
                print(f"Here is ${coins} in change.")
                print("Here is your Latte ☕️! Enjoy")
            else:
                print("Sorry that's not enough money. Money refunded.")
        else:
            if resources["water"] < MENU["latte"]["ingredients"]["water"]:
                print("Sorry there is not enough water.")
            if resources["milk"] < MENU["latte"]["ingredients"]["milk"]:
                print("Sorry there is not enough milk.")
            if resources["coffee"] < MENU["latte"]["ingredients"]["coffee"]:
                print("Sorry there is not enough coffee.")
    elif drink == "cappuccino":
        if resources["water"] >= MENU["cappuccino"]["ingredients"]["water"] and \
           resources["milk"] >= MENU["cappuccino"]["ingredients"]["milk"] and \
           resources["coffee"] >= MENU["cappuccino"]["ingredients"]["coffee"]:
            print("Please enter coins.")
            quarters = float(input("How many quarters?: "))
            quarters = quarters * quarter
            dimes = float(input("How many dimes?: "))
            dimes = dimes * dime
            nickles = float(input("How many nickles?: "))
            nickles = nickles * nickle
            pennies = float(input("How many pennies?: "))
            pennies = pennies * pennie
            coins = quarters + dimes + nickles + pennies
            cost = MENU["cappuccino"]["cost"]
            if coins >= cost:
                coins = coins - cost
                coins = round(coins, 2)
                resources["money"] += cost
                resources["water"] -= MENU["cappuccino"]["ingredients"]["water"]
                resources["milk"] -= MENU["cappuccino"]["ingredients"]["milk"]
                resources["coffee"] -= MENU["cappuccino"]["ingredients"]["coffee"]
                print(f"Here is ${coins} in change.")
                print("Here is your cappuccino ☕️! Enjoy")
            else:
                print("Sorry that's not enough money. Money refunded.")
        else:
            if resources["water"] < MENU["cappuccino"]["ingredients"]["water"]:
                print("Sorry there is not enough water.")
            if resources["milk"] < MENU["cappuccino"]["ingredients"]["milk"]:
                print("Sorry there is not enough milk.")
            if resources["coffee"] < MENU["cappuccino"]["ingredients"]["coffee"]:
                print("Sorry there is not enough coffee.")

    elif drink == "report":
        for key, value in resources.items():
            if key == "coffee":
                print(key, ": ", value, "g")
                continue
            elif key == "money":
                print(key, ": ", "$", value)
                continue
            print(key, ": ", value, "ml")

    elif drink == "off":
        start = False
