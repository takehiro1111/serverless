# def wrapper(func):
#   def inner(*args):
#     print('start_____________')
#     func(func)
#     print('end________________')
#   return inner

# def call_num(num):
#   print(num)


# wrapper(call_num)(2)


def start_end(func):
    def add_start_end(_text):
        print("start")
        func(_text)
        print("end")

        return _text

    return add_start_end


def print_text(text):
    print(text + "!!!!!!!!!!!!!!!")
    return text


result = start_end(print_text)("test")
print(result)
