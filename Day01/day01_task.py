def read_input():
    with open('input.txt', 'r') as file:
        return file.read().strip().splitlines()

def solve_part1():

    instructions = read_input()
    position = 50
    count = 0
    
    for instruction in instructions:
        if not instruction: 
            continue
            
        direction = instruction[0] 
        distance = int(instruction[1:]) 
        
        if direction == 'L':
            position = (position - distance) % 100
        else:  
            position = (position + distance) % 100
        
        if position == 0:
            count += 1
    
    return count

def solve_part2():
    instructions = read_input()
    position = 50
    count = 0
    
    for instruction in instructions:
        if not instruction: 
            continue
            
        direction = instruction[0]  
        distance = int(instruction[1:]) 
    
        for click in range(1, distance):
            if direction == 'L':
                temp_pos = (position - click) % 100
            else:
                temp_pos = (position + click) % 100
            
            if temp_pos == 0:
                count += 1
    
        if direction == 'L':
            position = (position - distance) % 100
        else:  
            position = (position + distance) % 100
        
        if position == 0:
            count += 1
    
    return count

print("=== Day 1: Secret Entrance ===")
print(f"Part 1 Answer: {solve_part1()}")
print(f"Part 2 Answer: {solve_part2()}")


# Part 1 answer = 1074
# Part 2 answer = 6254