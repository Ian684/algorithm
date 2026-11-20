from algorithms.sorting import merge_sort
from algorithms.strings import kmp, manacher_length
from algorithms.graphs import dijkstra, kruskal
from algorithms.dynamic_programming import coin_change, lis_length
from algorithms.number_theory import chinese_remainder
from algorithms.structures import FenwickTree
from algorithms.backtracking import n_queens

if __name__ == '__main__':
    print('merge sort:', merge_sort([7, -2, 3, 3, 1]))
    print('overlapping matches:', kmp('ababa', 'aba'))
    print('palindrome length:', manacher_length('abacaba'))
    print('distances:', dijkstra([[(1, 4), (2, 1)], [], [(1, 2)]], 0))
    print('MST:', kruskal(3, [(0, 1, 4), (0, 2, 1), (1, 2, 2)]))
    print('coin change:', coin_change([1, 3, 4], 6))
    print('LIS:', lis_length([3, 1, 2, 2, 5]))
    print('CRT:', chinese_remainder([(2, 3), (3, 5), (2, 7)]))
    print('range sum [1,4):', FenwickTree([2, -3, 5, 7]).range_sum(1, 4))
    print('four queens:', list(n_queens(4)))
