import sys
from algorithms.advanced_dp import cutting_sticks

def solve(text):
    tokens = iter(map(int, text.split()))
    answers = []
    for length in tokens:
        if length == 0:
            break
        count = next(tokens)
        cuts = [next(tokens) for _ in range(count)]
        answers.append(f'The minimum cutting is {cutting_sticks(length, cuts)}.')
    return '\n'.join(answers)
if __name__ == '__main__':
    print(solve(sys.stdin.read()))
