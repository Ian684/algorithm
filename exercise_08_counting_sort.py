def solve(values):
    if not values: return []
    low, high = min(values), max(values)
    counts = [0] * (high - low + 1)
    for value in values: counts[value-low] += 1
    return [low+i for i, count in enumerate(counts) for _ in range(count)]
