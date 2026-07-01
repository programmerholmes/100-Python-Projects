print("Welcome to the love Calculator!")
name1 = input("What is your name? \n")
name2 = input("What is their name? \n")

true = 0
love = 0
name_combined = name1 + name2
name_in_lower = name_combined.lower()

t = name_in_lower.count("t")
r = name_in_lower.count("r")
u = name_in_lower.count("u")
e = name_in_lower.count("e")
true = t + r + u + e
l = name_in_lower.count("l")
o = name_in_lower.count("o")
v = name_in_lower.count("v")
e = name_in_lower.count("e")
love = l + o + v + e


print(true)
print(love)

con = str(true) + str(love)
# con = int(str(true) + str(love))
if int(con) < 10 or int(con) > 90:
    print(f"Your score is {con}%, you go together like coke and mentos.")
elif int(con) >= 40 and int(con) <= 50:
    print("Your score is " + con + "%, you are alright together.")
else:
    print(f"Your score is {con}%")