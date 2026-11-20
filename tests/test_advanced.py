from collections import Counter
import itertools
import random
import unittest
from algorithms.advanced_graphs import max_flow,min_cost_flow,hopcroft_karp,hungarian,bridges,articulation_points,euler_trail
from algorithms.advanced_structures import LowestCommonAncestor,LazyRangeSum,PersistentKth,mo_distinct
from algorithms.advanced_dp import traveling_salesman,hamiltonian_paths,optimal_bst,cutting_sticks,distinct_subsequences,ferry_loading,chopsticks,tug_of_war,longest_descending_path
from algorithms.advanced_strings import suffix_array,lcp_array,AhoCorasick
from algorithms.advanced_geometry import rectangle_union_area,convex_hull,closest_pair_squared


class AdvancedTests(unittest.TestCase):
    def setUp(self): self.rng=random.Random(684)

    def test_maxflow_against_all_cuts(self):
        for _ in range(60):
            n=5;edges=[(a,b,self.rng.randrange(4)) for a in range(n) for b in range(n) if a!=b and self.rng.random()<.3]
            cuts=[]
            for mask in range(1<<n):
                if not mask&1 or mask>>(n-1)&1:continue
                cuts.append(sum(c for a,b,c in edges if mask>>a&1 and not mask>>b&1))
            self.assertEqual(max_flow(n,edges,0,n-1),min(cuts))
        self.assertEqual(max_flow(2,[(0,0,9),(0,1,2),(0,1,3)],0,1),5)

    def test_min_cost_flow(self):
        edges=[(0,1,2,1),(1,3,2,2),(0,2,1,0),(2,3,1,5)]
        self.assertEqual(min_cost_flow(4,edges,0,3,3),(3,11))
        self.assertEqual(min_cost_flow(4,edges,0,3,1),(1,3))
        self.assertEqual(min_cost_flow(3,[(0,1,1,-3),(1,2,1,1)],0,2,2),(1,-2))
        with self.assertRaises(ValueError):min_cost_flow(3,[(0,1,2,-1),(1,0,2,-1)],0,2,1)
        # Residual reverse edges must be usable to repair a poor first assignment.
        edges=[(0,1,1,0),(0,2,1,0),(1,3,1,0),(1,4,1,1),(2,3,1,1),(2,4,1,100),(3,5,1,0),(4,5,1,0)]
        self.assertEqual(min_cost_flow(6,edges,0,5,2),(2,2))

    def test_matching_and_assignment_against_permutations(self):
        for _ in range(40):
            graph=[[v for v in range(4) if self.rng.random()<.5] for _ in range(3)]
            result=hopcroft_karp(graph,4)
            best=max(sum(v!=-1 for v in choice) for choice in itertools.product(range(-1,4),repeat=3) if len([v for v in choice if v!=-1])==len(set(v for v in choice if v!=-1)) and all(v==-1 or v in graph[u] for u,v in enumerate(choice)))
            self.assertEqual(sum(v!=-1 for v in result),best)
            self.assertTrue(all(v==-1 or v in graph[u] for u,v in enumerate(result)))
            costs=[[self.rng.randrange(-5,10) for _ in range(4)] for _ in range(3)]
            total,columns=hungarian(costs)
            self.assertEqual(total,min(sum(costs[u][v] for u,v in enumerate(p)) for p in itertools.permutations(range(4),3)))
            self.assertEqual(len(set(columns)),3)
        self.assertEqual(hopcroft_karp([],0),[])
        self.assertEqual(hungarian([]),(0,[]))

    def test_lowlink_against_removal(self):
        def components(n,edges,removed_vertex=None):
            graph=[[] for _ in range(n)]
            for a,b in edges:
                if removed_vertex not in (a,b):graph[a].append(b);graph[b].append(a)
            seen={removed_vertex} if removed_vertex is not None else set();count=0
            for root in range(n):
                if root in seen:continue
                count+=1;stack=[root];seen.add(root)
                while stack:
                    u=stack.pop()
                    for v in graph[u]:
                        if v not in seen:seen.add(v);stack.append(v)
            return count
        for _ in range(50):
            n=6;edges=[(a,b) for a in range(n) for b in range(a+1,n) if self.rng.random()<.3]
            baseline=components(n,edges)
            expected_bridges=[e for i,e in enumerate(edges) if components(n,edges[:i]+edges[i+1:])>baseline]
            expected_cuts=[u for u in range(n) if components(n,edges,u)>baseline]
            self.assertEqual(bridges(n,edges),expected_bridges)
            self.assertEqual(articulation_points(n,edges),expected_cuts)
        self.assertEqual(bridges(2,[(0,1),(0,1)]),[])

    def test_euler_multigraph_and_failure(self):
        for edges in ([(0,1),(1,2),(2,0)],[(0,0),(0,1),(0,1)],[(0,1),(1,2)]):
            route=euler_trail(3,edges)
            self.assertEqual(Counter(tuple(sorted(e)) for e in zip(route,route[1:])),Counter(tuple(sorted(e)) for e in edges))
        with self.assertRaises(ValueError):euler_trail(4,[(0,1),(0,2),(0,3)])
        with self.assertRaises(ValueError):euler_trail(4,[(0,1),(0,1),(2,3),(2,3)])

    def test_lca(self):
        lca=LowestCommonAncestor(7,[(0,1),(0,2),(1,3),(1,4),(2,5),(5,6)])
        for a,b,want in [(3,4,1),(3,6,0),(5,6,5),(2,2,2),(0,6,0)]:self.assertEqual(lca.query(a,b),want)
        with self.assertRaises(ValueError):LowestCommonAncestor(3,[(0,1),(0,1)])

    def test_lazy_persistent_and_mo_against_lists(self):
        values=[self.rng.randrange(-10,11) for _ in range(25)];tree=LazyRangeSum(values)
        for _ in range(120):
            a,b=sorted(self.rng.choices(range(26),k=2));delta=self.rng.randrange(-10,11)
            tree.add(a,b,delta)
            for i in range(a,b):values[i]+=delta
            l,r=sorted(self.rng.choices(range(26),k=2))
            self.assertEqual(tree.range_sum(l,r),sum(values[l:r]))
        persistent=PersistentKth(values)
        for _ in range(80):
            a,b=sorted(self.rng.sample(range(26),2));k=self.rng.randrange(b-a)
            self.assertEqual(persistent.kth(a,b,k),sorted(values[a:b])[k])
        queries=[tuple(sorted(self.rng.choices(range(26),k=2))) for _ in range(80)]
        self.assertEqual(mo_distinct(values,queries),[len(set(values[a:b])) for a,b in queries])
        self.assertEqual(LazyRangeSum([]).range_sum(0,0),0)
        self.assertEqual(mo_distinct([],[(0,0)]),[0])
        with self.assertRaises(IndexError):persistent.kth(0,0,0)

    def test_geometry_against_grid_and_pairs(self):
        for _ in range(40):
            rectangles=[]
            for __ in range(8):
                x1,x2=sorted(self.rng.sample(range(-3,5),2));y1,y2=sorted(self.rng.sample(range(-3,5),2));rectangles.append((x1,y1,x2,y2))
            cells={(x,y) for a,b,c,d in rectangles for x in range(a,c) for y in range(b,d)}
            self.assertEqual(rectangle_union_area(rectangles),len(cells))
            points=[(self.rng.randrange(-10,11),self.rng.randrange(-10,11)) for _ in range(20)]
            expected=min((a[0]-b[0])**2+(a[1]-b[1])**2 for i,a in enumerate(points) for b in points[i+1:])
            self.assertEqual(closest_pair_squared(points),expected)
        self.assertEqual(convex_hull([(0,0),(1,0),(1,1),(0,1),(.5,.5),(0,0)]),[(0,0),(1,0),(1,1),(0,1)])
        self.assertEqual(convex_hull([(0,0),(1,1),(2,2)]),[(0,0),(2,2)])
        self.assertEqual(rectangle_union_area([]),0)
        self.assertIsNone(closest_pair_squared([(0,0)]))

    def test_suffix_and_aho_against_naive(self):
        for _ in range(100):
            text=''.join(self.rng.choices('ab甲',k=20));order=suffix_array(text)
            self.assertEqual(order,sorted(range(len(text)),key=lambda i:text[i:]))
            expected=[]
            for a,b in zip(order,order[1:]):
                length=0
                while a+length<len(text) and b+length<len(text) and text[a+length]==text[b+length]:length+=1
                expected.append(length)
            self.assertEqual(lcp_array(text,order),expected)
            patterns=['a','ab','甲','aba','a']
            expected=[(i,j) for j,p in enumerate(patterns) for i in range(len(text)) if text.startswith(p,i)]
            self.assertEqual(sorted(AhoCorasick(patterns).search(text)),sorted(expected))
        self.assertEqual(suffix_array(''),[])
        self.assertEqual(lcp_array('',[]),[])
        with self.assertRaises(ValueError):AhoCorasick([''])

    def test_bitmask_dp_against_permutations(self):
        for _ in range(15):
            n=5;costs=[[self.rng.randrange(1,20) for _ in range(n)] for __ in range(n)]
            expected=min(sum(costs[a][b] for a,b in zip((0,)+order,order+(0,))) for order in itertools.permutations(range(1,n)))
            self.assertEqual(traveling_salesman(costs),expected)
            graph=[[v for v in range(n) if u!=v and self.rng.random()<.5] for u in range(n)]
            expected=sum(all(b in graph[a] for a,b in zip((0,)+p,p+(4,))) for p in itertools.permutations(range(1,4)))
            self.assertEqual(hamiltonian_paths(graph,0,4),expected)

    def test_uvatype_interval_and_counting_dp(self):
        self.assertEqual(cutting_sticks(100,[25,50,75]),200)
        self.assertEqual(cutting_sticks(10,[]),0)
        self.assertEqual(optimal_bst([10,20]),10)
        self.assertEqual(optimal_bst([1,1,1]),2)
        self.assertEqual(distinct_subsequences('babgbag','bag'),5)
        self.assertEqual(distinct_subsequences('abc',''),1)
        self.assertEqual(distinct_subsequences('','x'),0)
        self.assertEqual(chopsticks([1,2,100],1),1)
        self.assertEqual(chopsticks([1,2,3,4,100,101],2),2)
        self.assertIsNone(chopsticks([1,2],1))

    def test_ferry_and_tug_against_all_choices(self):
        for _ in range(30):
            capacity=12;cars=[self.rng.randrange(1,10) for _ in range(8)];expected=0
            for size in range(len(cars)+1):
                feasible=any(sum(cars[i] for i in range(size) if bits>>i&1)<=capacity and sum(cars[i] for i in range(size) if not bits>>i&1)<=capacity for bits in range(1<<size))
                if feasible:expected=size
                else:break
            count,sides=ferry_loading(capacity,cars)
            self.assertEqual(count,expected);self.assertEqual(len(sides),count)
            for side in ('port','starboard'):self.assertLessEqual(sum(car for car,where in zip(cars,sides) if where==side),capacity)
            weights=[self.rng.randrange(20) for _ in range(7)]
            best=min(abs(sum(weights)-2*sum(c)) for c in itertools.combinations(weights,len(weights)//2))
            a,b=tug_of_war(weights);self.assertEqual(b-a,best);self.assertEqual(a+b,sum(weights))
        self.assertEqual(ferry_loading(0,[1]),(0,[]))
        self.assertEqual(tug_of_war([]),(0,0))

    def test_descending_grid(self):
        self.assertEqual(longest_descending_path([[9,8,7],[2,3,6],[1,4,5]]),9)
        self.assertEqual(longest_descending_path([[4,4],[4,4]]),1)
        self.assertEqual(longest_descending_path([]),0)


if __name__=='__main__':unittest.main()
