import sys
from algorithms.advanced_dp import optimal_bst

def solve(text):
    tokens = iter(map(int, text.split()))
    answers = []
    for count in tokens:
        answers.append(str(optimal_bst([next(tokens) for _ in range(count)])))
    return '\n'.join(answers)
if __name__ == '__main__':
    print(solve(sys.stdin.read()))
