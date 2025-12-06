def solve_part2():
    with open('input.txt', 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    

    max_len = max(len(line) for line in lines)
    padded = [line.ljust(max_len) for line in lines]
    
    
    number_lines = padded[:-1]
    op_line = padded[-1]
    
    print(f"Read {len(lines)} lines total")
    print(f"Number lines: {len(number_lines)}")
    print(f"First number line length: {len(number_lines[0])}")
    print(f"Operation line length: {len(op_line)}")
    
  
    separator_cols = []
    for col in range(max_len):
        all_spaces = True
        for line in padded:
            if col < len(line) and line[col] != ' ':
                all_spaces = False
                break
        if all_spaces:
            separator_cols.append(col)
    

    problems = []
    prev_sep = -1
    for sep in separator_cols + [max_len]:
        if sep > prev_sep + 1:
            start = prev_sep + 1
            end = sep
            
         
            operation = None
            for col in range(start, end):
                if op_line[col] in ('+', '*'):
                    operation = op_line[col]
                    break
            
            if operation:
                problems.append({
                    'start': start,
                    'end': end,
                    'operation': operation
                })
        
        prev_sep = sep
    
   
    problems.reverse()
    
    print(f"\nFound {len(problems)} problems")
    
    # Process each problem
    total = 0
    for prob_idx, problem in enumerate(problems):
        start = problem['start']
        end = problem['end']
        operation = problem['operation']


        numbers = []
        
        for col in range(end - 1, start - 1, -1):
            # Get digits in this column (top to bottom)
            col_digits = []
            for row in range(len(number_lines)):
                if col < len(number_lines[row]) and number_lines[row][col].isdigit():
                    col_digits.append(number_lines[row][col])
                else:
                    col_digits.append(' ')
            
 
            if any(d.isdigit() for d in col_digits):
  
                while col_digits and col_digits[-1] == ' ':
                    col_digits.pop()
                
   
                num_str = ''.join(col_digits)
                if num_str:
                    try:
                        num = int(num_str)
                        numbers.append(num)
                    except ValueError:
                        pass
        

        if operation == '+':
            result = sum(numbers)
        else:
            result = 1
            for n in numbers:
                result *= n
        
        total += result
    
    print(f"Grand total (Part 2): {total}")
    return total

if __name__ == "__main__":
    solve_part2()