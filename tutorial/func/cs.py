class Person(object):
  def __init__(self):
    self.t = 30

  @staticmethod
  def birthday(year):
    print('私の誕生日は{}です。'.format(year))

Person.birthday('3月')
