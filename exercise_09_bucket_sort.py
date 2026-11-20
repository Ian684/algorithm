def solve(values):
    if not values: return []
    buckets = [[] for _ in range(len(values))]
    maximum = max(values)
    for value in values:
        buckets[min(len(values)-1, int(value*len(values)/(maximum+1)))].append(value)
    return [value for bucket in buckets for value in sorted(bucket)]
