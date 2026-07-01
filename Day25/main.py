# with open("weather_data.csv") as file:
#     data = file.readlines()
#     print(data)

# import csv
# with open("weather_data.csv") as file:
#     data = csv.reader(file)
#     #print(data)
#     temperatures = []
#     for row in data:
#         if row[1] != "temp":
#             temperatures.append(int(row[1]))
#             print(row)
#     print(temperatures)


import pandas
data = pandas.read_csv("weather_data.csv")
print(data)
print("\n")
print(data["temp"])


# data_dictionary = data.to_dict()
# data_list = data["temp"].to_list()
# print("\n")
# print(data_dictionary)
# print(data_list)
#
# data_average = sum(data_list) / len(data_list)
# print(data_average)
#
# average = data["temp"].mean()
# print(average)
#
# max_value = data["temp"].max()
# print(max_value)
#
# print(data["condition"])
# print(data.condition)
#
# print(data[data["temp"] == data["temp"].max()])
# print(data[data.temp == data["temp"].max()])
#
# monday = data[data.day == "Monday"]
# print(monday.condition)
#
# Monday_temp_in_F = monday.temp * 1.8 + 32
# print(Monday_temp_in_F)
#
#
# data_dict = {
#     "students": ["Amy", "James", "Angela"],
#     "scores": [76, 56, 65]
# }
#
# data = pandas.DataFrame(data_dict)
# data.to_csv("newfile.csv")
