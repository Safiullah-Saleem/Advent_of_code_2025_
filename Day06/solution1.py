def solve():
    with open('input.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    

    lines = content.splitlines()
    

    while lines and not lines[-1].strip():
        lines.pop()
    
    if not lines:
        print("Empty input!")
        return 0
    
    print(f"Total lines: {len(lines)}")
    print(f"First line preview: {repr(lines[0][:80])}")
    print(f"Last line preview: {repr(lines[-1][:80])}")
    
    
    op_line = lines[-1]
    number_lines = lines[:-1]
    
    print(f"\nNumber lines: {len(number_lines)}")
    print(f"Operation line length: {len(op_line)}")
    

    all_numbers = []
    for line in number_lines:
        nums = []
        for part in line.split():
            if part:
                try:
                    nums.append(int(part))
                except:
                    pass
        all_numbers.append(nums)
    
    operations = []
    for part in op_line.split():
        if part in ('+', '*'):
            operations.append(part)
    
    print(f"\nMethod 1 (split):")
    print(f"  Numbers per line: {[len(nums) for nums in all_numbers[:3]]}...")
    print(f"  Operations: {len(operations)}")
    
    if all_numbers:
        num_problems1 = min(len(all_numbers[0]), len(operations))
        for nums in all_numbers:
            num_problems1 = min(num_problems1, len(nums))
        
        total1 = 0
        for i in range(num_problems1):
            nums = [line_nums[i] for line_nums in all_numbers if i < len(line_nums)]
            if i < len(operations):
                op = operations[i]
            else:
                op = '+'
            
            if op == '+':
                result = sum(nums)
            else:
                result = 1
                for n in nums:
                    result *= n
            
            total1 += result
        
        print(f"  Total: {total1}")

    print(f"\nMethod 2 (column-based):")
    
    # Pad all lines to same length
    max_len = max(len(line) for line in lines)
    padded = [line.ljust(max_len) for line in lines]
    
    number_lines_padded = padded[:-1]
    op_line_padded = padded[-1]
    

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
                if op_line_padded[col] in ('+', '*'):
                    operation = op_line_padded[col]
                    break
            
            if operation:
                problems.append({
                    'start': start,
                    'end': end,
                    'operation': operation,
                    'numbers': []
                })
        
        prev_sep = sep
    

    for line in number_lines_padded:
        current_num = ''
        current_problem_idx = -1
        
        for col in range(max_len):
            char = line[col]
            
            if char.isdigit():
           
                problem_idx = -1
                for i, problem in enumerate(problems):
                    if problem['start'] <= col < problem['end']:
                        problem_idx = i
                        break
                
                if problem_idx >= 0:
                    if problem_idx != current_problem_idx:
                  
                        if current_num and current_problem_idx >= 0:
                            try:
                                problems[current_problem_idx]['numbers'].append(int(current_num))
                            except:
                                pass
                        current_num = char
                        current_problem_idx = problem_idx
                    else:
                        
                        current_num += char
                elif current_num:
            
                    pass
            else:
           
                if current_num and current_problem_idx >= 0:
                    try:
                        problems[current_problem_idx]['numbers'].append(int(current_num))
                    except:
                        pass
                    current_num = ''
                    current_problem_idx = -1
        
  
        if current_num and current_problem_idx >= 0:
            try:
                problems[current_problem_idx]['numbers'].append(int(current_num))
            except:
                pass
    
    print(f"  Found {len(problems)} problems")
    
    total2 = 0
    for i, problem in enumerate(problems[:5]):
        numbers = problem['numbers']
        operation = problem['operation']
        
        if operation == '+':
            result = sum(numbers)
        else:
            result = 1
            for n in numbers:
                result *= n
        
        if i < 3:
            print(f"  Problem {i+1}: {numbers} {operation} = {result}")
        
        total2 += result
  
    for problem in problems[5:]:
        numbers = problem['numbers']
        operation = problem['operation']
        
        if operation == '+':
            result = sum(numbers)
        else:
            result = 1
            for n in numbers:
                result *= n
        
        total2 += result
    
    print(f"  ... and {len(problems)-5} more problems")
    print(f"  Total: {total2}")
    

    if abs(total1 - total2) > 100:
        print(f"\nWARNING: Methods disagree! {total1} vs {total2}")
        print("This suggests formatting issues with your input file.")
        return max(total1, total2)
    else:
        return total1

if __name__ == "__main__":
    result = solve()
    print(f"\nFinal answer: {result}")