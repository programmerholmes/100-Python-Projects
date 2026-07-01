numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

# squaring numbers

squared_numbers = [n * n for n in numbers]
#or
squared_numbers = [n ** 2 for n in numbers]

print(squared_numbers)


# printing even

results = [n for n in numbers if n % 2 == 0]

print(results)

# comparing lists from files

with open("file1.txt") as f1:
    data1 = f1.readlines()
    print(data1)

with open("file2.txt") as f2:
    data2 = f2.readlines()
    print(data2)

result = [int(num) for num in data1 if num in data2]
print(result)

