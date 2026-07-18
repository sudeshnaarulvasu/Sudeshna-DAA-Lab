import random
comparison_count = 0 # Global counter
def min_max_dc(arr, low, high):
     global comparison_count
     # Base case: single element
     if low == high:
          return arr[low], arr[low]
     # Base case: two elements
     if high == low + 1:
          comparison_count += 1
          if arr[low] < arr[high]:
               return arr[low], arr[high]
          return arr[high], arr[low]
     # Divide
     mid = (low + high) // 2
     lmin, lmax = min_max_dc(arr, low, mid)
     rmin, rmax = min_max_dc(arr, mid + 1, high)

     # Conquer: combine with 2 comparisons
     comparison_count += 1
     overall_min = lmin if lmin < rmin else rmin
     comparison_count += 1
     overall_max = lmax if lmax > rmax else rmax
     return overall_min, overall_max
def min_max_naive(arr):
     mn, mx = arr[0], arr[0]
     comps = 0
     for x in arr[1:]:
          comps += 1
          if x < mn: mn = x
          comps += 1
          if x > mx: mx = x
     return mn, mx, comps
# --- Demonstration on small array ---
arr = [3, 1, 7, 4, 9, 2, 8, 5, 6, 0]
comparison_count = 0
mn, mx = min_max_dc(arr, 0, len(arr) - 1)
dc_comps = comparison_count
_, _, naive_comps = min_max_naive(arr)
print(f'Array: {arr}')
print(f'Min: {mn}, Max: {mx}')
print(f'D&C Comparisons: {dc_comps}')
print(f'Naive Comparisons: {naive_comps}')

# --- Performance Analysis ---
print(f'\n{"Size":>8} {"DC Comps":>12} {"Naive Comps":>14} {"Formula 3n/2-2":>16}')
print('-' * 56)
for size in [10, 100, 1000, 10000]:
     arr = [random.randint(1, 10000) for _ in range(size)]
     comparison_count = 0
     mn, mx = min_max_dc(arr, 0, len(arr) - 1)
     dc = comparison_count
     _, _, naive = min_max_naive(arr)
     formula = 3 * size // 2 - 2
     print(f'{size:>8} {dc:>12} {naive:>14} {formula:>16}')

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

# --- Recursive Tree Trace Visualisation ---

def visual_dc_tree_trace(arr, low, high, depth=0):
    """
    Prints a step-by-step tree visualization showing how the array is split
    and how the min/max values are combined back up the recursive stack.
    """
    indent = "    " * depth
    segment = arr[low:high+1]
    
    # Base cases
    if low == high:
        print(f"{indent}-> Base Case (Size 1): {segment} | Min/Max found: ({arr[low]}, {arr[low]})")
        return arr[low], arr[low]
        
    if high == low + 1:
        mn = min(arr[low], arr[high])
        mx = max(arr[low], arr[high])
        print(f"{indent}-> Base Case (Size 2): {segment} | Min/Max found: ({mn}, {mx})")
        return mn, mx

    # Print the current split division
    print(f"{indent} Divide Array {segment}")
    
    mid = (low + high) // 2
    
    # Left and Right Recursive paths
    lmin, lmax = visual_dc_tree_trace(arr, low, mid, depth + 1)
    rmin, rmax = visual_dc_tree_trace(arr, mid + 1, high, depth + 1)

    # Conquer stage
    overall_min = min(lmin, rmin)
    overall_max = max(lmax, rmax)
    
    print(f"{indent} Conquer: Left ({lmin},{lmax}) + Right ({rmin},{rmax}) -> Combined: ({overall_min}, {overall_max})")
    return overall_min, overall_max

# Run the recursive tree demonstration on a small slice of the array
print("\n" + "="*70)
print("             DIVIDE AND CONQUER RECURSIVE TREE TRACE")
print("="*70)
visual_dc_tree_trace(arr[:6], 0, len(arr[:6]) - 1)
print("="*70)
