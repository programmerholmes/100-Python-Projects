def greet():
    print("Hello there!")
    print("How are you?")
    print("Nice to meet you!")

# greet()

def greet_with(name, location):
    print(f"Hello {name}")
    print("I heard you were from " + location)

greet_with("Angela", "London")
greet_with(location="London", name="Jack")