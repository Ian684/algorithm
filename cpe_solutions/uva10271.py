import sys
from algorithms.advanced_dp import chopsticks

def solve(text):
    tokens = iter(map(int, text.split()))
    cases = next(tokens)
    answers = []
    for _ in range(cases):
        guests = next(tokens)
        n = next(tokens)
        result = chopsticks([next(tokens) for _ in range(n)], guests + 8)
        if result is None:
            raise ValueError('not enough chopsticks')
        answers.append(str(result))
    return '\n'.join(answers)
if __name__ == '__main__':
    print(solve(sys.stdin.read()))
