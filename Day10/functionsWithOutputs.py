def format_name(f_name, l_name):
    """Takes a first and last name and converts it into a title case version of the name"""
    f_name = f_name.title()
    l_name = l_name.title()
    return f_name + " " + l_name



print(format_name("john", "doe"))


