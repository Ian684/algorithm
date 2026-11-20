"""Algorithm exercise 28: greatest common divisor."""

def greatest_common_divisor(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


if __name__ == "__main__":
    print("Exercise 28: " + __name__)
