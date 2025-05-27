def is_prime(num):
    """指定された数値が素数かどうかを判定します。"""
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def print_primes(limit):
    """指定された上限までの素数を表示します。"""
    print(f"Primes up to {limit}:")
    for number in range(2, limit + 1):
        if is_prime(number):
            print(number)

# 例: 30までの素数を表示
print_primes(30)
