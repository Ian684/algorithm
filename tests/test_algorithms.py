import bisect
import itertools
import math
import random
import unittest
from algorithms import sorting, searching, strings, structures, graphs, dynamic_programming as dp, number_theory as nt, sequences, backtracking


class AlgorithmTests(unittest.TestCase):
    def setUp(self):
        self.random = random.Random(684)

    def test_sorts_against_python(self):
        for _ in range(80):
            values = [self.random.randrange(-20, 21) for _ in range(self.random.randrange(30))]
            original = values[:]
            for sort in (sorting.insertion_sort, sorting.merge_sort, sorting.heap_sort, sorting.counting_sort):
                self.assertEqual(sort(values), sorted(values))
            self.assertEqual(sorting.quick_sort(values), sorted(values))
            self.assertEqual(sorting.radix_sort([abs(x) for x in values]), sorted(abs(x) for x in values))
            self.assertEqual(values, original)
        with self.assertRaises(ValueError):
            sorting.radix_sort([-1])

    def test_searches_and_selection(self):
        for _ in range(80):
            values = sorted(self.random.choices(range(-5, 6), k=20))
            for target in range(-6, 7):
                self.assertEqual(searching.lower_bound(values, target), bisect.bisect_left(values, target))
                self.assertEqual(searching.upper_bound(values, target), bisect.bisect_right(values, target))
                self.assertEqual(searching.binary_search(values, target), values.index(target) if target in values else -1)
            for k in range(len(values)):
                self.assertEqual(searching.quickselect(values[::-1], k), values[k])
        self.assertEqual(searching.binary_search([], 1), -1)
        with self.assertRaises(IndexError):
            searching.quickselect([], 0)
        for split in range(10):
            values = list(range(10))[split:] + list(range(10))[:split]
            for target in range(-1, 11):
                self.assertEqual(searching.rotated_search(values, target), values.index(target) if target in values else -1)

    def test_string_searches_against_naive(self):
        for _ in range(200):
            text = ''.join(self.random.choices('ab甲乙#', k=30))
            pattern = ''.join(self.random.choices('ab甲乙#', k=self.random.randrange(1, 5)))
            expected = [i for i in range(len(text) - len(pattern) + 1) if text.startswith(pattern, i)]
            self.assertEqual(strings.kmp(text, pattern), expected)
            self.assertEqual(strings.rabin_karp(text, pattern), expected)
        self.assertEqual(strings.kmp('ababa', 'aba'), [0, 2])
        self.assertEqual(strings.kmp('', 'a'), [])
        self.assertEqual(strings.kmp('abc', ''), [])
        self.assertEqual(strings.rabin_karp('abc', ''), [])
        self.assertEqual(strings.generate_lps('ababaca'), [0, 0, 1, 2, 3, 0, 1])

    def test_z_and_manacher_against_naive(self):
        for length in range(20):
            text = ''.join(self.random.choices('aba#甲', k=length))
            expected_z = [0] * length
            for i in range(1, length):
                while i + expected_z[i] < length and text[expected_z[i]] == text[i + expected_z[i]]:
                    expected_z[i] += 1
            self.assertEqual(strings.z_function(text), expected_z)
            longest = max((j - i for i in range(length + 1) for j in range(i, length + 1) if text[i:j] == text[i:j][::-1]), default=0)
            self.assertEqual(strings.manacher_length(text), longest)

    def test_trie(self):
        trie = strings.Trie()
        # Insertion is tested through the public API, including an empty word.
        for word in ('car', 'cart', '貓', ''):
            trie.add(word)
        self.assertTrue(trie.contains('car'))
        self.assertFalse(trie.contains('ca'))
        self.assertTrue(trie.contains(''))
        self.assertTrue(trie.starts_with('ca'))
        self.assertFalse(trie.starts_with('dog'))

    def test_range_structures_against_lists(self):
        values = [self.random.randrange(-50, 51) for _ in range(31)]
        fenwick, segment = structures.FenwickTree(values), structures.SegmentTree(values)
        for _ in range(150):
            index, value = self.random.randrange(len(values)), self.random.randrange(-50, 51)
            fenwick.add(index, value - values[index]); segment.update(index, value); values[index] = value
            left, right = sorted(self.random.sample(range(len(values) + 1), 2))
            self.assertEqual(fenwick.range_sum(left, right), sum(values[left:right]))
            self.assertEqual(segment.range_min(left, right), min(values[left:right]))
        sparse = structures.SparseTable(values)
        for left in range(len(values)):
            for right in range(left + 1, len(values) + 1):
                self.assertEqual(sparse.range_min(left, right), min(values[left:right]))
        self.assertEqual(structures.FenwickTree([]).range_sum(0, 0), 0)
        self.assertEqual(structures.SegmentTree([]).range_min(0, 0), math.inf)
        with self.assertRaises(IndexError):
            fenwick.add(-1, 1)
        with self.assertRaises(IndexError):
            sparse.range_min(1, 1)

    def test_disjoint_set(self):
        sets = structures.DisjointSet(5)
        self.assertTrue(sets.union(0, 1)); self.assertTrue(sets.union(1, 2))
        self.assertFalse(sets.union(2, 0))
        self.assertEqual(sets.find(0), sets.find(2))
        self.assertNotEqual(sets.find(0), sets.find(3))

    def test_graph_traversal_order_and_cycles(self):
        graph = [[1, 2], [3], [3], []]
        self.assertEqual(graphs.bfs(graph, 0), [0, 1, 1, 2])
        self.assertEqual(graphs.dfs(graph, 0), [0, 1, 3, 2])
        order = graphs.topological_sort(graph)
        for u, neighbors in enumerate(graph):
            for v in neighbors:
                self.assertLess(order.index(u), order.index(v))
        with self.assertRaises(ValueError):
            graphs.topological_sort([[1], [0]])
        self.assertIsNone(graphs.bipartite_coloring([[1, 2], [0, 2], [0, 1]]))
        self.assertEqual(graphs.bipartite_coloring([[1], [0], []]), [0, 1, 0])
        components = graphs.strongly_connected_components([[1], [0, 2], [3], [2], []])
        self.assertEqual({tuple(c) for c in components}, {(0, 1), (2, 3), (4,)})

    def test_shortest_paths_cross_check(self):
        for _ in range(25):
            n = 7
            edges = [(u, v, self.random.randrange(10)) for u in range(n) for v in range(n) if u != v and self.random.random() < .2]
            graph = [[] for _ in range(n)]
            for u, v, weight in edges:
                graph[u].append((v, weight))
            distances = graphs.floyd_warshall(n, edges)
            for start in range(n):
                self.assertEqual(graphs.dijkstra(graph, start), distances[start])
                self.assertEqual(graphs.bellman_ford(n, edges, start), distances[start])
        self.assertEqual(graphs.bellman_ford(3, [(0, 1, 2), (1, 2, -4)], 0), [0, 2, -2])
        with self.assertRaises(ValueError):
            graphs.dijkstra([[(1, -1)], []], 0)
        for algorithm in (lambda: graphs.bellman_ford(2, [(0, 1, -1), (1, 0, -1)], 0), lambda: graphs.floyd_warshall(2, [(0, 1, -1), (1, 0, -1)])):
            with self.assertRaises(ValueError):
                algorithm()

    def test_mst_against_exhaustive_trees(self):
        edges = [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 1), (2, 3, 5)]
        possible = []
        for selected in itertools.combinations(edges, 3):
            sets = structures.DisjointSet(4)
            if all(sets.union(u, v) for u, v, _ in selected):
                possible.append(sum(w for _, _, w in selected))
        graph = [[] for _ in range(4)]
        for u, v, w in edges:
            graph[u].append((v, w)); graph[v].append((u, w))
        self.assertEqual(graphs.kruskal(4, edges)[0], min(possible))
        self.assertEqual(graphs.prim(graph), min(possible))
        with self.assertRaises(ValueError):
            graphs.kruskal(3, [(0, 1, 1)])
        with self.assertRaises(ValueError):
            graphs.prim([[], []])

    def test_dynamic_programming_against_subsets(self):
        for _ in range(40):
            values = [self.random.randrange(1, 9) for _ in range(8)]
            choices = list(backtracking.subsets(values))
            longest = max(len(c) for c in choices if all(a < b for a, b in zip(c, c[1:])))
            self.assertEqual(dp.lis_length(values), longest)
            target = self.random.randrange(30)
            self.assertEqual(dp.subset_sum(values, target), any(sum(c) == target for c in choices))
            items = list(zip(values, range(1, 9)))
            best = max(sum(v for _, v in c) for c in backtracking.subsets(items) if sum(w for w, _ in c) <= 12)
            self.assertEqual(dp.knapsack(items, 12), best)
        self.assertEqual(dp.lcs_length('ABCBDAB', 'BDCABA'), 4)
        self.assertEqual(dp.edit_distance('kitten', 'sitting'), 3)
        self.assertEqual(dp.edit_distance('', 'abc'), 3)
        self.assertEqual(dp.coin_change([1, 3, 4], 6), 2)
        self.assertIsNone(dp.coin_change([2], 3))
        self.assertEqual(dp.coin_change([], 0), 0)
        with self.assertRaises(ValueError):
            dp.coin_change([0], 5)
        self.assertEqual(dp.matrix_chain([30, 35, 15, 5, 10, 20, 25]), 15125)
        self.assertEqual(dp.matrix_chain([10]), 0)

    def test_number_theory(self):
        for a in range(-12, 13):
            for b in range(-12, 13):
                divisor, x, y = nt.extended_gcd(a, b)
                self.assertEqual(divisor, math.gcd(a, b))
                self.assertEqual(a * x + b * y, divisor)
                self.assertEqual(nt.gcd(a, b), divisor)
        for _ in range(80):
            a, exponent, modulus = self.random.randrange(-100, 100), self.random.randrange(40), self.random.randrange(1, 100)
            self.assertEqual(nt.modular_power(a, exponent, modulus), pow(a, exponent, modulus))
        self.assertEqual(nt.modular_inverse(3, 11), 4)
        self.assertEqual(nt.sieve(30), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])
        self.assertEqual(nt.factorize(360), {2: 3, 3: 2, 5: 1})
        self.assertEqual(nt.factorize(1), {})
        self.assertEqual(nt.chinese_remainder([(2, 3), (3, 5), (2, 7)]), (23, 105))
        self.assertEqual(nt.chinese_remainder([(2, 4), (6, 8)]), (6, 8))
        with self.assertRaises(ValueError):
            nt.chinese_remainder([(1, 2), (0, 4)])
        with self.assertRaises(ValueError):
            nt.modular_inverse(6, 9)

    def test_sequences(self):
        self.assertEqual(sequences.prefix_sums([2, -3, 5]), [0, 2, -1, 4])
        for width in range(1, 9):
            values = [3, 1, 5, 5, -1, 7, 2, 0]
            self.assertEqual(sequences.sliding_maximum(values, width), [max(values[i:i + width]) for i in range(len(values) - width + 1)])
        self.assertEqual(sequences.merge_intervals([(5, 6), (1, 3), (3, 4)]), [(1, 4), (5, 6)])
        self.assertEqual(sequences.interval_scheduling([(0, 4), (1, 2), (2, 3), (3, 5)]), [(1, 2), (2, 3), (3, 5)])
        self.assertEqual(sequences.maximum_subarray([-4, -2, -7]), -2)
        self.assertEqual(sequences.maximum_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6)
        self.assertEqual(sequences.huffman_cost([5, 9, 12, 13, 16, 45]), 224)
        self.assertEqual(sequences.huffman_cost([7]), 0)

    def test_backtracking(self):
        self.assertEqual(list(backtracking.unique_permutations([1, 1, 2])), [(1, 1, 2), (1, 2, 1), (2, 1, 1)])
        self.assertEqual(len(list(backtracking.n_queens(8))), 92)
        self.assertEqual(list(backtracking.n_queens(0)), [()])
        self.assertEqual(list(backtracking.n_queens(3)), [])
        self.assertEqual(list(backtracking.subsets([])), [()])


if __name__ == '__main__':
    unittest.main()
