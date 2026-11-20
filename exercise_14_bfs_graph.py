from collections import deque
def solve(graph, start):
    seen = {start}; queue = deque([start]); order = []
    while queue:
        node = queue.popleft(); order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in seen: seen.add(neighbor); queue.append(neighbor)
    return order
