# コンポジションを使用した例
class Engine:
    def start(self):
        print("エンジン始動")

    def stop(self):
        print("エンジン停止")


class Car:
    def __init__(self):
        # Carクラスは Engineクラスのインスタンスを持つ
        self.engine = Engine()

    def start_car(self):
        self.engine.start()
        print("車の電装系起動")

    def stop_car(self):
        self.engine.stop()
        print("車の電装系停止")


if __name__ == "__main__":
    # Carのインスタンスを作成
    car = Car()

    # 車を始動
    print("=== 車を始動します ===")
    car.start_car()

    print("\n=== 車を停止します ===")
    car.stop_car()
