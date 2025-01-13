from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

date = datetime.now().date()
print(date)

# time = datetime.datetime(2024, 12, 10, 20, 15, 30, 2000)
# print(time)

# dt1 = datetime.datetime(2024, 12, 1, 1, 1, 1, 1000)
# dt2 = datetime.datetime(2024, 12, 2, 1, 1, 1, 1000)

# td = dt2 - dt1
# print(td)

# day = td.days
# print(day)

zi = datetime(2020, 10, 31, 12, tzinfo=ZoneInfo("Asia/Tokyo"))
print(zi)
zi_name = zi.tzname()
print(type(zi_name))


td_1w = timedelta(days=2, hours=3, minutes=4)
print(td_1w)

now = datetime.now(ZoneInfo("Asia/Tokyo"))
print(now)
