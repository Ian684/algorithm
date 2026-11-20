"""Algorithm exercise 01: linear search."""

def linear_search(items, target):
    return next((i for i, value in enumerate(items) if value == target), -1)


if __name__ == "__main__":
    print("Exercise 01: " + __name__)
