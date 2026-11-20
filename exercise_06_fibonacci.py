"""Algorithm exercise 06: fibonacci."""

def fibonacci(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


if __name__ == "__main__":
    print("Exercise 06: " + __name__)
