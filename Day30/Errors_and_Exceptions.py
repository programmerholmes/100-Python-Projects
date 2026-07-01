# try:
#     file = open("a_file.txt")
#     a_dict = {"Key": "value"}
#     print(a_dict["Key"])
#
# except FileNotFoundError:
#     file = open("a_file.txt", "w")
#     file.write("Something")
#
# except KeyError as error_message:
#     print(f"The key {error_message} does not exist.")
#
# else:
#     content = file.read()
#     print(content)
#
# finally:
#     file.close()
#     print("File was closed!")
#     # raise TypeError("This is an error that I made up!")

height = float(input("Enter height:"))
weight = int(input("Enter weight:"))

if height > 3:  # 3 meters
    raise ValueError

bmi = weight / height ** 2
print(bmi)