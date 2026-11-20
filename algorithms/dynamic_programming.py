"""把狀態定義寫在函式旁：先確定 dp 表示什麼，再決定迴圈方向。"""
from bisect import bisect_left


def lis_length(values):
    """嚴格遞增子序列長度；tails[i] 保存長度 i+1 的最小尾端，O(n log n)。"""
    tails = []
    for value in values:
        position = bisect_left(tails, value)
        if position == len(tails):
            tails.append(value)
        else:
            tails[position] = value
    return len(tails)


def lcs_length(a, b):
    """最長共同子序列長度；O(nm) time/O(m) space。"""
    previous = [0] * (len(b) + 1)
    for x in a:
        current = [0]
        for j, y in enumerate(b, 1):
            current.append(previous[j - 1] + 1 if x == y else max(previous[j], current[-1]))
        previous = current
    return previous[-1]


def edit_distance(a, b):
    """Levenshtein 距離：插入、刪除、替換各成本 1；O(nm) time/O(m) space。"""
    previous = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        current = [i]
        for j, y in enumerate(b, 1):
            current.append(min(previous[j] + 1, current[-1] + 1, previous[j - 1] + (x != y)))
        previous = current
    return previous[-1]


def knapsack(items, capacity):
    """0/1 背包 items=(weight,value)，非負整數重量；O(nC) time/O(C) space。"""
    if capacity < 0 or any(weight < 0 for weight, _ in items):
        raise ValueError('negative capacity or weight')
    best = [0] * (capacity + 1)
    for weight, value in items:
        for limit in range(capacity, weight - 1, -1):
            best[limit] = max(best[limit], best[limit - weight] + value)
    return best[-1]


def coin_change(coins, amount):
    """不限次數的最少硬幣數，無解回傳 None；O(kA) time/O(A) space。"""
    if amount < 0 or any(coin <= 0 for coin in coins):
        raise ValueError('amount must be non-negative; coins must be positive')
    best = [0] + [float('inf')] * amount

    for total in range(1, amount + 1):
        best[total] = min((best[total - coin] + 1 for coin in coins if coin <= total), default=float('inf'))
    return None if best[amount] == float('inf') else best[amount]


def subset_sum(values, target):
    """非負整數子集合和；整數 bitset，bit s 代表是否能湊到 s。"""
    if target < 0 or any(value < 0 for value in values):
        raise ValueError('non-negative values required')
    reachable, mask = 1, (1 << (target + 1)) - 1
    for value in values:
        if value <= target:
            reachable = (reachable | reachable << value) & mask
    return bool(reachable & (1 << target))


def matrix_chain(dimensions):
    """A_i 大小 dimensions[i]×dimensions[i+1]，最少純量乘法數；O(n³)。"""
    if any(d <= 0 for d in dimensions):
        raise ValueError('matrix dimensions must be positive')
    n = len(dimensions) - 1
    if n < 1:
        return 0
    best = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1
            best[left][right] = min(best[left][k] + best[k + 1][right] + dimensions[left] * dimensions[k + 1] * dimensions[right + 1] for k in range(left, right))
    return best[0][-1]
