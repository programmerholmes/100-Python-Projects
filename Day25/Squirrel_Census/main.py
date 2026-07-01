import pandas

data = pandas.read_csv("Central-Park-Squirrel-Census-Squirrel-Data.csv")


print(data["Primary Fur Color"])

data_fur = data["Primary Fur Color"].to_list()
print(data_fur)

gray = 0
cinnamon = 0
black = 0
red = 0
for fur in data_fur:
    if fur == "Gray":
        gray = gray + 1
    if fur == "Cinnamon":
        cinnamon = cinnamon + 1
    if fur == "Black":
        black = black + 1
    if fur == "Red":
        red = red + 1

# OR

# gray_squirrel_count = len(data[data["Primary Fur Color"] == "Gray"])
# cinnamon_squirrel_count = len(data[data["Primary Fur Color"] == "Cinnamon"])
# black_squirrel_count = len(data[data["Primary Fur Color"] == "Black"])
# print(gray_squirrel_count)
# print(cinnamon_squirrel_count)
# print(black_squirrel_count)

data_dict = {
    "Fur color": ["Gray", "Cinnamon", "Black"],
    "count": [gray, cinnamon, black]
}

shift = pandas.DataFrame(data_dict)
shift.to_csv("squirrel_count.csv")

