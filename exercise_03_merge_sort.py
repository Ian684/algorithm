def solve(values):
    if len(values) < 2:
        return values
    middle = len(values) // 2
    left = solve(values[:middle])
    right = solve(values[middle:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]
