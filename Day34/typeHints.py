def police_check(age: int) -> bool:         # the hyphen means that it is expecting this result
    if age > 18:
        return True
    else:
        return False


if police_check(19):
    print("Let him go")
else:
    print("Pay the fine")
