s = 'TanakaTakehiro'
slice_obj = slice(2 ,5, None)

# スライスの範囲を明示的に計算
print(slice_obj.indices(len(s)))  # (0, 4, 1)

# スライス結果も確認
print(s[slice_obj.start:slice_obj.stop:slice_obj.step])  # 'Pyth'

print(len(s))
