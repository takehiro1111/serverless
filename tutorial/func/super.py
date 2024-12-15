# class Character():
#     def __init__(self, name, hp, mp):
#         self.name = name
#         self.hp = hp
#         self.mp = mp

#     def showCharacterInfo1(self):
#         print(f"charactor_parent: {self.name}")
#         print(f"HP_parent: {self.hp}")
#         print(f"MP_parent: {self.mp}")

#     def hello(self):
#           print(f"私は{self.name}です。世界を旅することが好きです。")

# class Hero(Character):
#     def __init__(self,name,hp,mp,job):
#       super().__init__(name,hp,mp)
#       self.job = job

#     def showCharacterInfo2(self):
#         super().showCharacterInfo1()
#         print(f"職業： {self.job}")

#     def hello(self):
#         print("私は勇者です。世界を救います！")


# hero = Character("探検家", "300", "150")
# hero.hello()

# child_hero = Hero("勇者",1000,1200,"俳優")
# child_hero.hello()
# child_hero.showCharacterInfo2()

class Animal(object):
    def __init__(self, name):
        self.name = name
        
    def __del__(self):
      print('デストラクタ')
      
    def name1(self):
      print(f'私の名前は{self.name}')

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # 親クラスのコンストラクタを呼び出す
        self.breed = breed
    
    def show_breed(self):
      print(self.breed)

# 動作確認
dog = Dog("tanaka","tiwawa")

dog.name1()
dog.show_breed()
