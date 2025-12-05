def solve_optimized():
    with open('input.txt', 'r') as f:
        content = f.read()
    
    parts = content.strip().split('\n\n')
    ranges_text, ids_text = parts
    
    ranges = []
    for line in ranges_text.strip().split('\n'):
        a, b = map(int, line.strip().split('-'))
        ranges.append((a, b))
    
    ids = []
    for line in ids_text.strip().split('\n'):
        ids.append(int(line.strip()))
    
    print(f"Ranges: {len(ranges)}, IDs: {len(ids)}")
    
    ranges.sort(key=lambda x: x[0])
    
    fresh_count = 0
    
    for ingredient_id in ids:
       
        left, right = 0, len(ranges) - 1
        found = False
        
        while left <= right:
            mid = (left + right) // 2
            start, end = ranges[mid]
            
            if ingredient_id < start:
                right = mid - 1
            elif ingredient_id > end:
                left = mid + 1
            else:
            
                found = True
                break
        
        if found:
            fresh_count += 1
    
    return fresh_count

if __name__ == "__main__":
    result = solve_optimized()
    print(f"\nANSWER: {result}")