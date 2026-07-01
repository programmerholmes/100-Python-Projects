import random

names = input("Give me everybody's name, seperated by a comma!")
list_names = names.split(", ")                # the split function converts a string into the list
# print(list_names)

size = len(list_names)
random_names = random.randint(0, size - 1)
new_choice = list_names[random_names]
print(f"{new_choice} is going to pay the bill!")

# s = random.choice(L_names)            # trying without the choice function
#print(f"{s} is going to pay the bill!")