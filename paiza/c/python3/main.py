def fizz_buzz(i):
    if i % 3 == 0 and i % 5 == 0:
        return "FizzBuzz"
    elif i % 5 == 0:
        return "Buzz"
    elif i % 3 == 0:
        return "Fizz"
    else:
        return i


for x in range(1, 101):
    print(fizz_buzz(x))
