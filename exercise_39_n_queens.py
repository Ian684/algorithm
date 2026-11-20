def solve(n):
    result = []
    def backtrack(row, columns, diagonal1, diagonal2, board):
        if row == n:
            result.append(board[:]); return
        for column in range(n):
            if column in columns or row-column in diagonal1 or row+column in diagonal2: continue
            backtrack(row+1, columns|{column}, diagonal1|{row-column}, diagonal2|{row+column}, board+[column])
    backtrack(0,set(),set(),set(),[])
    return result
