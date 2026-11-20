"""字串搜尋、回文與前綴樹。索引是 Python 字元位置，不是 UTF-8 位元組位置。"""
from kmp import generate_lps, kmp


def z_function(text):
    """z[i] 是 text 與 text[i:] 的最長共同前綴長度；O(n)。z[0]=0。"""
    z, left, right = [0] * len(text), 0, 0
    for i in range(1, len(text)):
        if i < right:
            z[i] = min(right - i, z[i - left])
        while i + z[i] < len(text) and text[z[i]] == text[i + z[i]]:
            z[i] += 1
        if i + z[i] > right:
            left, right = i, i + z[i]
    return z


def rabin_karp(text, pattern):
    """滾動雜湊，命中後比對原文排除碰撞；平均 O(n+m)，最差 O(nm)。"""
    n, m, base, modulus = len(text), len(pattern), 257, 1_000_000_007
    if not m or m > n:
        return []
    target = window = 0
    for i in range(m):
        target = (target * base + ord(pattern[i])) % modulus
        window = (window * base + ord(text[i])) % modulus
    power, result = pow(base, m - 1, modulus), []
    for i in range(n - m + 1):
        if window == target and text[i:i + m] == pattern:
            result.append(i)
        if i + m < n:
            window = ((window - ord(text[i]) * power) * base + ord(text[i + m])) % modulus
    return result


def manacher_length(text):
    """最長連續回文長度；O(n)。用 None 當分隔符，避免與輸入字元衝突。"""
    transformed = [None]
    for character in text:
        transformed.extend((character, None))
    radius = [0] * len(transformed)
    center = right = 0
    for i in range(len(transformed)):
        if i < right:
            radius[i] = min(right - i, radius[2 * center - i])
        while i - radius[i] - 1 >= 0 and i + radius[i] + 1 < len(transformed):
            if transformed[i - radius[i] - 1] != transformed[i + radius[i] + 1]:
                break
            radius[i] += 1
        if i + radius[i] > right:
            center, right = i, i + radius[i]
    return max(radius, default=0)


class Trie:
    """字典作為子節點，None 標記單字結尾；插入/查詢 O(字串長度)。"""
    def __init__(self):
        self.root = {}

    def add(self, word):
        node = self.root
        for character in word:
            node = node.setdefault(character, {})
        node[None] = True

    def contains(self, word):
        node = self.root
        for character in word:
            if character not in node:
                return False
            node = node[character]
        return None in node

    def starts_with(self, prefix):
        node = self.root
        for character in prefix:
            if character not in node:
                return False
            node = node[character]
        return True
