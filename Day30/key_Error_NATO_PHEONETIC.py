import pandas

data = pandas.read_csv("nato_phonetic_alphabet.csv")

new_d = {row.letter: row.code for (index, row) in data.iterrows()}
print(new_d)

# check = False
# while not check:
#     word = input("Enter any word: ").upper()
#
#     try:
#         phonetic_code_list = [new_d[i] for i in word]
#         check = True
#     except KeyError:
#         print("Sorry, only letters in the alphabet please.")
#     else:
#         print(phonetic_code_list)


# OR

def generate_phonetic():
    word = input("Enter any word: ").upper()

    try:
        phonetic_code_list = [new_d[i] for i in word]
    except KeyError:
        print("Sorry, only letters in the alphabet please.")
        generate_phonetic()
    else:
        print(phonetic_code_list)


generate_phonetic()
