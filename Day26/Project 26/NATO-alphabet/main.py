student_dict = {
    "student": ["Angela", "James", "Lily"], 
    "score": [56, 76, 98]
}

#Looping through dictionaries:
for (key, value) in student_dict.items():
    #Access key and value
    pass

import pandas
student_data_frame = pandas.DataFrame(student_dict)

#Loop through rows of a data frame
for (index, row) in student_data_frame.iterrows():
    #Access index and row
    #Access row.student or row.score
    pass

# Keyword Method with iterrows()
# {new_key:new_value for (index, row) in df.iterrows()}

#TODO 1. Create a dictionary in this format:
#{"A": "Alfa", "B": "Bravo"}

data = pandas.read_csv("nato_phonetic_alphabet.csv")
#print(data)

data_letter = data["letter"].to_list()
#print(data_letter)

data_code = data["code"].to_list()
#print(data_code)

dic = {}
new_dict = {}
for i in range(26):
    dic = {data_letter[i]: data_code[i]}
    new_dict.update(dic)
print(new_dict)
# OR
new_d = {row.letter: row.code for (index, row) in data.iterrows()}
print(new_d)
#TODO 2. Create a list of the phonetic code words from a word that the user inputs.

word = input("Enter any word: ").upper()
# phonetic_code_list = []
# for i in word:
#     phonetic_code_list.append(new_dict[i])
# print(phonetic_code_list)

# OR
phonetic_code_list = [new_dict[i] for i in word]
print(phonetic_code_list)
