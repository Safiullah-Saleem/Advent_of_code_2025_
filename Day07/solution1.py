from collections import deque

def solve():
    with open('input.txt', 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    
    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0])
 
    start_r = start_c = -1
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start_r, start_c = r, c
                break
        if start_r != -1:
            break

    queue = deque()

    queue.append((start_r + 1, start_c))
  
    visited = set()
    visited.add((start_r + 1, start_c))
    
    split_count = 0
    
    while queue:
        r, c = queue.popleft()
        
    
        if r < 0 or r >= rows or c < 0 or c >= cols:
            continue
        
        cell = grid[r][c]
        
        if cell == '^':
            split_count += 1
            
        
            left_pos = (r, c - 1)
            right_pos = (r, c + 1)
            
        
            left_next = (r + 1, c - 1)
            if 0 <= c - 1 < cols and left_next not in visited:
                visited.add(left_next)
                queue.append(left_next)
        
            right_next = (r + 1, c + 1)
            if 0 <= c + 1 < cols and right_next not in visited:
                visited.add(right_next)
                queue.append(right_next)
        
        else:

            next_pos = (r + 1, c)
            if 0 <= r + 1 < rows and next_pos not in visited:
                visited.add(next_pos)
                queue.append(next_pos)
    
    return split_count

if __name__ == "__main__":
    result = solve()
    print(f"Answer: {result}")