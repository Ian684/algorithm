def solve(values):
    if len(values) < 2:
        return values
    pivot = values[len(values) // 2]
    return solve([v for v in values if v < pivot]) + [v for v in values if v == pivot] + solve([v for v in values if v > pivot])
