def solve(values):
    for i in range(len(values)):
        index = i
        for j in range(i + 1, len(values)):
            if values[j] < values[index]: index = j
        values[i], values[index] = values[index], values[i]
    return values
