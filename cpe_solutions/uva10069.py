import sys
from algorithms.advanced_dp import distinct_subsequences

def solve(text):
    lines = iter(text.splitlines())
    count = int(next(lines))
    answers = []
    for _ in range(count):
        source = next(lines)
        target = next(lines)
        answers.append(str(distinct_subsequences(source, target)))
    return '\n'.join(answers)
if __name__ == '__main__':
    print(solve(sys.stdin.read()))
