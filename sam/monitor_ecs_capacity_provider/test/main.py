# import datetime

# day = datetime.datetime.now()
# weekday = day.strftime("%a")
# # 日付と曜日の表示形式を変更
# day_format = day.strftime("%Y/%-m/%-d") + f"({weekday})"
# print(type(day_format))
# print(day_format)

rules = [
    {"cluster": ["cluster-web"], "service": "nginx-service-stg"},
    {"cluster": ["cluster-web"], "service": "app-service-stg"},
    {"cluster": ["cluster-api"], "service": "api-service-stg"},
]

# これらは同じ結果になります
# all_rules = rules[0:]  # インデックス0から最後まで
all_rules = rules[:]["service"]  # 省略形（開始と終了インデックスを省略）

print(all_rules)

# rule['ecs_service'] = [{'cluster': ['cluster-web'], 'service': 'nginx-service-stg'}]
