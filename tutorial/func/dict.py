# zip関数を用いたキーバリューの結合
num = [1,2,3]
l = ['sato','suzuki','tanaka']

d = dict(zip(num,l))
print(d)

## キー、バリューの取り出し
dict = {
    "sports" : "soccer",
    "game" : "monsto",
    "anime" : "naruto"
}

print(dict.keys())
print(dict.values())
print(dict.items())

## getメソッド
### getメソッドは存在しないキーではNoneが返る。
### 第二引数で、存在しないキーを指定した場合の戻り値を書いておくことができます。
print(dict.get("game")) 
print(dict.get("animal","存在しないキーを指定しています。"))

for k,v in dict.items():
	print(k,v)

for i in dict.items():
	print(i)
 


dict.setdefault("iphone",12)



dict2 = {'pc': 'MacBookM3'}

dict.update(dict2)

print(dict)

population1 = {'東京':900, '横浜':370, '大阪':250, '名古屋':230, '福岡':150}
population2 = population1.copy()
population2.setdefault("add","add1")
print(population1)
print(population2)

