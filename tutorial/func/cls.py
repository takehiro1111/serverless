class MyClass:
    CLASS_PARAM = 100

    def __init__(self, value):
        self.value = value

    # 普通のメソッド（インスタンスが必要）
    def instance_method(self, multiplier):
        # インスタンス変数を利用可能
        return MyClass(self.value * multiplier)

    # クラスメソッド（インスタンス不要）
    @classmethod
    def class_method(cls, multiplier):
        # クラスオブジェクト (cls) を利用
        return cls(cls.CLASS_PARAM * multiplier)  # clsを利用して動的に呼び出す


# インスタンスを生成
general = MyClass(3)

# インスタンスメソッドから新しいインスタンスを生成
new_instance = general.instance_method(2)
print(new_instance)  # 出力: 200


# クラスメソッドを直接呼び出し
cls_instance = MyClass.class_method(2)
print(cls_instance.value)  # 出力: 200
