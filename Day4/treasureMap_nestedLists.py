row1 = ["💀","💀","💀"]
row2 = ["💀","💀","💀"]
row3 = ["💀","💀","💀"]
map = [row1, row2, row3]

print(f"{row1}\n{row2}\n{row3}")
position = input("Where do you want to put the treasure? :")

row = int(position[0])
column = int(position[1])
map[column - 1][row - 1] = "x"

#  OR
#
# sr = map[column - 1]
# sr[row - 1] = 'p'

print(f"{row1}\n{row2}\n{row3}")

