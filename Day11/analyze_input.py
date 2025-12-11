import sys
from functools import lru_cache

DAC_BIT = 1
FFT_BIT = 2
BOTH_BITS = DAC_BIT | FFT_BIT

def load_graph(path="input.txt"):
    graph = {}
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            src, dsts = line.split(":", 1)
            src = src.strip()
            dst_list = dsts.strip().split() if dsts.strip() else []
            graph[src] = dst_list
    return graph

def solveDay_11(graph, start="svr", target="out"):
    @lru_cache(None)

    def dfs(node, mask):
        if node == "dac":
            mask |= DAC_BIT
        elif node == "fft":
            mask |= FFT_BIT

        if node == target:
            return 1 if mask == BOTH_BITS else 0

        if node not in graph or not graph[node]:
            return 0

        total = 0
        for nxt in graph[node]:
            total += dfs(nxt, mask)
        return total

    return dfs(start, 0)

if __name__ == "__main__":
    sys.setrecursionlimit(10000)

    graph = load_graph("input.txt")
    if "svr" not in graph:
        print("Warning: 'svr' not found in graph keys; result may be 0 if unreachable.")
    result = solveDay_11(graph, start="svr", target="out")
    print(result)