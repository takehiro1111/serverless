class Person:
    def __init__(self):
        self.t = 30

    @staticmethod
    def birthday(year):
        print(f"私の誕生日は{year}です。")


Person.birthday("3月")
