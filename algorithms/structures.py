"""四種資料結構；查詢範圍統一使用左閉右開 [left, right)。"""


class DisjointSet:
    """路徑壓縮與依大小合併，攤銷 O(alpha(n))。"""
    def __init__(self, n):
        if n < 0:
            raise ValueError('negative size')
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        if not 0 <= x < len(self.parent):
            raise IndexError('vertex outside the set')
        while x != self.parent[x]:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True


class FenwickTree:
    """單點增量與區間總和，O(log n)；外部 0-based，內部 1-based。"""
    def __init__(self, values):
        self.tree = [0] * (len(values) + 1)
        for i, value in enumerate(values):
            self.add(i, value)

    def add(self, index, delta):
        if not 0 <= index < len(self.tree) - 1:
            raise IndexError('index outside Fenwick tree')
        index += 1
        while index < len(self.tree):
            self.tree[index] += delta
            index += index & -index

    def prefix_sum(self, end):
        if not 0 <= end < len(self.tree):
            raise IndexError('prefix outside Fenwick tree')
        total = 0
        while end:
            total += self.tree[end]
            end -= end & -end
        return total

    def range_sum(self, left, right):
        if not 0 <= left <= right < len(self.tree):
            raise IndexError('invalid range')
        return self.prefix_sum(right) - self.prefix_sum(left)


class SegmentTree:
    """迭代式區間最小值；建樹 O(n)，單點指定與查詢 O(log n)。"""
    def __init__(self, values):
        self.n = len(values)
        self.tree = [float('inf')] * self.n + list(values)
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, index, value):
        if not 0 <= index < self.n:
            raise IndexError('index outside segment tree')
        index += self.n
        self.tree[index] = value
        while index > 1:
            index //= 2
            self.tree[index] = min(self.tree[2 * index], self.tree[2 * index + 1])

    def range_min(self, left, right):
        if not 0 <= left <= right <= self.n:
            raise IndexError('invalid range')
        left, right, result = left + self.n, right + self.n, float('inf')
        while left < right:
            if left & 1:
                result = min(result, self.tree[left]); left += 1
            if right & 1:
                right -= 1; result = min(result, self.tree[right])
            left //= 2; right //= 2
        return result


class SparseTable:
    """靜態區間最小值；O(n log n) 建表，O(1) 查詢，不支援更新。"""
    def __init__(self, values):
        self.n = len(values)
        self.rows = [list(values)]
        width = 2
        while width <= self.n:
            previous = self.rows[-1]
            half = width // 2
            self.rows.append([min(previous[i], previous[i + half]) for i in range(self.n - width + 1)])
            width *= 2

    def range_min(self, left, right):
        if not 0 <= left < right <= self.n:
            raise IndexError('non-empty range required')
        level = (right - left).bit_length() - 1
        return min(self.rows[level][left], self.rows[level][right - (1 << level)])
