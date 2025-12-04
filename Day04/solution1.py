
def count_accessible_rolls(grid):
    rows = len(grid)
    if rows == 0:
        return 0
    cols = len(grid[0])
    accessible_count = 0
    total_rolls = 0

    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '@':
                continue
            
            total_rolls += 1
        
            neighbor_count = 0
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                    neighbor_count += 1
                
                    if neighbor_count >= 4:
                        break
            
            if neighbor_count < 4:
                accessible_count += 1
    
    print(f"Total rolls: {total_rolls}")
    print(f"Accessible rolls: {accessible_count}")
    return accessible_count

def main():

    with open('input.txt', 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    lines = [line for line in lines if line]
    
    result = count_accessible_rolls(lines)
    print(f"Answer: {result}")

if __name__ == '__main__':
    main()