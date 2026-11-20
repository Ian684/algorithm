import sys
from algorithms.advanced_dp import ferry_loading

def solve(text):
    tokens = iter(map(int, text.split()))
    cases = next(tokens)
    answers = []
    for _ in range(cases):
        capacity = next(tokens) * 100
        cars = []
        for car in tokens:
            if car == 0:
                break
            cars.append(car)
        count, placement = ferry_loading(capacity, cars)
        answers.append('\n'.join([str(count), *placement]))
    return '\n\n'.join(answers)
if __name__ == '__main__':
    print(solve(sys.stdin.read()))
