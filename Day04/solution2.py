
from collections import deque

def count_removable_rolls(grid):
    rows = len(grid)
    cols = len(grid[0])
    
    board = [list(row) for row in grid]
    

    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    

    degree = [[0] * cols for _ in range(rows)]
    to_process = deque()
    
    # Initialize degrees and queue
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == '@':
                # Count initial neighbors
                count = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == '@':
                        count += 1
                degree[r][c] = count
                if count < 4:
                    to_process.append((r, c))
    
    in_queue = [[False] * cols for _ in range(rows)]
    for r, c in to_process:
        in_queue[r][c] = True
    
    removed_count = 0
    

    while to_process:
        r, c = to_process.popleft()
        in_queue[r][c] = False
        
    
        if board[r][c] != '@':
            continue
            

        if degree[r][c] >= 4:
            continue
            

        board[r][c] = '.'
        removed_count += 1
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == '@':
                degree[nr][nc] -= 1
                if degree[nr][nc] < 4 and not in_queue[nr][nc]:
                    to_process.append((nr, nc))
                    in_queue[nr][nc] = True
    
    return removed_count

def main():

    with open('input.txt', 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    
    lines = [line for line in lines if line]
    
    result = count_removable_rolls(lines)
    print(result)

if __name__ == '__main__':
    main()