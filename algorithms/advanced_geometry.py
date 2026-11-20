"""以整數座標驗證幾何邊界；距離回傳平方值，避免不必要的開根號。"""
from bisect import bisect_left

def rectangle_union_area(rectangles):
    """掃描線 + 覆蓋長度 Segment Tree，O(n log n)，矩形 (x1,y1,x2,y2)。"""
    if any((x1 > x2 or y1 > y2 for x1, y1, x2, y2 in rectangles)):
        raise ValueError('reversed rectangle')
    rectangles = [r for r in rectangles if r[0] != r[2] and r[1] != r[3]]
    if not rectangles:
        return 0
    ys = sorted({y for _, y1, _, y2 in rectangles for y in (y1, y2)})
    n = len(ys) - 1
    cover = [0] * (4 * n)
    length = [0] * (4 * n)

    def update(node, left, right, ql, qr, delta):
        if qr <= left or right <= ql:
            return
        if ql <= left and right <= qr:
            cover[node] += delta
        else:
            middle = (left + right) // 2
            update(node * 2, left, middle, ql, qr, delta)
            update(node * 2 + 1, middle, right, ql, qr, delta)
        if cover[node]:
            length[node] = ys[right] - ys[left]
        elif right - left == 1:
            length[node] = 0
        else:
            length[node] = length[node * 2] + length[node * 2 + 1]
    events = sorted(((x, delta, bisect_left(ys, y1), bisect_left(ys, y2)) for x1, y1, x2, y2 in rectangles for x, delta in ((x1, 1), (x2, -1))))
    area = 0
    previous = events[0][0]
    for x, delta, left, right in events:
        area += (x - previous) * length[1]
        update(1, 0, n, left, right, delta)
        previous = x
    return area

def convex_hull(points):
    """Monotone chain，O(n log n)，逆時針，去重且不保留邊上的中間點。"""
    points = sorted(set(map(tuple, points)))
    if len(points) < 2:
        return points

    def cross(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    lower = []
    upper = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

def closest_pair_squared(points):
    """分治最近點對，O(n log²n)；少於兩點回傳 None，重複點距離為 0。"""
    ordered = sorted(map(tuple, points))
    if len(ordered) < 2:
        return None

    def distance(a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    def visit(values):
        if len(values) <= 3:
            return min((distance(a, b) for i, a in enumerate(values) for b in values[i + 1:]), default=float('inf'))
        middle = len(values) // 2
        x = values[middle][0]
        best = min(visit(values[:middle]), visit(values[middle:]))
        if best == 0:
            return 0
        strip = sorted((p for p in values if (p[0] - x) ** 2 < best), key=lambda p: p[1])
        for i, a in enumerate(strip):
            for b in strip[i + 1:i + 8]:
                if (b[1] - a[1]) ** 2 >= best:
                    break
                best = min(best, distance(a, b))
        return best
    return visit(ordered)
