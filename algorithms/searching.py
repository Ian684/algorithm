"""二分搜尋的邊界與第 k 小選擇；位置皆從 0 開始。"""


def lower_bound(values, target):
    """已排序陣列中，第一個 >= target 的位置；O(log n)。"""
    left, right = 0, len(values)
    while left < right:
        middle = (left + right) // 2
        if values[middle] < target:
            left = middle + 1
        else:
            right = middle
    return left


def upper_bound(values, target):
    """已排序陣列中，第一個 > target 的位置；O(log n)。"""
    left, right = 0, len(values)
    while left < right:
        middle = (left + right) // 2
        if values[middle] <= target:
            left = middle + 1
        else:
            right = middle
    return left


def binary_search(values, target):
    """找到時回傳最左位置，找不到回傳 -1；O(log n)。"""
    index = lower_bound(values, target)
    return index if index < len(values) and values[index] == target else -1


def rotated_search(values, target):
    """旋轉過且沒有重複值的遞增陣列，O(log n)。"""
    left, right = 0, len(values) - 1
    while left <= right:
        middle = (left + right) // 2
        if values[middle] == target:
            return middle
        if values[left] <= values[middle]:
            if values[left] <= target < values[middle]:
                right = middle - 1
            else:
                left = middle + 1
        elif values[middle] < target <= values[right]:
            left = middle + 1
        else:
            right = middle - 1
    return -1


def quickselect(values, k):
    """回傳排序後第 k 個值；平均 O(n)，最差 O(n²)，不改輸入。"""
    if not 0 <= k < len(values):
        raise IndexError('k is outside the sequence')
    remaining = list(values)
    while True:
        pivot = remaining[len(remaining) // 2]
        low = [x for x in remaining if x < pivot]
        equal = [x for x in remaining if x == pivot]
        if k < len(low):
            remaining = low
        elif k < len(low) + len(equal):
            return pivot
        else:
            k -= len(low) + len(equal)
            remaining = [x for x in remaining if x > pivot]
