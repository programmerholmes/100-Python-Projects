from art import logo

def add(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2

operations = {
                "+": add,
                "-": subtract,
                "*": multiply,
                "/": divide,
             }

def calculator():
    print(logo)
    num1 = float(input("Enter your first number: "))

    for symbol in operations:
        print(symbol)

    operation_symbol = input("Choose an operation you wanna perform from the line above: ")

    num2 = float(input("Enter your second number: "))

    calculation_function = operations[operation_symbol]

    first_answer = calculation_function(num1, num2)
    print(f"{num1} {operation_symbol} {num2} = {first_answer}")

    flag = True
    while flag == True:
        choice = input(f"Type 'y' to continue calculating with {first_answer}, type 'n' to exit or start a new"
                       f"calculator.: ").lower()
        if choice == 'y':

            operation_symbol = input("Pick another operation: ")
            num3 = int(input("Enter your number: "))

            calculation_function = operations[operation_symbol]
            second_answer = calculation_function(first_answer, num3)
            print(f"{first_answer} {operation_symbol} {num3} = {second_answer}")
            first_answer = second_answer
        else:
            flag = False
            calculator()

calculator()