def solve(values):
    tree = [0]*(len(values)+1)
    for index, value in enumerate(values,1):
        while index < len(tree):
            tree[index]+=value; index += index & -index
    def prefix(index):
        total=0
        while index:
            total += tree[index]; index -= index & -index
        return total
    return prefix
