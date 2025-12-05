def solve_part2():
    
    with open('input.txt', 'r') as f:
        content = f.read()
    

    ranges_text = content.strip().split('\n\n')[0]
    
    
    ranges = []
    for line in ranges_text.strip().split('\n'):
        start, end = map(int, line.strip().split('-'))
        ranges.append((start, end))
    
    print(f"Parsed {len(ranges)} ranges")
    
    
    ranges.sort(key=lambda x: x[0])
    
    
    merged = []
    current_start, current_end = ranges[0]
    
    for start, end in ranges[1:]:
        if start <= current_end + 1: 
            current_end = max(current_end, end)
        else:
            
            merged.append((current_start, current_end))
            current_start, current_end = start, end
    
    merged.append((current_start, current_end))
    
    print(f"After merging: {len(merged)} ranges")
    
    
    total_ids = 0
    for start, end in merged:
        total_ids += (end - start + 1) 
    
    return total_ids, merged


def solve_part2_simple():
    """Alternative simpler approach"""
    with open('input.txt', 'r') as f:
        content = f.read()
 
    ranges_text = content.strip().split('\n\n')[0]
    
 
    ranges = []
    for line in ranges_text.strip().split('\n'):
        start, end = map(int, line.strip().split('-'))
        ranges.append((start, end))
    

    ranges.sort()
    merged = []
    
    for start, end in ranges:
       
        if not merged or start > merged[-1][1] + 1:
            merged.append([start, end])
        else:
            
            merged[-1][1] = max(merged[-1][1], end)
    

    total = 0
    for start, end in merged:
        total += (end - start + 1)
    
    return total, merged


if __name__ == "__main__":

    total1, merged1 = solve_part2()
    total2, merged2 = solve_part2_simple()
    
    print("\nMethod 1:")
    print(f"Total fresh ingredient IDs: {total1}")
    print(f"Merged into {len(merged1)} ranges")
    
    print("\nMethod 2:")
    print(f"Total fresh ingredient IDs: {total2}")
    print(f"Merged into {len(merged2)} ranges")
    
   
    if total1 == total2:
        print(f"\n✓ Both methods agree: {total1}")
    else:
        print(f"\n✗ Discrepancy: {total1} vs {total2}")