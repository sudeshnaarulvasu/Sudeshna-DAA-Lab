import heapq
def dijkstra(graph, source):
     """
     Dijkstra's Algorithm using Min-Heap
     Time: O((V + E) log V), Space: O(V)
     graph: dict {u: [(v, weight), ...]}, 0-indexed
     """
     n = len(graph)
     dist = [float('inf')] * n
     prev = [None] * n
     dist[source] = 0
     pq = [(0, source)] # (distance, vertex)
     visited = set()
     while pq:
          d, u = heapq.heappop(pq)
          if u in visited:
               continue
          visited.add(u)
          for v, w in graph[u]:
               if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u
                    heapq.heappush(pq, (dist[v], v))
     return dist, prev
def reconstruct_path(prev, source, target):
     path = []
     node = target
     while node is not None:
          path.append(node)
          node = prev[node]
     path.reverse()
     if path[0] == source:
          return path
     return []
# --- Graph Definition (Adjacency List) ---
graph = {
0: [(1, 4), (2, 1)],
1: [(3, 1)],
2: [(1, 2), (3, 5)],
3: [(4, 3)],
4: [(5, 2)],
5: []
}
source = 0
dist, prev = dijkstra(graph, source)
print(f'Shortest paths from vertex {source}:')
print(f'{"Vertex":>8} {"Distance":>10} {"Path":>30}')
print('-' * 55)
for v in range(len(graph)):
     path = reconstruct_path(prev, source, v)
     path_str = ' -> '.join(map(str, path)) if path else 'No path'
     d = dist[v] if dist[v] != float('inf') else 'INF'
     print(f'{v:>8} {str(d):>10} {path_str:>30}')

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
# --- Shortest Path Network Visualisation ---

def visualize_shortest_paths(graph, dist, prev, source):
    """
    Prints a clear visual trace highlighting the parent-child relationships
    and exact edges utilized in Dijkstra's shortest paths.
    """
    print("\n" + "="*60)
    print(f"       DIJKSTRA SHORTEST PATH NETWORK VISUALIZATION")
    print("="*60)
    print(f"{'Target Node':^12} | {'Optimal Path Taken':^25} | {'Edge Details'}")
    print("-" * 60)
    
    for v in range(len(graph)):
        if v == source:
            print(f"{v:^12} | {f'[{v}] (Source)':^25} | Cost: 0")
            continue
            
        # Trace backwards using your reconstruct_path strategy
        path = reconstruct_path(prev, source, v)
        if not path:
            print(f"{v:^12} | {'UNREACHABLE':^25} | No valid edges")
            continue
            
        path_str = ' -> '.join(map(str, path))
        
        # Pull edge weight specifics for the final leg
        parent = prev[v]
        edge_weight = next((w for target, w in graph[parent] if target == v), None)
        
        print(f"{v:^12} | {f'[{path_str}]':<25} | (Node {parent} to {v}) with segment weight: {edge_weight}")
        
    print("="*60)

# Run the visualization utilizing your existing graph variables
visualize_shortest_paths(graph, dist, prev, source)

