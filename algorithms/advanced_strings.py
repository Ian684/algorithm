"""後綴陣列、LCP 與多模式匹配；索引皆以 Python Unicode 字元計。"""
from collections import deque

def suffix_array(text):
    """倍增法 + 比較排序，O(n log²n)；回傳各後綴的排序起點。"""
    n = len(text)
    order = list(range(n))
    rank = [ord(c) for c in text]
    width = 1
    while width < n:
        key = lambda i: (rank[i], rank[i + width] if i + width < n else -1)
        order.sort(key=key)
        following = [0] * n
        for i in range(1, n):
            following[order[i]] = following[order[i - 1]] + (key(order[i]) != key(order[i - 1]))
        rank = following
        if rank[order[-1]] == n - 1:
            break
        width *= 2
    return order

def lcp_array(text, order):
    """Kasai，O(n)，輸出相鄰排序後綴的共同前綴長度，共 max(0,n-1) 個。"""
    n = len(text)
    if sorted(order) != list(range(n)):
        raise ValueError('suffix array permutation required')
    rank = [0] * n
    for position, index in enumerate(order):
        rank[index] = position
    answer = [0] * max(0, n - 1)
    length = 0
    for i in range(n):
        position = rank[i]
        if position == n - 1:
            length = 0
            continue
        j = order[position + 1]
        while i + length < n and j + length < n and (text[i + length] == text[j + length]):
            length += 1
        answer[position] = length
        length = max(0, length - 1)
    return answer

class AhoCorasick:
    """建 Trie/failure links 後一次掃描多個非空模式；搜尋 O(text+matches)。"""

    def __init__(self, patterns):
        self.patterns = list(patterns)
        self.next = [{}]
        self.fail = [0]
        self.output = [[]]
        if any((not pattern for pattern in self.patterns)):
            raise ValueError('empty pattern')
        for identity, pattern in enumerate(self.patterns):
            node = 0
            for character in pattern:
                if character not in self.next[node]:
                    self.next[node][character] = len(self.next)
                    self.next.append({})
                    self.fail.append(0)
                    self.output.append([])
                node = self.next[node][character]
            self.output[node].append(identity)
        queue = deque(self.next[0].values())
        while queue:
            node = queue.popleft()
            for character, child in self.next[node].items():
                fallback = self.fail[node]
                while fallback and character not in self.next[fallback]:
                    fallback = self.fail[fallback]
                self.fail[child] = self.next[fallback].get(character, 0)
                self.output[child].extend(self.output[self.fail[child]])
                queue.append(child)

    def search(self, text):
        """回傳 (起點,模式索引)，包含重疊與重複模式。"""
        node = 0
        matches = []
        for end, character in enumerate(text):
            while node and character not in self.next[node]:
                node = self.fail[node]
            node = self.next[node].get(character, 0)
            matches.extend(((end - len(self.patterns[i]) + 1, i) for i in self.output[node]))
        return matches
