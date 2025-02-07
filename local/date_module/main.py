from datetime import timedelta, date

# Intelligent-Tieringになった最初の日
dt_1 = date(2025, 3, 4) # 3/3(月) # 2025-04-03 (土)
dt_2 = date(2025, 3, 5) # 26(水) # 2025-03-29 (土)
dt_3 = date(2025, 3, 6) # 25(火) # 2025-03-28 (金)


# 曜日マッピング（英語→日本語）
weekday_map = {
    "Mon": "(月)",
    "Tue": "(火)",
    "Wed": "(水)",
    "Thu": "(木)",
    "Fri": "(金)",
    "Sat": "(土)",
    "Sun": "(日)",
}

# 最短でストレージクラスが1階層下がる日(Intelligent-Tieringになった日 + 30日)
dates = [dt_1, dt_2, dt_3]

if __name__ == "__main__":
    for dt in dates:
        new_date = dt + timedelta(days=30)
        weekday = new_date.strftime("%a")
        print(f"{new_date} {weekday_map[weekday]}")


# # IntelligentTieringになった最初の日
# dt_0218 = date(year=2025, month=2, day=18)
# dt_0219 = date(year=2025, month=2, day=19)
# dt_0220 = date(year=2025, month=2, day=20)
# dt_0224 = date(year=2025, month=2, day=24)
# dt_0225 = date(year=2025, month=2, day=25)
# dt_0226 = date(year=2025, month=2, day=26)
# dt_0227 = date(year=2025, month=2, day=26)

# # 最短でストレージクラスが1階層下がる日(Intelligent-Tieringになった日 + 30日)
# new_date_0218 = dt_0218 + timedelta(days=30) 
# new_date_0219 = dt_0219 + timedelta(days=30) 
# new_date_0220 = dt_0220 + timedelta(days=30)
# new_date_0224 = dt_0224 + timedelta(days=30)
# new_date_0225 = dt_0225 + timedelta(days=30)
# new_date_0226 = dt_0226 + timedelta(days=30)
# new_date_0227 = dt_0227 + timedelta(days=30)

# if __name__ == "__main__":
#     print(new_date_0218)
#     print(new_date_0219)
#     print(new_date_0220)
#     print(new_date_0224)
#     print(new_date_0225)
#     print(new_date_0226)
#     print(new_date_0227)
