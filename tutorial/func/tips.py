# import os
 
# os.environ["STAGE"] = "stg"
 
# print(f"ENV: {os.environ["STAGE"]}")

l = [1,2,3]

if len(l) > 2:
  print(len(l))
  
# セイウチ演算子で冗長性を排除
if (i := len(l)) > 2:
  print(i)
