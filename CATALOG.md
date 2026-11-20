# 80 種演算法與資料結構

所有 API 從 repo 根目錄匯入 algorithms。n/m 為輸入長度，k 為值域或硬幣種類，V/E 為頂點／邊，C 為背包容量，A/T 為目標值，w 為大整數內部字組寬度。複雜度採一般比較與整數運算模型；Python 大整數的位元成本另計。

## 排序

來源：[algorithms/sorting.py](algorithms/sorting.py)

| 名稱 | 用途與條件 | 時間複雜度 |
|---|---|---|
| insertion_sort | 接近排序完成的小資料 | O(n²)／最佳 O(n) |
| merge_sort | 穩定排序與分治 | O(n log n) |
| quick_sort | 三分區快速排序 | 平均 O(n log n)，最差 O(n²) |
| heap_sort | 堆積連續取最小值 | O(n log n) |
| counting_sort | 小整數值域 | O(n+k) |
| radix_sort | 非負整數逐位分桶 | O(d(n+10)) |

## 搜尋

來源：[algorithms/searching.py](algorithms/searching.py)

| 名稱 | 用途與條件 | 時間複雜度 |
|---|---|---|
| lower_bound | 第一個 >=target 的位置 | O(log n) |
| upper_bound | 第一個 >target 的位置 | O(log n) |
| binary_search | 找最左相同值 | O(log n) |
| rotated_search | 旋轉且無重複的排序陣列 | O(log n) |
| quickselect | 第 k 小，0-based | 平均 O(n)，最差 O(n²) |

## 字串

來源：[algorithms/strings.py](algorithms/strings.py)

| 名稱 | 用途與條件 | 時間複雜度 |
|---|---|---|
| generate_lps | KMP 的最長前綴後綴表；來源在根目錄 kmp.py | O(m) |
| kmp | 含重疊匹配的位置；來源在根目錄 kmp.py | O(n+m) |
| z_function | 每個後綴與原文的共同前綴 | O(n) |
| rabin_karp | 滾動雜湊，原文比對排除碰撞 | 平均 O(n+m)，最差 O(nm) |
| manacher_length | 最長連續回文長度 | O(n) |
| Trie | 單字存在與前綴查詢 | 每次 O(字串長度) |

## 資料結構

來源：[algorithms/structures.py](algorithms/structures.py)

| 名稱 | 用途與條件 | 時間複雜度 |
|---|---|---|
| DisjointSet | 連通分量與依大小合併 | 攤銷 O(α(n)) |
| FenwickTree | 單點增加、前綴與區間總和 | 更新／查詢 O(log n) |
| SegmentTree | 單點指定、區間最小值 | 建樹 O(n)，更新／查詢 O(log n) |
| SparseTable | 靜態區間最小值 | 建表 O(n log n)，查詢 O(1) |

## 圖論

來源：[algorithms/graphs.py](algorithms/graphs.py)

| 名稱 | 用途與條件 | 時間複雜度 |
|---|---|---|
| bfs | 無權圖的最短距離 | O(V+E) |
| dfs | 深度優先造訪順序 | O(V+E) |
| topological_sort | DAG 工作依賴；偵測有向環 | O(V+E) |
| dijkstra | 非負加權單源最短路徑 | O((V+E) log V) |
| bellman_ford | 負邊與起點可達負環 | O(VE) |
| floyd_warshall | 所有點對最短距離與負環 | O(V³) |
| kruskal | 邊列表的最小生成樹 | O(E log E) |
| prim | 鄰接表的最小生成樹 | O(E log V) |
| strongly_connected_components | Kosaraju，迭代式雙向走訪 | O(V+E) |
| bipartite_coloring | 二分圖染色，失敗回傳 None | O(V+E) |

## 動態規劃

來源：[algorithms/dynamic_programming.py](algorithms/dynamic_programming.py)

| 名稱 | 用途與條件 | 時間複雜度 |
|---|---|---|
| lis_length | 嚴格遞增子序列，tails | O(n log n) |
| lcs_length | 最長共同子序列 | O(nm) |
| edit_distance | 插入、刪除與替換 | O(nm) |
| knapsack | 每件物品最多一次的背包 | O(nC) |
| coin_change | 不限次數的最少硬幣 | O(kA) |
| subset_sum | 非負子集合和，整數 bitset | O(n ceil(T/w)) 位元組塊運算 |
| matrix_chain | 矩陣鏈括號化成本 | O(n³) |

## 數論

來源：[algorithms/number_theory.py](algorithms/number_theory.py)

| 名稱 | 用途與條件 | 時間複雜度 |
|---|---|---|
| gcd | 歐幾里得最大公因數 | O(log min(|a|,|b|)) |
| extended_gcd | Bézout 係數 | O(log min(|a|,|b|)) |
| modular_inverse | 模反元素，需互質 | O(log modulus) |
| modular_power | 非負指數平方乘法 | O(log exponent) |
| sieve | Eratosthenes 質數篩 | O(n log log n) |
| factorize | 正整數試除分解 | O(√n) |
| chinese_remainder | 廣義 CRT，可處理不互質模數 | 每次合併 O(log M) |

## 序列與貪婪

來源：[algorithms/sequences.py](algorithms/sequences.py)

| 名稱 | 用途與條件 | 時間複雜度 |
|---|---|---|
| prefix_sums | 連續區間和的預處理 | 建表 O(n)，查詢 O(1) |
| sliding_maximum | 單調佇列滑動視窗 | O(n) |
| merge_intervals | 閉區間排序後合併 | O(n log n) |
| interval_scheduling | 最多非重疊活動 | O(n log n) |
| maximum_subarray | Kadane 非空最大連續和 | O(n) |
| huffman_cost | 最優合併的總成本 | O(n log n) |

## 回溯與枚舉

來源：[algorithms/backtracking.py](algorithms/backtracking.py)

| 名稱 | 用途與條件 | 時間複雜度 |
|---|---|---|
| unique_permutations | 不重複排列 | 最差 O(n! n) |
| n_queens | 逐列擺放皇后 | 搜尋最差 O(n!)；輸出另需 O(n/解) |
| subsets | 位元遮罩子集合 | O(2^n n) |

## 往 CPE 三星題型延伸

以下新增 26 個進階單元，與前面 54 個合計 **80 種**。同一演算法的 UVa 輸入輸出包裝不再重複計數。題目路線與官方來源見 [CPE_GUIDE.md](CPE_GUIDE.md)。

### 進階圖論

來源：[algorithms/advanced_graphs.py](algorithms/advanced_graphs.py)

| 名稱 | 用途 | 複雜度／條件 |
|---|---|---|
| max_flow | Edmonds–Karp 最大流 | O(VE²) |
| min_cost_flow | 帶負費用邊的逐次最短增廣路 | O(FVE)，拒絕可達負環 |
| hopcroft_karp | 二分圖最大匹配 | O(E√V)，DFS 使用遞迴 |
| hungarian | 矩形最小成本指派 | O(n²m)，n<=m |
| bridges | 多重無向圖的橋 | O(V+E) |
| articulation_points | 割點與 DFS 根特例 | O(V+E) |
| euler_trail | Hierholzer，平行邊與自環 | O(V+E) |

### 進階區間與樹

來源：[algorithms/advanced_structures.py](algorithms/advanced_structures.py)

| 名稱 | 用途 | 複雜度／條件 |
|---|---|---|
| LowestCommonAncestor | Binary lifting 最近共同祖先 | 建表 O(n log n)，查詢 O(log n) |
| LazyRangeSum | 區間加值與總和的延遲標記 | 建樹 O(n)，操作 O(log n) |
| PersistentKth | 持久化前綴版本與區間第 k 小 | 建樹 O(n log n)，查詢 O(log n) |
| mo_distinct | Mo 離線區間不同值數 | O((n+q)√n) |

### 計算幾何

來源：[algorithms/advanced_geometry.py](algorithms/advanced_geometry.py)

| 名稱 | 用途 | 複雜度／條件 |
|---|---|---|
| rectangle_union_area | 掃描線與覆蓋長度樹求矩形聯集 | O(n log n) |
| convex_hull | Monotone chain 凸包 | O(n log n) |
| closest_pair_squared | 分治最近點對，回傳平方距離 | O(n log²n) |

### 進階字串

來源：[algorithms/advanced_strings.py](algorithms/advanced_strings.py)

| 名稱 | 用途 | 複雜度／條件 |
|---|---|---|
| suffix_array | 倍增後綴陣列 | O(n log²n) |
| lcp_array | Kasai 相鄰後綴共同前綴 | O(n) |
| AhoCorasick | Failure links 多模式匹配 | 建表與輸出相關；搜尋 O(n+matches) |

### 競程進階 DP

來源：[algorithms/advanced_dp.py](algorithms/advanced_dp.py)

| 名稱 | 用途 | 複雜度／條件 |
|---|---|---|
| traveling_salesman | Held–Karp 旅行推銷員 | O(n²2^n) |
| hamiltonian_paths | 恰好走訪每點的有向路徑數 | O((V+E)2^V) |
| optimal_bst | 根深度 0 的最佳二元搜尋樹 | O(n³) |
| cutting_sticks | 區間 DP 切木棒 | O(n³) |
| distinct_subsequences | 不同子序列的計數 | O(nm) |
| ferry_loading | 兩側容量與路徑還原 | O(nC) |
| chopsticks | 兩短一長的筷子配組 | O(kn) |
| tug_of_war | 人數限制的 bitset 分隊 | O(nk ceil(S/w)) 位元字組運算 |
| longest_descending_path | 排序後四方向下降 DP | O(hw log(hw)) |
