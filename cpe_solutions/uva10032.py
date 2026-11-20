import sys
from algorithms.advanced_dp import tug_of_war

def solve(text):
    tokens = iter(map(int, text.split()))
    cases = next(tokens)
    answers = []
    for _ in range(cases):
        n = next(tokens)
        a, b = tug_of_war([next(tokens) for _ in range(n)])
        answers.append(f'{a} {b}')
    return '\n\n'.join(answers)
if __name__ == '__main__':
    print(solve(sys.stdin.read()))
