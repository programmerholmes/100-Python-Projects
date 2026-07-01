from art import logo

print(logo)

def caesar(cipher_direction, start_text, shift_amount):
    end_text = ""
    if cipher_direction == "decode":
        shift_amount = shift_amount * -1
    for letter in start_text:
        if letter in alphabet:
            position = alphabet.index(letter)
            new_position = position + shift_amount
            new_letter = alphabet[new_position]
            end_text = end_text + new_letter
        else:
            end_text += letter
    print(f"The {cipher_direction}d text is {end_text}")



alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
            'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

should_contunue = True
while should_contunue:
    direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
    text = input("Type your message:\n").lower()
    shift = int(input("Type the shift number:\n"))

    shift = shift % 26

    caesar(direction, text, shift)

    result = input("Type 'yes' if you want to go again. Otherwise type 'no'.\n")
    if result == "no":
        should_contunue = False
        print("GoodBye!")




# def encrypt(plain_text, shift_amount):
#     cipher_text = ""
#     for letter in plain_text:
#         position = alphabet.index(letter)
#         new_position = position + shift_amount
#         new_letter = alphabet[new_position]
#         cipher_text = cipher_text + new_letter
#     print(f"The encoded text is {cipher_text}")
#
#
# def decrypt(cipher_text, shift_amount):
#     original_text = ""
#     for letter in cipher_text:
#         position = alphabet.index(letter)
#         new_position = position - shift_amount
#         new_letter = alphabet[new_position]
#         original_text = original_text + new_letter
#     print(f"The decoded text is {original_text}")