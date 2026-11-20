"""Algorithm exercise 03: bubble sort."""

def bubble_sort(items):
    result = items.copy()
    for end in range(len(result), 1, -1):
        for i in range(end - 1):
            if result[i] > result[i + 1]:
                result[i], result[i + 1] = result[i + 1], result[i]
    return result


if __name__ == "__main__":
    print("Exercise 03: " + __name__)
