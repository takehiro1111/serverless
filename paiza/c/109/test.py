import re

text = "paiza1 pizza99"
numbers = re.findall(r"\d+", text)
print(numbers)  # 出力: ['1', '99']

user_id = ["tanaka2", "tanaka1"]
sorted_users = sorted(user_id, key=lambda x: int("".join(filter(str.isdigit, x))))
print(sorted_users)
