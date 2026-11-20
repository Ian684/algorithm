def solve(values):
    if not values: return []
    maximum = max(values)
    exponent = 1
    while maximum // exponent:
        buckets = [[] for _ in range(10)]
        for value in values: buckets[(value // exponent) % 10].append(value)
        values = [value for bucket in buckets for value in bucket]
        exponent *= 10
    return values
