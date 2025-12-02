def solve_part1(filename):
    with open(filename, 'r') as f: 
        data = f.read().strip()
    
    total = 0
    
    for range_str in data.split(','):
        if not range_str.strip():
            continue
            
        start, end = map(int, range_str.split('-'))
        min_len = len(str(start))
        max_len = len(str(end))
        
        for length in range(2, max_len + 1, 2):
            if length < min_len:
                continue
                
            half_len = length // 2
            multiplier = 10**half_len + 1
            
            min_n = 10**(half_len - 1)
            max_n = 10**half_len - 1
            
            if length == min_len:
                min_n = max(min_n, (start + multiplier - 1) // multiplier)
            
            if length == max_len:
                max_n = min(max_n, end // multiplier)
            
            if length > min_len and length < max_len:
                min_n = 10**(half_len - 1)
                max_n = 10**half_len - 1
            
            if min_n <= max_n:
                count = max_n - min_n + 1
                total += multiplier * (min_n + max_n) * count // 2
    
    return total

if __name__ == "__main__":
    result = solve_part1("input.txt")
    print(f"Part 1 Answer: {result}")