def add(*args):
    sum1 = 0
    for n in args:
        sum1 = sum1 + n
    return sum1


print(add(1, 2, 4, 5, 7))


def calculate(n, **kwargs):
    # for key, value in kwargs.items():
    #     print(key)
    #     print(value)
    n += kwargs["add"]
    n *= kwargs["multiply"]
    print(n)


calculate(2, add=3, multiply=5)


class Car:

    def __init__(self, **kwargs):
        self.model = kwargs["model"]
        self.make = kwargs["make"]
        self.colour = kwargs.get("colour")
        self.model = kwargs.get("model")
        self.make = kwargs.get("make")
        self.shape = kwargs.get("shape")


my_car = Car(model="i5", make="BMW", colour="black")
print(my_car.make)
print(my_car.model)
print(my_car.colour)
print(my_car.shape)

