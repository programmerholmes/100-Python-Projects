class User:
    def __init__(self, name):
        self.name = name
        self.is_logged_in = False


def is_authenticated_decorator(function):
    def wrapper(user):
        if user.is_logged_in == True:
            function(user)
    return wrapper



@is_authenticated_decorator
def create_blog_post(user):
    print(f"This is {user.name}'s new blog post.")


new_user = User("John")
new_user.is_logged_in = True
create_blog_post(new_user)


""" What i am about to do below is exactly, what i have
done above, the only difference is, is if you don't want
to specify the number of users, and if they are too many,
and rather than changing the names of the arguments each 
time, we would just use *args and **kwargs to make it simple
and beautiful"""

"""Now this way, if arguments are there, they are there,
if not, then not. No issues."""


class User:
    def __init__(self, name):
        self.name = name
        self.is_logged_in = False


def is_authenticated_decorator(function):
    def wrapper(*args, **kwargs):
        if args[0].is_logged_in == True:
            function(args[0])
    return wrapper



@is_authenticated_decorator
def create_blog_post(user):
    print(f"This is {user.name}'s new blog post.")


new_user = User("John")
new_user.is_logged_in = True
create_blog_post(new_user)


"""Another example"""


def logging_decorator(function):
    def wrapper(*args, **kwargs):
        print(f"You called {function.__name__}{args}")
        result = function(args[0], args[1], args[2])
        print(f"It returned: {result}")
    return wrapper


@logging_decorator
def a_function(a, b, c):
    return a * b * c


a_function(1, 2, 3)