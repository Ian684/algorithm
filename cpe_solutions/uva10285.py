import sys
from algorithms.advanced_dp import longest_descending_path

def solve(text):
    tokens = iter(text.split())
    cases = int(next(tokens))
    answers = []
    for _ in range(cases):
        name = next(tokens)
        h = int(next(tokens))
        w = int(next(tokens))
        rows = [[int(next(tokens)) for _ in range(w)] for __ in range(h)]
        answers.append(f'{name}: {longest_descending_path(rows)}')
    return '\n'.join(answers)
if __name__ == '__main__':
    print(solve(sys.stdin.read()))
