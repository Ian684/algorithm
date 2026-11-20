import heapq
def solve(values):
    heap = values[:]
    heapq.heapify(heap)
    return [heapq.heappop(heap) for _ in range(len(heap))]
