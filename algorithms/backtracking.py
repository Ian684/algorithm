"""小規模窮舉；產生器避免一次把所有答案放入記憶體。"""


def unique_permutations(values):
    """去除重複排列；最壞 O(n! n)，輸入元素需可排序。"""
    ordered, used, path = sorted(values), [False] * len(values), []
    def visit():
        if len(path) == len(ordered):
            yield tuple(path)
            return
        for i, value in enumerate(ordered):
            if used[i] or (i and ordered[i] == ordered[i - 1] and not used[i - 1]):
                continue
            used[i] = True; path.append(value)
            yield from visit()
            path.pop(); used[i] = False
    yield from visit()


def n_queens(n):
    """每個答案是各列皇后的欄位置；最壞 O(n!)，n=0 有一個空解。"""
    if n < 0:
        raise ValueError('negative board size')
    columns, diagonal_a, diagonal_b, path = set(), set(), set(), []
    def place(row):
        if row == n:
            yield tuple(path)
            return
        for column in range(n):
            if column in columns or row - column in diagonal_a or row + column in diagonal_b:
                continue
            columns.add(column); diagonal_a.add(row - column); diagonal_b.add(row + column)
            path.append(column)
            yield from place(row + 1)
            path.pop()
            columns.remove(column); diagonal_a.remove(row - column); diagonal_b.remove(row + column)
    yield from place(0)


def subsets(values):
    """位元遮罩列出子集合，O(2^n n)；相同值仍視為不同位置。"""
    for mask in range(1 << len(values)):
        yield tuple(value for i, value in enumerate(values) if mask & (1 << i))
