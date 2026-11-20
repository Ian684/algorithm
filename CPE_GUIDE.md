# 往 CPE 三星題型的練習路線

這一階段練習區間 DP、狀態壓縮、圖論結構與進階字串。星等依所採題庫而異；下面的題名與輸入輸出依 UVa 官方題面，不把本機通過標示成線上 AC。

## 可執行題目入口

在 repo 根目錄執行，例如：

    python -m cpe_solutions.uva10003 < input.txt
    python -m unittest discover -s tests -v

| UVa | 技巧／要注意的條件 | 官方題目 |
|---|---|---|
| 10003 Cutting Sticks | 區間內枚舉第一刀；不是每次選最短段 | [題面](https://onlinejudge.org/external/100/10003.pdf) |
| 10069 Distinct Subsequences | 倒序更新 target，Python 整數避免計數溢位 | [題面](https://onlinejudge.org/external/100/10069.pdf) |
| 10304 Optimal Binary Search Tree | 根的成本是 0 層，不是 1 層 | [題面](https://onlinejudge.org/external/103/10304.pdf) |
| 10032 Tug of War | 不只重量差小，人數差也必須至多一 | [題面](https://onlinejudge.org/external/100/10032.pdf) |
| 10271 Chopsticks | 題目客人數 K 要再加 8；先確保每組有第三支長筷 | [題面](https://onlinejudge.org/external/102/10271.pdf) |
| 10285 Longest Run on a Snowboard | 四方向嚴格下降；平台等高不能移動 | [題面](https://onlinejudge.org/external/102/10285.pdf) |
| 10261 Ferry Loading | 船長公尺先轉公分；不能跳過車；還原左右停放 | [題面](https://onlinejudge.org/external/102/10261.pdf) |

官方範例的輸入與輸出收錄在 `tests/test_cpe_formats.py`。渡輪另用自訂多案例檢查格式、單位與容量；沒有把自訂案例稱為官方範例。

## 建議練習順序

1. 先完成 Cutting Sticks、Optimal BST。寫清楚區間代表什麼，列舉最後／第一個決定的選擇。
2. 做 Distinct Subsequences、Chopsticks、Tug of War。觀察一維壓縮後哪些迴圈必須倒序，以及「重量達標」與「人數也達標」的差別。
3. 做 Ferry Loading 與 Snowboard。先寫狀態，再練路徑還原或依相依順序計算；不要只輸出最終數字。
4. 再進入 max-flow、二分匹配、Hungarian、LCA、延遲標記與持久化樹。先用小資料暴力找答案，對照後再放大資料。
5. 最後練後綴陣列、LCP、Aho–Corasick、凸包、最近點對與掃描線。手算失敗連結或掃描事件，避免只記程式碼。

## 有刻意處理的邊界

- 橋與割點用 edge id 排除父邊，避免把兩條平行邊誤判成橋。
- Euler 路徑除了奇度數條件，也檢查有邊的部分是否連通。
- Min-cost flow 使用反向殘餘邊修正先前選擇，測試含需要改配的例子；可達負費用環會明確拒絕。
- 持久化樹查的是兩個前綴版本的差，k 從 0 開始，區間左閉右開。
- 矩形聯集在同一個 x 的事件間面積增量為 0，重疊覆蓋需靠 cover 計數，不是單純切換布林值。
- LCP 用 Unicode 字元索引；空字串回傳空陣列。Aho 的重複模式保留不同 pattern id。

## 複雜度與使用範圍

複雜度完整列在 CATALOG.md。狀態壓縮只適合小 n；subset sum／Tug of War 的 bitset 成本取決於總和。Low-link 與 Hopcroft–Karp 使用遞迴，深圖會受到 Python 遞迴深度限制；要挑戰大限制時，應改成迭代版或評估執行環境。不同題目的星等與線上時限不等同於單一演算法的難度。
