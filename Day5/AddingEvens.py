even = 0
for i in range(0, 101, 2):
    even = even + i
print(even)

even2 = 0
for i in range(0,101):
    if i % 2 == 0:
        even2 = even2 + i
print(even2)