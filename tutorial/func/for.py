ages = [10, 20, 30, 40]
places = ["東京", "広島", "大阪", "京都"]

# for age,place in zip(ages,places):
#   if age >= 10 and place == places[0]:
#     print(f"私の年齢は{age}で、性別は{place}です。")

# for i , place in enumerate(places):
#   print(f'{i} => {place}')

# for place in reversed(places):
#   print(place)

# nums = [0,1,2,3,4,5]

# for num in nums[1:6:2]:
#   print(num)

# inclusive_notation = [ place for place in places ]
# print(f'私が住んだことのある場所は、{inclusive_notation}です。')

for age in ages:
    if age < 10:
        continue
    elif age >= 10 and age <= 30:
        print(age)
    else:
        break
