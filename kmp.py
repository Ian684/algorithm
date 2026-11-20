def generate_lps(p):
    
    lps = [0]*len(p)
    length = 0
    i = 1

    while i < len(p):
        if p[i] == p[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length-1]
        else:
            lps[i] = 0
            i += 1

    return lps

def kmp(text , pattern):

    if not pattern:return []
    lps = generate_lps(pattern)
    i = 0
    j = 0
    ans = []

    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == len(pattern):
            j = lps[j - 1]
        elif i < len(text) and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return ans
