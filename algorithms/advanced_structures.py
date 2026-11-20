"""樹查詢、延遲標記、持久化與離線查詢；範圍皆 [left,right)。"""
from collections import Counter, deque
from math import isqrt

class LowestCommonAncestor:
    """Binary lifting，O(n log n) 建表，O(log n) 查詢。"""

    def __init__(self, n, edges, root=0):
        if not 0 <= root < n or len(edges) != n - 1:
            raise ValueError('tree required')
        graph = [[] for _ in range(n)]
        for a, b in edges:
            if not 0 <= a < n or not 0 <= b < n:
                raise ValueError('invalid vertex')
            graph[a].append(b)
            graph[b].append(a)
        parent = [-1] * n
        parent[root] = root
        self.depth = [0] * n
        queue = deque([root])
        visited = 0
        while queue:
            u = queue.popleft()
            visited += 1
            for v in graph[u]:
                if v == parent[u]:
                    continue
                if parent[v] != -1:
                    raise ValueError('cycle')
                parent[v] = u
                self.depth[v] = self.depth[u] + 1
                queue.append(v)
        if visited != n:
            raise ValueError('disconnected tree')
        self.up = [parent]
        for _ in range(1, n.bit_length()):
            prior = self.up[-1]
            self.up.append([prior[prior[u]] for u in range(n)])

    def query(self, a, b):
        if not 0 <= a < len(self.depth) or not 0 <= b < len(self.depth):
            raise IndexError('invalid vertex')
        if self.depth[a] < self.depth[b]:
            a, b = (b, a)
        difference = self.depth[a] - self.depth[b]
        for k in range(len(self.up)):
            if difference >> k & 1:
                a = self.up[k][a]
        if a == b:
            return a
        for row in reversed(self.up):
            if row[a] != row[b]:
                a, b = (row[a], row[b])
        return self.up[0][a]

class LazyRangeSum:
    """區間加值／區間總和，建樹 O(n)，操作 O(log n)。"""

    def __init__(self, values):
        self.n = len(values)
        self.tree = [0] * max(1, 4 * self.n)
        self.lazy = self.tree[:]

        def build(node, left, right):
            if right - left == 1:
                self.tree[node] = values[left]
                return
            middle = (left + right) // 2
            build(2 * node, left, middle)
            build(2 * node + 1, middle, right)
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
        if self.n:
            build(1, 0, self.n)

    def _operate(self, ql, qr, delta, update):
        if not 0 <= ql <= qr <= self.n:
            raise IndexError('invalid range')

        def visit(node, left, right):
            if qr <= left or right <= ql:
                return 0
            if ql <= left and right <= qr:
                if update:
                    self.tree[node] += delta * (right - left)
                    self.lazy[node] += delta
                return self.tree[node]
            middle = (left + right) // 2
            if self.lazy[node]:
                for child, length in ((2 * node, middle - left), (2 * node + 1, right - middle)):
                    self.tree[child] += self.lazy[node] * length
                    self.lazy[child] += self.lazy[node]
                self.lazy[node] = 0
            answer = visit(2 * node, left, middle) + visit(2 * node + 1, middle, right)
            if update:
                self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
            return answer
        return visit(1, 0, self.n) if ql < qr else 0

    def add(self, left, right, delta):
        self._operate(left, right, delta, True)

    def range_sum(self, left, right):
        return self._operate(left, right, 0, False)

class PersistentKth:
    """前綴版本的頻率線段樹；建表 O(n log n)，區間第 k 小 O(log n)。"""

    def __init__(self, values):
        self.coordinates = sorted(set(values))
        rank = {x: i for i, x in enumerate(self.coordinates)}
        self.nodes = [(0, 0, 0)]
        self.roots = [0]

        def insert(old, left, right, position):
            a, b, count = self.nodes[old]
            identity = len(self.nodes)
            self.nodes.append((a, b, count + 1))
            if right - left > 1:
                middle = (left + right) // 2
                if position < middle:
                    a = insert(a, left, middle, position)
                else:
                    b = insert(b, middle, right, position)
                self.nodes[identity] = (a, b, count + 1)
            return identity
        for value in values:
            self.roots.append(insert(self.roots[-1], 0, len(rank), rank[value]))

    def kth(self, left, right, k):
        """k 從 0 開始，查 values[left:right] 中第 k 小。"""
        if not 0 <= left < right < len(self.roots) or not 0 <= k < right - left:
            raise IndexError('invalid interval or k')
        a, b = (self.roots[left], self.roots[right])
        low, high = (0, len(self.coordinates))
        while high - low > 1:
            middle = (low + high) // 2
            count = self.nodes[self.nodes[b][0]][2] - self.nodes[self.nodes[a][0]][2]
            if k < count:
                a, b = (self.nodes[a][0], self.nodes[b][0])
                high = middle
            else:
                k -= count
                a, b = (self.nodes[a][1], self.nodes[b][1])
                low = middle
        return self.coordinates[low]

def mo_distinct(values, queries):
    """Mo 離線區間不同值數，O((n+q)√n)；答案保留原查詢順序。"""
    n = len(values)
    if any((not 0 <= a <= b <= n for a, b in queries)):
        raise IndexError('invalid interval')
    width = max(1, isqrt(n))
    counts = Counter()
    distinct = 0
    left = right = 0
    answers = [0] * len(queries)

    def change(index, delta):
        nonlocal distinct
        value = values[index]
        old = counts[value]
        counts[value] += delta
        if old == 0 and counts[value] > 0:
            distinct += 1
        if old > 0 and counts[value] == 0:
            distinct -= 1
    order = sorted(range(len(queries)), key=lambda i: (queries[i][0] // width, queries[i][1] * (-1 if queries[i][0] // width % 2 else 1)))
    for identity in order:
        a, b = queries[identity]
        while left > a:
            left -= 1
            change(left, 1)
        while right < b:
            change(right, 1)
            right += 1
        while left < a:
            change(left, -1)
            left += 1
        while right > b:
            right -= 1
            change(right, -1)
        answers[identity] = distinct
    return answers
