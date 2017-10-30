from fetchHitsory import sync
import datetime
from time import sleep

now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day
hours = range(4, 24)

for hour in hours:
    sync(day, month, year, hour)
    
while True:
    now = datetime.datetime.now()
    sync(now.day, now.month, now.year, now.hour)
    sleep(10)