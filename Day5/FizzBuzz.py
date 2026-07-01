for i in range(1, 101):
    if (i % 3 == 0) and (i % 5 == 0):
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 ==0:
        print("Buzz")
    else:
        print(i)

# OR
print("\n\n\n")
for i in range(1, 101):
    if (i % 3 == 0) and (i % 5 == 0):
        print("FizzBuzz")
        continue
    elif i % 3 == 0:
        print("Fizz")
        continue
    elif i % 5 ==0:
        print("Buzz")
        continue
    print(i)