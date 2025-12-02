def solve_part2(filename):
    with open(filename, 'r') as f:
        data = f.read().strip()

    total = 0
    
    for range_str in data.split(','):
        if not range_str.strip():
            continue
            
        start, end = map(int, range_str.split('-'))
        
        invalid_numbers = set()
        
        min_len = len(str(start))
        max_len = len(str(end))
        
        for length in range(min_len, max_len + 1):
            min_num_of_len = 10**(length - 1) if length > 1 else 0
            max_num_of_len = 10**length - 1
            
            if end < min_num_of_len or start > max_num_of_len:
                continue
        
            for k in range(2, length + 1):
                if length % k != 0:
                    continue
                
                part_len = length // k
                
                min_part = 10**(part_len - 1) if part_len > 1 else 1
                max_part = 10**part_len - 1
                
                min_possible = int(str(min_part) * k)
                max_possible = int(str(max_part) * k)
                
                if min_possible > end or max_possible < start:
                    continue
                
                for part_num in range(min_part, max_part + 1):
                    num_str = str(part_num) * k
                    num = int(num_str)
                    
                    if num > end:
                        break
                    
                    if start <= num <= end and len(str(num)) == length:
                        invalid_numbers.add(num)
        
        total += sum(invalid_numbers)
    
    return total

if __name__ == "__main__":

    print("Testing with example...")
    
    test_input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212121-2121212124"
    
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
        tmp.write(test_input)
        tmp_filename = tmp.name
    
    try:
        test_result = solve_part2(tmp_filename)
        print(f"Test result: {test_result} (expected: 4174379265)")
        
        if test_result == 4174379265:
            print("✓ Test passed!")
        else:
            print("✗ Test failed!")
    finally:
        os.unlink(tmp_filename)
    
    print("\n" + "="*50 + "\n")

    print("Solving for actual input (input.txt)...")
    result = solve_part2("input.txt")
    print(f"\nPart 2 Answer: {result}")