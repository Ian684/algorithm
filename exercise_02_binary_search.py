"""Algorithm exercise 02: binary search."""

def binary_search(items, target):
    lo, hi = 0, len(items)
    while lo < hi:
        mid = (lo + hi) // 2
        if items[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo if lo < len(items) and items[lo] == target else -1


if __name__ == "__main__":
    print("Exercise 02: " + __name__)
