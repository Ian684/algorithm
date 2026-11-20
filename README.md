# 演算法練習

新增 **54 種演算法與資料結構**，依問題類型整理。每種實作的適用條件與複雜度寫在函式旁，完整清單見 [CATALOG.md](CATALOG.md)，推導與除錯筆記見 [NOTES.md](NOTES.md)。

原有 booth_rotate.py、exgcd_inverse.py 與 kmp.py 保留。KMP 已修正匹配後沒有把位置加入答案的問題，支援重疊匹配。

## 執行

需要 Python 3.10 以上，沒有第三方依賴。在 repo 根目錄執行：

    python demo.py
    python -m unittest discover -s tests -v

    from algorithms.graphs import dijkstra
    from algorithms.structures import FenwickTree
    from algorithms.dynamic_programming import coin_change

    print(dijkstra([[(1, 4), (2, 1)], [], [(1, 2)]], 0))  # [0, 3, 1]
    tree = FenwickTree([2, -3, 5, 7])
    print(tree.range_sum(1, 4))  # 9，左閉右開
    print(coin_change([1, 3, 4], 6))  # 2，不能直接貪婪拿 4+1+1

## 主題地圖

| 模組 | 數量 | 內容 |
|---|---:|---|
| sorting | 6 | 插入、合併、快速、堆積、計數、基數排序 |
| searching | 5 | lower/upper bound、二分、旋轉搜尋、Quickselect |
| strings | 6 | 前綴表、KMP、Z、Rabin–Karp、Manacher、Trie |
| structures | 4 | DSU、Fenwick、Segment Tree、Sparse Table |
| graphs | 10 | 走訪、拓樸、最短路、生成樹、SCC、二分圖 |
| dynamic_programming | 7 | LIS、LCS、編輯距離、背包、找零、子集合和、矩陣鏈 |
| number_theory | 7 | GCD、擴展 GCD、反元素、快速冪、篩法、分解、CRT |
| sequences | 6 | 前綴和、滑動最大值、區間、活動選擇、Kadane、Huffman 成本 |
| backtracking | 3 | 去重排列、N 皇后、子集合 |

## 怎麼確認實作

排序對照 Python sorted，二分邊界對照 bisect，字串搜尋與回文對照窮舉；最短路交叉比較，MST 對照小圖的生成樹窮舉，背包與 LIS 對照子集合枚舉。固定亂數種子 684，失敗可重現。

圖的頂點為 0 到 n-1，鄰接表需包含全部頂點；Dijkstra 禁止負權重。Quick Sort 與回溯的遞迴版適合中小輸入，極端資料需考慮 Python 遞迴深度。這些範例著重理解，不是可直接套用任何題目的萬用模板。
