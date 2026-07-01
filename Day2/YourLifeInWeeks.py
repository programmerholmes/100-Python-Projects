age = input("What's your current age? ")
days = 365
weeks = 52
months = 12
max_limit = 90
remaining_age_in_years = max_limit - int(age)
age_in_weeks = remaining_age_in_years * weeks
age_in_days = remaining_age_in_years * days
age_in_months = remaining_age_in_years * months
message = (f"You have {age_in_days} days, {age_in_weeks} weeks, and {age_in_months} months left.")
print(message)