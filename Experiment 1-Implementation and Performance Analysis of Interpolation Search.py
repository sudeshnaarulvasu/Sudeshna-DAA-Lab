import time
import random
import sys
def interpolation_search(arr, target):
     low, high = 0, len(arr) - 1
     comparisons = 0
     while low <= high and arr[low] <= target <= arr[high]:
          comparisons += 1
          if low == high:
               if arr[low] == target:
                    return low, comparisons
               return -1, comparisons
          # Interpolation formula
          pos = low + int(((target - arr[low]) * (high - low))/ (arr[high] - arr[low]))
          if arr[pos] == target:
               return pos, comparisons
          elif arr[pos] < target:
               low = pos + 1
          else:
               high = pos - 1
     return -1, comparisons
def binary_search(arr, target):
     """Binary Search for comparison"""
     low, high = 0, len(arr) - 1
     comparisons = 0
     while low <= high:
          comparisons += 1
          
          mid = (low + high) // 2
          if arr[mid] == target:
               return mid, comparisons
          elif arr[mid] < target:
               low = mid + 1
          else:
               high = mid - 1
     return -1, comparisons
def performance_analysis():
     sizes = [1000, 5000, 10000, 50000, 100000]
     print(f"{'Size':>10} {'IS Time(ms)':>14} {'BS Time(ms)':>14} "f"{'IS Comparisons':>16} {'BS Comparisons':>16}")
     print('-' * 75)
     for size in sizes:
          arr = sorted(random.sample(range(size * 10), size))
          target = arr[random.randint(0, size - 1)]
          # Interpolation Search timing
          start = time.perf_counter()
          for _ in range(100):
               idx_is, comp_is = interpolation_search(arr, target)
          is_time = (time.perf_counter() - start) / 100 * 1000
          # Binary Search timing
          start = time.perf_counter()
          for _ in range(100):
               idx_bs, comp_bs = binary_search(arr, target)
          bs_time = (time.perf_counter() - start) / 100 * 1000
          print(f"{size:>10} {is_time:>14.4f} {bs_time:>14.4f} "f"{comp_is:>16} {comp_bs:>16}")
# --- Main ---
arr = [2,5,10,15,23,35,48,60,75,90,105,120]
target = 35
idx, comps = interpolation_search(arr, target)
print(f"Array: {arr}")
print(f"Searching for: {target}")
print(f"Found at index: {idx}, Comparisons: {comps}")
print()
performance_analysis()

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


# Quick Demonstration of Big-O Table & Runtime Estimation
demo_analysis = [
    {"name": "Binary Search", "best": "O(1)", "avg": "O(log N)", "worst": "O(log N)", "space": "O(1)"},
    {"name": "Interpolation", "best": "O(1)", "avg": "O(log log N)", "worst": "O(N)", "space": "O(1)"},
    {"name": "KMP Search", "best": "O(N)", "avg": "O(N+M)", "worst": "O(N+M)", "space": "O(M)"},
    {"name": "Dijkstra", "best": "O(V log V)", "avg": "O(E log V)", "worst": "O(E log V)", "space": "O(V)"}
]
print_complexity_sheet(demo_analysis)

# Example runtime scaling (e.g., if O(N log N) took 5ms for N=10,000, estimate for N=1,000,000,000)
est = estimate_future_runtime(10000, 5.0, 1000000000, "O(N log N)")
print(f"Est. O(N log N) time for N=1,000,000,000 based on 5ms @ 10k: {est}")
