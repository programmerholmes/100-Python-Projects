numbers = [1, 2, 3]
new_list = []
for n in numbers:
    n = n + 1
    new_list.append(n)
print(new_list)

# OR list comprehension
# new_list = [n + 1 for n in numbers]

#list comprehension more stuff
# name = "Angela"
# new_list = [letter for letter in name]
# new_range = [i * 2 for i in range(1, 5)]
# names = ["Adil", "Basit", "Caroline", "Daud", "Ehtesham", "Fatima"]
# short_names = [name for name in names if len(name) < 5]
# caps_names = [caps.upper() for caps in names if len(caps) > 5]


