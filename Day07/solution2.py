def solve_part2():
    with open('input.txt', 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    
    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0])
    
    print(f"Real input: {rows} x {cols}")
    
    
    start_r = start_c = -1
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start_r, start_c = r, c
                break
        if start_r != -1:
            break
    
    print(f"S at ({start_r}, {start_c})")
    
  
    dp = [{} for _ in range(rows)]
    

    if start_r + 1 < rows:
        dp[start_r + 1][start_c] = 1
    
    
    for r in range(rows - 1):  
        if not dp[r]:
            continue
            
        for c, count in list(dp[r].items()):
            if count == 0:
                continue
                
            cell = grid[r][c]
            
            if cell == '^':
                left_c = c - 1
                right_c = c + 1
                
                if 0 <= left_c < cols:
                    dp[r + 1][left_c] = dp[r + 1].get(left_c, 0) + count
                
            
                if 0 <= right_c < cols:
                    dp[r + 1][right_c] = dp[r + 1].get(right_c, 0) + count
            
            else:
            
                if 0 <= c < cols:
                    dp[r + 1][c] = dp[r + 1].get(c, 0) + count
    

    total = 0
    last_row = rows - 1
    if dp[last_row]:
        for count in dp[last_row].values():
            total += count
    
    return total

if __name__ == "__main__":
    print("Running part 2...")
    result = solve_part2()
    print(f"Part 2 answer: {result}")