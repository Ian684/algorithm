"""頂點固定編號 0..n-1。鄰接表 graph[u]；加權圖元素為 (v, weight)。"""
from collections import deque
import heapq
from .structures import DisjointSet


def bfs(graph, start):
    """無權圖最短距離，無法到達為 -1；O(V+E)。"""
    distance = [-1] * len(graph)
    distance[start] = 0
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if distance[v] == -1:
                distance[v] = distance[u] + 1
                queue.append(v)
    return distance


def dfs(graph, start):
    """迭代 DFS 的造訪順序，依鄰接表順序展開；O(V+E)。"""
    stack, seen, order = [start], set(), []
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u); order.append(u)
        stack.extend(reversed(graph[u]))
    return order


def topological_sort(graph):
    """Kahn 拓樸排序，遇環拋出 ValueError；O(V+E)。"""
    degree = [0] * len(graph)
    for neighbors in graph:
        for v in neighbors:
            degree[v] += 1
    queue = deque(u for u, value in enumerate(degree) if value == 0)
    order = []
    while queue:
        u = queue.popleft(); order.append(u)
        for v in graph[u]:
            degree[v] -= 1
            if degree[v] == 0:
                queue.append(v)
    if len(order) != len(graph):
        raise ValueError('graph contains a directed cycle')
    return order


def dijkstra(graph, start):
    """非負權重最短路徑；O((V+E) log V)，不可達為 inf。"""
    if any(weight < 0 for neighbors in graph for _, weight in neighbors):
        raise ValueError('negative edge in Dijkstra input')
    distance = [float('inf')] * len(graph)
    distance[start] = 0
    queue = [(0, start)]
    while queue:
        cost, u = heapq.heappop(queue)
        if cost != distance[u]:
            continue
        for v, weight in graph[u]:
            if cost + weight < distance[v]:
                distance[v] = cost + weight
                heapq.heappush(queue, (distance[v], v))
    return distance


def bellman_ford(n, edges, start):
    """edges=(u,v,w)，可含負邊；可達負環拋出 ValueError；O(VE)。"""
    distance = [float('inf')] * n
    distance[start] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, weight in edges:
            if distance[u] + weight < distance[v]:
                distance[v] = distance[u] + weight
                changed = True
        if not changed:
            break
    if any(distance[u] + weight < distance[v] for u, v, weight in edges):
        raise ValueError('reachable negative cycle')
    return distance


def floyd_warshall(n, edges):
    """所有點對最短路徑；O(V³) time/O(V²) space，遇任意負環拋錯。"""
    distance = [[float('inf')] * n for _ in range(n)]
    for u in range(n):
        distance[u][u] = 0
    for u, v, weight in edges:
        distance[u][v] = min(distance[u][v], weight)
    for k in range(n):
        for u in range(n):
            for v in range(n):
                distance[u][v] = min(distance[u][v], distance[u][k] + distance[k][v])
    if any(distance[u][u] < 0 for u in range(n)):
        raise ValueError('negative cycle')
    return distance


def kruskal(n, edges):
    """無向圖最小生成樹 (總重, 邊列表)，不連通時拋錯；O(E log E)。"""
    sets, chosen, total = DisjointSet(n), [], 0
    for u, v, weight in sorted(edges, key=lambda edge: edge[2]):
        if sets.union(u, v):
            chosen.append((u, v, weight)); total += weight
    if n and len(chosen) != n - 1:
        raise ValueError('graph is disconnected')
    return total, chosen


def prim(graph):
    """無向加權鄰接表最小生成樹總重，不連通時拋錯；O(E log V)。"""
    if not graph:
        return 0
    queue, seen, total = [(0, 0)], set(), 0
    while queue:
        weight, u = heapq.heappop(queue)
        if u in seen:
            continue
        seen.add(u); total += weight
        for v, cost in graph[u]:
            if v not in seen:
                heapq.heappush(queue, (cost, v))
    if len(seen) != len(graph):
        raise ValueError('graph is disconnected')
    return total


def strongly_connected_components(graph):
    """Kosaraju 強連通分量；迭代實作避免遞迴深度限制，O(V+E)。"""
    seen, order = set(), []
    for root in range(len(graph)):
        if root in seen:
            continue
        seen.add(root)
        stack = [(root, iter(graph[root]))]
        while stack:
            u, neighbors = stack[-1]
            v = next(neighbors, None)
            if v is None:
                order.append(u); stack.pop()
            elif v not in seen:
                seen.add(v); stack.append((v, iter(graph[v])))
    reverse = [[] for _ in graph]
    for u, neighbors in enumerate(graph):
        for v in neighbors:
            reverse[v].append(u)
    seen, components = set(), []
    for root in reversed(order):
        if root in seen:
            continue
        component, stack = [], [root]
        seen.add(root)
        while stack:
            u = stack.pop(); component.append(u)
            for v in reverse[u]:
                if v not in seen:
                    seen.add(v); stack.append(v)
        components.append(sorted(component))
    return components


def bipartite_coloring(graph):
    """無向圖二分染色，成功回傳 0/1 顏色，失敗回傳 None；O(V+E)。"""
    colors = [-1] * len(graph)
    for root in range(len(graph)):
        if colors[root] != -1:
            continue
        colors[root], queue = 0, deque([root])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if colors[v] == -1:
                    colors[v] = colors[u] ^ 1; queue.append(v)
                elif colors[v] == colors[u]:
                    return None
    return colors
