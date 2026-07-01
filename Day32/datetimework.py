#import datetime
import datetime as dt   # for simplicity

now = dt.datetime.now()
print(now)
year = now.year
month = now.month
day_of_the_week = now.weekday()
print(year)
print(month)
print(day_of_the_week)

date_of_birth = dt.datetime(year=2000, month=1, day=1, hour=12, minute=0)
print(date_of_birth)
