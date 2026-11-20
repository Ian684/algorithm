"""比較排序與整數排序。函式都回傳新列表，不改動輸入。"""
import heapq


def insertion_sort(values):
    """O(n²) time, O(n) copy; 適合小量或接近有序的資料。"""
    result = list(values)
    for i in range(1, len(result)):
        value, j = result[i], i - 1
        while j >= 0 and result[j] > value:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = value
    return result


def merge_sort(values):
    """O(n log n) time, O(n) auxiliary space; 合併時先取左側以維持穩定。"""
    if len(values) < 2:
        return list(values)
    middle = len(values) // 2
    left, right = merge_sort(values[:middle]), merge_sort(values[middle:])
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]


def quick_sort(values):
    """三路分割，重複值直接歸到中段；平均 O(n log n)，最差 O(n²)。"""
    if len(values) < 2:
        return list(values)
    pivot = values[len(values) // 2]
    smaller = [x for x in values if x < pivot]
    equal = [x for x in values if x == pivot]
    larger = [x for x in values if x > pivot]
    return quick_sort(smaller) + equal + quick_sort(larger)


def heap_sort(values):
    """O(n log n) time, O(n) copy；練習 heapify 與連續取最小值。"""
    heap = list(values)
    heapq.heapify(heap)
    return [heapq.heappop(heap) for _ in range(len(heap))]


def counting_sort(values):
    """O(n + k)，k=max-min+1；支援負整數，不適合值域極大的資料。"""
    if not values:
        return []
    low, high = min(values), max(values)
    counts = [0] * (high - low + 1)
    for value in values:
        counts[value - low] += 1
    return [low + offset for offset, count in enumerate(counts) for _ in range(count)]


def radix_sort(values):
    """非負整數的 LSD 十進位排序，O(d(n+10))；每輪分桶保持穩定。"""
    if any(value < 0 for value in values):
        raise ValueError('radix_sort accepts non-negative integers')
    result, place = list(values), 1
    while result and max(result) >= place:
        buckets = [[] for _ in range(10)]
        for value in result:
            buckets[(value // place) % 10].append(value)
        result = [value for bucket in buckets for value in bucket]
        place *= 10
    return result
