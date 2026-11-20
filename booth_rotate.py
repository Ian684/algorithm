def booth(s):
    ss = s + s 
    n = len(s)
    i = best = 0
    while i < n:
        best = i
        j = i + 1
        k = i
        while j < 2 * n and ss[k] == ss[j]:
            k += 1
            j += 1
        if j == 2 * n and ss[k] < ss[j]:
            i = k + 1
        else:
            i = j
    return ss[best:best + n]
if __name__ == "__main__":
    s = "0110"
    print(booth(s))