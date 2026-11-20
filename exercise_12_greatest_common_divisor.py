"""Algorithm exercise 12: greatest common divisor."""

def greatest_common_divisor(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


if __name__ == "__main__":
    print("Exercise 12: " + __name__)
