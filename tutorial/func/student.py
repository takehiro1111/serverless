from dataclasses import dataclass


@dataclass
class Student:
    name: str

    def calculateAVG(name, data):
        sum = 0
        for i in data:
            sum += i
        avg = sum / len(data)
        return avg

    def judge(name, avg):
        result = "pass" if avg >= 60 else "failed"
        return result


a001 = Student("sato")
data = [70, 65, 10, 50, 30]

avg = a001.calculateAVG(data)
result = a001.judge(avg)

print(avg)
print(f"{a001.name} -> {result}")


print(R"年齢は30歳です" + r"\\")
