import heapq
# --- Union-Find for Kruskal ---
class UnionFind:
     def __init__(self, n):
          self.parent = list(range(n))
          self.rank = [0] * n
     def find(self, x):
          if self.parent[x] != x:
               self.parent[x] = self.find(self.parent[x]) # Path compression
          return self.parent[x]
     def union(self, x, y):
          rx, ry = self.find(x), self.find(y)
          if rx == ry: return False
          if self.rank[rx] < self.rank[ry]: rx, ry = ry, rx
          self.parent[ry] = rx
          if self.rank[rx] == self.rank[ry]: self.rank[rx] += 1
          return True
     
def kruskal(n, edges):
     """edges: list of (weight, u, v)"""
     edges.sort() # O(E log E)
     uf = UnionFind(n)
     mst = []
     cost = 0
     for w, u, v in edges:
          if uf.union(u, v):
               mst.append((u, v, w))
               cost += w
               if len(mst) == n - 1:
                    break
     return mst, cost
def prim(n, adj, start=0):
     """adj: adjacency list {u: [(v, w), ...]}"""
     INF = float('inf')
     key = [INF] * n
     parent = [-1] * n
     inMST = [False] * n
     key[start] = 0
     pq = [(0, start)]
     mst = []
     cost = 0
     while pq:
          w, u = heapq.heappop(pq)
          if inMST[u]: continue
          inMST[u] = True
          if parent[u] != -1:
               mst.append((parent[u], u, w))
               cost += w
          for v, wt in adj.get(u, []):
               if not inMST[v] and wt < key[v]:
                    key[v] = wt
                    parent[v] = u
                    heapq.heappush(pq, (wt, v))
     return mst, cost

# --- Graph Definition ---
n = 7
edges = [
(7, 0, 1), (5, 0, 3), (8, 1, 2), (9, 1, 3),
(7, 1, 4), (5, 2, 4), (15, 3, 4), (6, 3, 5),
(8, 4, 5), (9, 4, 6), (11, 5, 6)
]
adj = {}
for w, u, v in edges:
     adj.setdefault(u, []).append((v, w))
     adj.setdefault(v, []).append((u, w))
     
k_mst, k_cost = kruskal(n, edges[:])
p_mst, p_cost = prim(n, adj)

print('=== Kruskal\'s MST ===')
for u, v, w in k_mst:
     print(f' Edge ({u} - {v}) Weight: {w}')
print(f' Total MST Cost: {k_cost}')
print('\n=== Prim\'s MST ===')
for u, v, w in p_mst:
     print(f' Edge ({u} - {v}) Weight: {w}')
print(f' Total MST Cost: {p_cost}')

# --- Big-O and Scale Estimation Utility (Add to end of code) ---
def estimate_future_runtime(n_current, time_current, n_target, complexity="O(N)"):
    """
    Estimates the runtime for a larger input size based on current performance.
    complexity options: 'O(log N)', 'O(N)', 'O(N log N)', 'O(N^2)', 'O(E log V)'
    """
    import math
    try:
        if complexity == "O(log N)":
            scale = math.log2(n_target) / math.log2(n_current)
        elif complexity == "O(N log N)":
            scale = (n_target * math.log2(n_target)) / (n_current * math.log2(n_current))
        elif complexity == "O(N^2)":
            scale = (n_target ** 2) / (n_current ** 2)
        else: # Default to O(N) linear scaling
            scale = n_target / n_current
        
        estimated_time = time_current * scale
        if estimated_time >= 3600:
            return f"{estimated_time / 3600:.2f} hours"
        elif estimated_time >= 60:
            return f"{estimated_time / 60:.2f} mins"
        return f"{estimated_time:.4f} ms"
    except ZeroDivisionError:
        return "N/A"

def print_complexity_sheet(algorithms):
    """
    algorithms: list of dicts with keys 'name', 'best', 'avg', 'worst', 'space'
    """
    print("\n" + "="*80)
    print(f"{'Algorithm Analysis':^80}")
    print("="*80)
    print(f"{'Algorithm':<20} | {'Best':<12} | {'Average':<12} | {'Worst':<12} | {'Space':<12}")
    print("-" * 80)
    for alg in algorithms:
        print(f"{alg['name']:<20} | {alg['best']:<12} | {alg['avg']:<12} | {alg['worst']:<12} | {alg['space']:<12}")
    print("="*80)
# --- Graph MST Visualisation ---

def visualize_mst_edges(n, all_edges, mst_edges, algo_name):
    """
    Prints an ASCII table visualizing the original graph connections 
    and highlights which ones are selected for the MST.
    """
    # Standardize the direction of MST edges for matching
    mst_set = set()
    for u, v, w in mst_edges:
        mst_set.add((min(u, v), max(u, v)))
        
    print("\n" + "="*60)
    print(f"       GRAPH & MST PATH VISUALIZATION ({algo_name.upper()})")
    print("="*60)
    print(f"{'Edge (u-v)':^12} | {'Weight':^10} | {'Status in MST':^20}")
    print("-" * 60)
    
    for w, u, v in sorted(all_edges):
        edge_pair = (min(u, v), max(u, v))
        if edge_pair in mst_set:
            status = "   [SELECTED] "
        else:
            status = "   [Skipped Cycle/High Cost]"
            
        print(f"{f'{u} <---> {v}':<12} | {w:^10} | {status}")
    print("="*60)

# Run the visualization for Kruskal's output
visualize_mst_edges(n, edges, k_mst, "Kruskal's Algorithm")

# Run the visualization for Prim's output
visualize_mst_edges(n, edges, p_mst, "Prim's Algorithm")

