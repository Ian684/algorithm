"""網路流、匹配與圖結構。頂點 0..n-1；low-link/HK 使用遞迴 DFS。"""
from collections import deque

def max_flow(n, edges, source, sink):
    """Edmonds–Karp，edges=(u,v,非負容量)，O(VE²)，支援平行邊。"""
    if not 0 <= source < n or not 0 <= sink < n or source == sink:
        raise ValueError('distinct valid source and sink required')
    graph = [[] for _ in range(n)]
    for u, v, capacity in edges:
        if not 0 <= u < n or not 0 <= v < n or capacity < 0:
            raise ValueError('invalid edge')
        forward = [v, capacity, len(graph[v]) + (u == v)]
        reverse = [u, 0, len(graph[u])]
        graph[u].append(forward)
        graph[v].append(reverse)
    answer = 0
    while True:
        parent = [None] * n
        parent[source] = (-1, -1)
        queue = deque([source])
        while queue and parent[sink] is None:
            u = queue.popleft()
            for i, (v, capacity, _) in enumerate(graph[u]):
                if capacity > 0 and parent[v] is None:
                    parent[v] = (u, i)
                    queue.append(v)
        if parent[sink] is None:
            return answer
        amount = float('inf')
        v = sink
        while v != source:
            u, i = parent[v]
            amount = min(amount, graph[u][i][1])
            v = u
        v = sink
        while v != source:
            u, i = parent[v]
            edge = graph[u][i]
            edge[1] -= amount
            graph[v][edge[2]][1] += amount
            v = u
        answer += amount

def min_cost_flow(n, edges, source, sink, limit):
    """逐次最短增廣路，edges=(u,v,cap,cost)，O(FVE)。回傳 (flow,cost)。

    Bellman–Ford 支援負費用邊；可達負環會拒絕。F 是增廣次數上界。
    """
    if not 0 <= source < n or not 0 <= sink < n or source == sink or (limit < 0):
        raise ValueError('invalid source, sink or flow limit')
    graph = [[] for _ in range(n)]
    for u, v, capacity, cost in edges:
        if not 0 <= u < n or not 0 <= v < n or capacity < 0:
            raise ValueError('invalid edge')
        forward = [v, capacity, cost, len(graph[v]) + (u == v)]
        reverse = [u, 0, -cost, len(graph[u])]
        graph[u].append(forward)
        graph[v].append(reverse)
    flow = total = 0
    while flow < limit:
        distance = [float('inf')] * n
        distance[source] = 0
        parent = [None] * n
        for _ in range(n - 1):
            changed = False
            for u in range(n):
                for i, (v, capacity, cost, _) in enumerate(graph[u]):
                    if capacity > 0 and distance[u] + cost < distance[v]:
                        distance[v] = distance[u] + cost
                        parent[v] = (u, i)
                        changed = True
            if not changed:
                break
        if any((cap > 0 and distance[u] + cost < distance[v] for u in range(n) for v, cap, cost, _ in graph[u])):
            raise ValueError('reachable negative cost cycle')
        if parent[sink] is None:
            break
        amount = limit - flow
        v = sink
        while v != source:
            u, i = parent[v]
            amount = min(amount, graph[u][i][1])
            v = u
        v = sink
        while v != source:
            u, i = parent[v]
            edge = graph[u][i]
            edge[1] -= amount
            graph[v][edge[3]][1] += amount
            v = u
        flow += amount
        total += amount * distance[sink]
    return (flow, total)

def hopcroft_karp(graph, right_count):
    """左側鄰接表、右側頂點數；回傳左側配對 (-1 未匹配)，O(E√V)。"""
    if right_count < 0 or any((not 0 <= v < right_count for row in graph for v in row)):
        raise ValueError('invalid right vertex')
    left = [-1] * len(graph)
    right = [-1] * right_count
    infinity = len(graph) + 1
    while True:
        distance = [0 if match == -1 else infinity for match in left]
        queue = deque((u for u, match in enumerate(left) if match == -1))
        shortest = infinity
        while queue:
            u = queue.popleft()
            if distance[u] >= shortest:
                continue
            for v in graph[u]:
                if right[v] == -1:
                    shortest = distance[u] + 1
                elif distance[right[v]] == infinity:
                    distance[right[v]] = distance[u] + 1
                    queue.append(right[v])
        if shortest == infinity:
            return left

        def augment(u):
            for v in graph[u]:
                matched = right[v]
                if matched == -1 and distance[u] + 1 == shortest or (matched != -1 and distance[matched] == distance[u] + 1 and augment(matched)):
                    left[u] = v
                    right[v] = u
                    return True
            distance[u] = infinity
            return False
        for u, match in enumerate(left):
            if match == -1:
                augment(u)

def hungarian(costs):
    """最小成本指派，n×m、n<=m 的矩陣，O(n²m)，回傳 (cost,columns)。"""
    n = len(costs)
    if not n:
        return (0, [])
    m = len(costs[0])
    if m < n or any((len(row) != m for row in costs)):
        raise ValueError('rectangular n<=m matrix required')
    u = [0] * (n + 1)
    v = [0] * (m + 1)
    matched = [0] * (m + 1)
    for row in range(1, n + 1):
        matched[0] = row
        column = 0
        best = [float('inf')] * (m + 1)
        used = [False] * (m + 1)
        previous = [0] * (m + 1)
        while True:
            used[column] = True
            current = matched[column]
            delta = float('inf')
            next_column = 0
            for j in range(1, m + 1):
                if used[j]:
                    continue
                reduced = costs[current - 1][j - 1] - u[current] - v[j]
                if reduced < best[j]:
                    best[j] = reduced
                    previous[j] = column
                if best[j] < delta:
                    delta = best[j]
                    next_column = j
            for j in range(m + 1):
                if used[j]:
                    u[matched[j]] += delta
                    v[j] -= delta
                else:
                    best[j] -= delta
            column = next_column
            if matched[column] == 0:
                break
        while column:
            prior = previous[column]
            matched[column] = matched[prior]
            column = prior
    assignment = [-1] * n
    for j in range(1, m + 1):
        if matched[j]:
            assignment[matched[j] - 1] = j - 1
    return (sum((costs[i][j] for i, j in enumerate(assignment))), assignment)

def _lowlink(n, edges):
    graph = [[] for _ in range(n)]
    for identity, (u, v) in enumerate(edges):
        if not 0 <= u < n or not 0 <= v < n:
            raise ValueError('invalid vertex')
        graph[u].append((v, identity))
        graph[v].append((u, identity))
    discovery = [-1] * n
    low = [0] * n
    cuts = set()
    critical = []
    clock = 0

    def visit(u, parent_edge):
        nonlocal clock
        discovery[u] = low[u] = clock
        clock += 1
        children = 0
        for v, edge_id in graph[u]:
            if edge_id == parent_edge:
                continue
            if discovery[v] == -1:
                children += 1
                visit(v, edge_id)
                low[u] = min(low[u], low[v])
                if low[v] > discovery[u]:
                    critical.append(tuple(sorted((u, v))))
                if parent_edge != -1 and low[v] >= discovery[u]:
                    cuts.add(u)
            else:
                low[u] = min(low[u], discovery[v])
        if parent_edge == -1 and children > 1:
            cuts.add(u)
    for u in range(n):
        if discovery[u] == -1:
            visit(u, -1)
    return (sorted(critical), sorted(cuts))

def bridges(n, edges):
    """無向多重圖的橋，O(V+E)；用 edge id 正確處理平行邊。"""
    return _lowlink(n, edges)[0]

def articulation_points(n, edges):
    """無向圖割點，O(V+E)，根節點需要超過一個 DFS 子樹。"""
    return _lowlink(n, edges)[1]

def euler_trail(n, edges):
    """Hierholzer 無向 Euler 路徑，含平行邊／自環，O(V+E)。無解拋錯。"""
    if n < 0:
        raise ValueError('negative vertex count')
    if not edges:
        return [0] if n else []
    graph = [[] for _ in range(n)]
    for identity, (u, v) in enumerate(edges):
        if not 0 <= u < n or not 0 <= v < n:
            raise ValueError('invalid vertex')
        graph[u].append((v, identity))
        graph[v].append((u, identity))
    odd = [u for u in range(n) if len(graph[u]) % 2]
    if len(odd) not in (0, 2):
        raise ValueError('odd degree condition fails')
    start = odd[0] if odd else next((u for u in range(n) if graph[u]))
    used = [False] * len(edges)
    stack = [start]
    path = []
    while stack:
        u = stack[-1]
        while graph[u] and used[graph[u][-1][1]]:
            graph[u].pop()
        if not graph[u]:
            path.append(stack.pop())
        else:
            v, identity = graph[u].pop()
            used[identity] = True
            stack.append(v)
    if not all(used):
        raise ValueError('non-isolated vertices are disconnected')
    return path[::-1]
