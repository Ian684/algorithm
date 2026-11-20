"""位元集合與區間 DP；含對照本帳號 CPE 三星題庫的應用。"""

def traveling_salesman(costs):
    """Held–Karp，從 0 出發再回 0 的最小成本；O(n²2^n)，建議 n<=18。"""
    n = len(costs)
    if not n:
        return 0
    if any((len(row) != n for row in costs)):
        raise ValueError('square matrix required')
    if n == 1:
        return 0
    best = {(1, 0): 0}
    for mask in range(1, 1 << n):
        if not mask & 1:
            continue
        for last in range(n):
            current = best.get((mask, last), float('inf'))
            if current == float('inf'):
                continue
            for nxt in range(1, n):
                if not mask >> nxt & 1:
                    key = (mask | 1 << nxt, nxt)
                    best[key] = min(best.get(key, float('inf')), current + costs[last][nxt])
    return min((best.get(((1 << n) - 1, last), float('inf')) + costs[last][0] for last in range(1, n)))

def hamiltonian_paths(graph, source, sink):
    """有向圖從 source 到 sink、恰訪每點一次的路徑數；O((V+E)2^V)。"""
    n = len(graph)
    if not 0 <= source < n or not 0 <= sink < n:
        raise ValueError('invalid endpoint')
    if any((not 0 <= v < n for row in graph for v in row)):
        raise ValueError('invalid vertex')
    ways = {(1 << source, source): 1}
    for mask in range(1, 1 << n):
        if not mask >> source & 1:
            continue
        for u in range(n):
            count = ways.get((mask, u), 0)
            if not count:
                continue
            for v in graph[u]:
                if not mask >> v & 1:
                    key = (mask | 1 << v, v)
                    ways[key] = ways.get(key, 0) + count
    return ways.get(((1 << n) - 1, sink), 0)

def optimal_bst(frequencies):
    """UVa 10304 型：鍵已排序，根深度為 0 的最小加權搜尋成本；O(n³)。"""
    if any((f < 0 for f in frequencies)):
        raise ValueError('negative frequency')
    n = len(frequencies)
    prefix = [0]
    for f in frequencies:
        prefix.append(prefix[-1] + f)
    best = [[0] * (n + 1) for _ in range(n + 1)]
    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length
            best[left][right] = min((best[left][root] + best[root + 1][right] + prefix[right] - prefix[left] - frequencies[root] for root in range(left, right)))
    return best[0][n]

def cutting_sticks(length, cuts):
    """UVa 10003 型：切一次的成本是當段長度；O(k³) time/O(k²) space。"""
    if length <= 0 or len(set(cuts)) != len(cuts) or any((not 0 < x < length for x in cuts)):
        raise ValueError('distinct interior cuts required')
    points = [0, *sorted(cuts), length]
    n = len(points)
    best = [[0] * n for _ in range(n)]
    for width in range(2, n):
        for left in range(n - width):
            right = left + width
            best[left][right] = min((best[left][k] + best[k][right] for k in range(left + 1, right))) + points[right] - points[left]
    return best[0][-1]

def distinct_subsequences(text, target):
    """UVa 10069 型：刪除字元後等於 target 的方式數；O(nm)，任意精度整數。"""
    ways = [1] + [0] * len(target)
    for character in text:
        for j in range(len(target), 0, -1):
            if character == target[j - 1]:
                ways[j] += ways[j - 1]
    return ways[-1]

def ferry_loading(capacity, cars):
    """UVa 10261 型，左右各 capacity，同單位；回傳最多前綴車數與停放方向。

    O(nC) time/space；不能跳過或重排車輛。輸入正整數。
    """
    if capacity < 0 or any((car <= 0 for car in cars)):
        raise ValueError('invalid capacity or car')
    states = {0}
    history = []
    loaded_length = 0
    for car in cars:
        parents = {}
        for port in sorted(states):
            if port + car <= capacity:
                parents.setdefault(port + car, (port, 'port'))
            if loaded_length - port + car <= capacity:
                parents.setdefault(port, (port, 'starboard'))
        if not parents:
            break
        history.append(parents)
        states = set(parents)
        loaded_length += car
    state = min(states)
    placement = []
    for parents in reversed(history):
        state, side = parents[state]
        placement.append(side)
    return (len(history), placement[::-1])

def chopsticks(lengths, pairs):
    """UVa 10271 型核心：每位客人兩短一長，差平方總和最小；O(k n)。

    pairs 是實際客人數；若依原題含額外 8 位，要由呼叫者傳 guests+8。
    """
    if pairs < 0 or any((x < 0 for x in lengths)):
        raise ValueError('negative input')
    if len(lengths) < 3 * pairs:
        return None
    ordered = sorted(lengths, reverse=True)
    n = len(ordered)
    previous = [0] * (n + 1)
    for people in range(1, pairs + 1):
        current = [float('inf')] * (n + 1)
        for used in range(3 * people, n + 1):
            cost = (ordered[used - 1] - ordered[used - 2]) ** 2
            current[used] = min(current[used - 1], previous[used - 2] + cost)
        previous = current
    return previous[-1]

def tug_of_war(weights):
    """UVa 10032 型：人數差至多一，總重差最小；count 維度的 bitset DP。"""
    if any((weight < 0 for weight in weights)):
        raise ValueError('negative weight')
    count = len(weights) // 2
    reachable = [1] + [0] * count
    for i, weight in enumerate(weights):
        for size in range(min(count, i + 1), 0, -1):
            reachable[size] |= reachable[size - 1] << weight
    total = sum(weights)
    candidates = reachable[count]
    best = min((value for value in range(total + 1) if candidates >> value & 1), key=lambda x: abs(total - 2 * x))
    return tuple(sorted((best, total - best)))

def longest_descending_path(rows):
    """UVa 10285 型：四方向嚴格下降的最長路徑；排序 DP，O(hw log(hw))。"""
    if not rows or not rows[0]:
        return 0
    h, w = (len(rows), len(rows[0]))
    if any((len(row) != w for row in rows)):
        raise ValueError('ragged grid')
    best = [[1] * w for _ in rows]
    for _, r, c in sorted(((rows[r][c], r, c) for r in range(h) for c in range(w))):
        best[r][c] = 1 + max((best[a][b] for a, b in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)) if 0 <= a < h and 0 <= b < w and (rows[a][b] < rows[r][c])), default=0)
    return max(map(max, best))
