from collections import defaultdict, deque
import sys

def read_input(filename):
    graph = defaultdict(list)
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if ':' not in line:
                continue
            source, targets = line.split(':', 1)
            source = source.strip()
            for target in targets.split():
                graph[source].append(target.strip())
    return graph

def topological_sort(graph, start, end):
    """Check if graph is DAG and return topological order if possible."""
    indegree = defaultdict(int)
    for node in graph:
        for neighbor in graph[node]:
            indegree[neighbor] += 1
    
    queue = deque([node for node in graph if indegree[node] == 0])
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(topo_order) != len(graph):
        return None 
    
    return topo_order

def count_paths_dp(graph, start, end):
    """Count paths using DP if graph is DAG."""
    topo_order = topological_sort(graph, start, end)
    if topo_order is None:
        
        return None
    
    
    dp = defaultdict(int)
    dp[end] = 1
    
    for node in reversed(topo_order):
        if node == end:
            continue
        for neighbor in graph[node]:
            dp[node] += dp[neighbor]
    
    return dp[start]

def find_all_paths_iterative(graph, start, end):
    """Find all paths using iterative DFS with stack."""
    stack = [(start, [start], {start})]
    paths = []
    
    while stack:
        node, path, visited = stack.pop()
        if node == end:
            paths.append(path)
            continue
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                new_visited = visited.copy()
                new_visited.add(neighbor)
                stack.append((neighbor, path + [neighbor], new_visited))
    
    return paths

def main():
    if len(sys.argv) < 2:
        print("Usage: python reactor.py input.txt")
        return
    
    filename = sys.argv[1]
    graph = read_input(filename)
    
    if 'you' not in graph:
        print("Error: 'you' node not found in graph")
        return
    if 'out' not in set().union(*[set(v) for v in graph.values()]):
        found_out = False
        for node in graph:
            if node == 'out':
                found_out = True
                break
        if not found_out:

            for node in graph:
                if 'out' in graph[node]:
                    found_out = True
                    break
        if not found_out:
            print("Error: 'out' node not found in graph")
            return
    
    dp_count = count_paths_dp(graph, 'you', 'out')
    if dp_count is not None:
        print(f"Graph is a DAG. Number of paths (DP): {dp_count}")
    else:
        print("Graph contains cycles, using DFS approach...")
    

    paths = find_all_paths_iterative(graph, 'you', 'out')
    print(f"Total paths found (DFS): {len(paths)}")
    
    if paths:
        avg_length = sum(len(p) for p in paths) / len(paths)
        print(f"Average path length: {avg_length:.2f}")
        print(f"Shortest path length: {min(len(p) for p in paths)}")
        print(f"Longest path length: {max(len(p) for p in paths)}")
        
        if len(paths) <= 5:
            for i, path in enumerate(paths[:5], 1):
                print(f"\nPath {i} (length {len(path)}):")
                print(" -> ".join(path))
        elif dp_count is None:
            print(f"\nFirst path (of {len(paths)}):")
            print(" -> ".join(paths[0]))

if __name__ == "__main__":
    main()