def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("関数実行前の処理")
        result = func(*args, **kwargs)
        print("関数実行後の処理")
        return result

    return wrapper


@my_decorator  # execute_instance = my_decorator(test_function) が入っている状態と同等
def execute_instance():
    print("fuction execute")


# 実行
execute_instance()

# 関数実行前の処理
# fuction execute
# 関数実行後の処理
