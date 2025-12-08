import heapq
from typing import List, Tuple

def read_coordinates(filename: str) -> List[Tuple[int, int, int]]:
    """Read coordinates from file"""
    coordinates = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y, z = map(int, line.split(','))
                coordinates.append((x, y, z))
    return coordinates

def distance_squared(p1: Tuple[int, int, int], p2: Tuple[int, int, int]) -> int:
    """Calculate squared Euclidean distance"""
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]
    return dx*dx + dy*dy + dz*dz

class UnionFind:
    """Union-Find (Disjoint Set) data structure"""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n  
        
    def find(self, x: int) -> int:
        """Find root with path compression"""
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    
    def union(self, x: int, y: int) -> bool:
        """Union two sets, returns True if they were separate"""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
            
      
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
            
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        self.components -= 1  
        return True
    
    def get_components(self) -> int:
        """Get number of connected components"""
        return self.components

def solve_part2() -> int:
    print("Reading coordinates from input.txt...")
    
  
    coordinates = read_coordinates('input.txt')
    n = len(coordinates)
    print(f"Read {n} coordinates")
    
    total_pairs = n * (n - 1) // 2
    print(f"Calculating distances between {total_pairs:,} pairs...")
    heap = []
    
    for i in range(n):
        for j in range(i + 1, n):
            dist_sq = distance_squared(coordinates[i], coordinates[j])
            heapq.heappush(heap, (dist_sq, i, j))
    
    print("Pairs calculated and sorted")
    
    # Initialize Union-Find
    uf = UnionFind(n)
    
    print("\n=== Part 1: Making 1000 connection attempts ===")
    attempts_made = 0
    successful_in_part1 = 0
    
   
    temp_heap = []
    while heap and attempts_made < 1000:
        dist_sq, i, j = heapq.heappop(heap)
        temp_heap.append((dist_sq, i, j))  
        attempts_made += 1
        
        if uf.union(i, j):
            successful_in_part1 += 1
    
    print(f"Made {attempts_made} connection attempts")
    print(f"Successfully connected {successful_in_part1} pairs")
    print(f"Components remaining: {uf.get_components()}")
    
    for item in temp_heap:
        heapq.heappush(heap, item)
    
    
    print("\n=== Part 2: Continue until all boxes in one circuit ===")
    
   
    last_successful_connection = None
    
    while heap and uf.get_components() > 1:
        dist_sq, i, j = heapq.heappop(heap)
        
        
        if uf.find(i) != uf.find(j):
            
            last_successful_connection = (i, j, dist_sq)
            
            
            uf.union(i, j)
            
            
            if uf.get_components() == 1:
                break
    
    if last_successful_connection is None:
        print("ERROR: Never reached a single circuit!")
        return 0
    
    i, j, dist_sq = last_successful_connection
    
   
    x1 = coordinates[i][0]
    x2 = coordinates[j][0]
    
    print(f"\nLast connection that completed the circuit:")
    print(f"  Junction box 1: {coordinates[i]}, X = {x1}")
    print(f"  Junction box 2: {coordinates[j]}, X = {x2}")
    print(f"  Distance: {dist_sq**0.5:.2f}")
    
    result = x1 * x2
    return result

if __name__ == "__main__":
    print("=== Advent of Code 2025 - Day 8 - Part 2 ===")
    result = solve_part2()
    print(f"\nPart 2 Answer: {result}")
    print("="*50)