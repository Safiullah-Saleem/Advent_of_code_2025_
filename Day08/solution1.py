import math
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
    """Calculate squared Euclidean distance (avoids sqrt for comparison)"""
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]
    return dx*dx + dy*dy + dz*dz

class UnionFind:
    """Union-Find (Disjoint Set) data structure"""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        
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
        return True

def solve() -> int:
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
    
   
    uf = UnionFind(n)
    
    
    print("Attempting 1000 shortest connections...")
    attempts_made = 0
    
    while heap and attempts_made < 1000:
        dist_sq, i, j = heapq.heappop(heap)
        
        
        uf.union(i, j) 
        attempts_made += 1
        
        if attempts_made % 100 == 0:
            print(f"Attempted {attempts_made}/1000 connections...")
    
    print(f"Attempted {attempts_made} connections")
    
   
    print("Counting circuit sizes...")
    circuit_sizes = {}
    for i in range(n):
        root = uf.find(i)
        circuit_sizes[root] = circuit_sizes.get(root, 0) + 1
    
   
    sizes = list(circuit_sizes.values())
    sizes.sort(reverse=True)
    
    print(f"\nAfter 1000 connection attempts:")
    print(f"Number of circuits: {len(sizes)}")
    print(f"Top circuit sizes: {sizes[:10]}")
 
    if len(sizes) < 3:
        print(f"Warning: Only {len(sizes)} circuits found")
        
        while len(sizes) < 3:
            sizes.append(1)
    
    result = sizes[0] * sizes[1] * sizes[2]
    return result

if __name__ == "__main__":
    try:
        result = solve()
        print(f"\nFinal answer (product of three largest circuits): {result}")
    except FileNotFoundError:
        print("ERROR: File 'input.txt' not found!")
        print("Please make sure 'input.txt' is in the same directory as this script.")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()