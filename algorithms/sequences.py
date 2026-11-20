"""前綴和、單調佇列、貪婪與分治以外的序列問題。"""
from collections import deque
import heapq


def prefix_sums(values):
    """O(n) 建立含前導 0 的表；sum[left:right]=prefix[right]-prefix[left]。"""
    result = [0]
    for value in values:
        result.append(result[-1] + value)
    return result


def sliding_maximum(values, width):
    """單調佇列，O(n) time/O(width) space；width 必須介於 1 與 n。"""
    if not 1 <= width <= len(values):
        raise ValueError('window outside sequence')
    queue, result = deque(), []
    for i, value in enumerate(values):
        while queue and queue[0] <= i - width:
            queue.popleft()
        while queue and values[queue[-1]] <= value:
            queue.pop()
        queue.append(i)
        if i >= width - 1:
            result.append(values[queue[0]])
    return result


def merge_intervals(intervals):
    """閉區間合併，端點相接也合併；O(n log n)。"""
    if any(start > end for start, end in intervals):
        raise ValueError('reversed interval')
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    return merged


def interval_scheduling(intervals):
    """最多不重疊的半開活動；O(n log n)，前一活動結束時可開始下一個。"""
    if any(start >= end for start, end in intervals):
        raise ValueError('activities must have positive duration')
    chosen, end = [], float('-inf')
    for activity in sorted(intervals, key=lambda pair: (pair[1], pair[0])):
        if activity[0] >= end:
            chosen.append(activity); end = activity[1]
    return chosen


def maximum_subarray(values):
    """Kadane 非空最大連續和；O(n)，空輸入拋錯，全負數仍保留一個元素。"""
    if not values:
        raise ValueError('non-empty sequence required')
    current = best = values[0]
    for value in values[1:]:
        current = max(value, current + value)
        best = max(best, current)
    return best


def huffman_cost(weights):
    """最優合併成本／Huffman 加權路徑長；非負權重，O(n log n)。"""
    if any(weight < 0 for weight in weights):
        raise ValueError('negative frequency')
    queue, total = list(weights), 0
    heapq.heapify(queue)
    while len(queue) > 1:
        merged = heapq.heappop(queue) + heapq.heappop(queue)
        total += merged
        heapq.heappush(queue, merged)
    return total
