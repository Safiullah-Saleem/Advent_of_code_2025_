def find_max_joltage_12(bank):
    n = len(bank)
    k = 12 
    
    if n == k:
        return int(bank)
    
    result = []
    start = 0
    
    for i in range(k):
        
        end = n - (k - i) + 1
        
    
        max_digit = '0'
        max_pos = start
        
        for pos in range(start, end):
            if bank[pos] > max_digit:
                max_digit = bank[pos]
                max_pos = pos
                
               
                if max_digit == '9':
                    break
        
        result.append(max_digit)
        start = max_pos + 1
    
    return int(''.join(result))

def main():

    try:
        with open('input.txt', 'r') as f:
            banks = f.read().strip().split('\n')
        
        print(f"Found {len(banks)} banks")
        
        total_joltage = 0
        
        for idx, bank in enumerate(banks):
            bank = bank.strip()
            if not bank:
                continue 
                
            max_jolt = find_max_joltage_12(bank)
            total_joltage += max_jolt
            
            if (idx + 1) % 10 == 0:
                print(f"Processed {idx + 1} banks...")
        
        print(f"\nTotal output joltage (12 batteries): {total_joltage}")
        
    except FileNotFoundError:
        print("Error: input.txt file not found!")
        print("Please make sure input.txt is in the same directory as the script.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()