# anime= [
#         ('CO', 'Comedy'),
#         ('MY', 'Mystery'),
#         ('LO', 'Love'),
#         ('DR', 'Drama'),
#         ('SP', 'Sport'),
#         ('CO', 'Comedy'),
#         ('MY', 'Mystery'),
#         ('LO', 'Love'),
#         ('DR', 'Drama'),
#         ('SP', 'Sport'),
#         ('CO', 'Comedy'),
#         ('MY', 'Mystery'),
#         ('LO', 'Love'),
#         ('DR', 'Drama'),
#         ('SP', 'Sport'),
#         ('CO', 'Comedy'),
#         ('MY', 'Mystery'),
#         ('LO', 'Love'),
#         ('DR', 'Drama'),
#         ('SP', 'Sport'),
#     ]

# naru_items = [item for item in anime if item[1] == 'Comedy']
# for item in naru_items[:5]:
#             print(item)


def fibonacci_sequence_iterative(n):
    if n <= 0:
        print("Please enter a positive integer")
    elif n == 1:
        print("Fibonacci sequence up to 1:")
        print(0)
    else:
        print("Fibonacci sequence:")
        a = 0
        b = 1
        count = 0
        while count < n:
            print(a)
            nth = a + b
            # update values
            a = b
            b = nth
            count += 1

fibonacci_sequence_iterative(10)

def iterative_factorial(n):
    if n < 0:
        return "Factorial is not defined for negative numbers"
    elif n == 0:
        return 1
    else:
        factorial = 1
        for i in range(1, n + 1):
            factorial *= i
        return factorial

num = 5
result = iterative_factorial(num)
print(f"The factorial of {num} is {result}")



def is_prime(number):

    # Check for factors from 5 onwards with a step of 6
    # This optimization checks numbers of the form 6k ± 1
    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 10
    return True

# Example usage:
num = 1113
if is_prime(num):
    print(f"{num} is a prime number.")
else:
    print(f"{num} is not a prime number.")