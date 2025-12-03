def find_max_joltage(bank):
    """Find the maximum 2-digit number possible from a bank of batteries."""
    max_joltage = 0
    
    # Try all pairs of positions (i, j) where i < j
    for i in range(len(bank)):
        for j in range(i + 1, len(bank)):
            # Form the 2-digit number: first digit is at position i, second at position j
            current = int(bank[i] + bank[j])
            if current > max_joltage:
                max_joltage = current
    
    return max_joltage

def main():
    total_joltage = 0
    count = 0
    
    # Try to read from input.txt
    try:
        with open('input.txt', 'r') as f:
            banks = f.readlines()
        
        print(f"Found {len(banks)} banks")
        
        for bank in banks:
            bank = bank.strip()
            if bank:  # Skip empty lines
                max_jolt = find_max_joltage(bank)
                total_joltage += max_jolt
                count += 1
                # Optional: print progress for debugging
                if count % 10 == 0:
                    print(f"Processed {count} banks...")
        
        print(f"\nTotal output joltage: {total_joltage}")
        
    except FileNotFoundError:
        print("Error: input.txt file not found!")
        print("Please make sure input.txt is in the same directory as the script.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()