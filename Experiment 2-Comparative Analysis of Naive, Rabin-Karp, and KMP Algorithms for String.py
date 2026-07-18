import time
import random
import string
def naive_search(text, pattern):
     n, m = len(text), len(pattern)
     matches, comparisons = [], 0
     for i in range(n - m + 1):
          j = 0
          while j < m:
               comparisons += 1
               if text[i + j] != pattern[j]:
                    break
               j += 1
          if j == m:
               matches.append(i)
     return matches, comparisons
def compute_lps(pattern):
     m = len(pattern)
     lps = [0] * m
     length, i = 0, 1
     while i < m:
          if pattern[i] == pattern[length]:
               length += 1
               lps[i] = length
               i += 1
          elif length != 0:
               length = lps[length - 1]
          else:
               lps[i] = 0
               i += 1
     return lps
def kmp_search(text, pattern):
     n, m = len(text), len(pattern)
     lps = compute_lps(pattern)
     matches, comparisons = [], 0
     i = j = 0
     while i < n:
          comparisons += 1
          if pattern[j] == text[i]:
               i += 1; j += 1
          if j == m:
               matches.append(i - j)
               j = lps[j - 1]
          elif i < n and pattern[j] != text[i]:
               if j != 0:
                    j = lps[j - 1]
               else:
                    i += 1
     return matches, comparisons
def rabin_karp(text, pattern, q=101):
     n, m = len(text), len(pattern)
     d = 256
     h = pow(d, m - 1, q)
     p_hash = t_hash = 0
     matches, comparisons = [], 0
     for i in range(m):
          p_hash = (d * p_hash + ord(pattern[i])) % q
          t_hash = (d * t_hash + ord(text[i])) % q
     for s in range(n - m + 1):
          if p_hash == t_hash:
               for k in range(m):
                    comparisons += 1
                    if text[s + k] != pattern[k]:
                         break
                    else:
                         matches.append(s)
          if s < n - m:
               t_hash = (d * (t_hash - ord(text[s]) * h) + ord(text[s + m])) % q
               if t_hash < 0:
                    t_hash += q
     return matches, comparisons
# --- Main Execution ---
text = 'AABAACAADAABAABA'
pattern = 'AABA'
print(f'Text: {text}')
print(f'Pattern: {pattern}')

m1, c1 = naive_search(text, pattern)
m2, c2 = kmp_search(text, pattern)
m3, c3 = rabin_karp(text, pattern)

print(f'\nNaive -> Matches at: {m1}, Comparisons: {c1}')
print(f'KMP -> Matches at: {m2}, Comparisons: {c2}')
print(f'RK -> Matches at: {m3}, Comparisons: {c3}')
# Performance comparison

text_large = ''.join(random.choices('ABCD', k=10000))
patterns = ['AB', 'ABCD', 'ABCDAB', 'ABCDABCD']
print(f'\n{"Pattern":>12} {"Naive":>10} {"KMP":>10} {"RK":>10}')
print('-' * 50)

for p in patterns:
     _, c1 = naive_search(text_large, p)
     _, c2 = kmp_search(text_large, p)
     _, c3 = rabin_karp(text_large, p)
     print(f'{p:>12} {c1:>10} {c2:>10} {c3:>10}')

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


# --- Step-by-Step Alignment Visualiser ---

def visual_trace_search(text, pattern):
    """
    Prints a step-by-step visual trace showing how each algorithm shifts 
    the pattern across the text.
    """
    print("\n" + "="*60)
    print(f" ALGORITHM STEP-BY-STEP TRACE".center(60))
    print(f"Text: '{text}' | Pattern: '{pattern}'")
    print("="*60)

    # 1. Naive Step Visualisation
    print("\n[ 1. NAIVE SEARCH TRACE ]")
    n, m = len(text), len(pattern)
    for i in range(n - m + 1):
        match_marker = "Match" if text[i:i+m] == pattern else "Mismatch"
        print(f"Step {i+1:02d} ({match_marker}): {text}")
        print(f"          {' ' * i}{pattern}")

    # 2. KMP Shift Visualisation
    print("\n[ 2. KMP SEARCH TRACE ]")
    lps = compute_lps(pattern) 
    i = j = 0
    step = 1
    while i < n:
        start_pos = i - j
        print(f"Step {step:02d}: {text}")
        
        if j < m:
            pat_display = pattern[:j] + pattern[j].upper() + pattern[j+1:]
        else:
            pat_display = pattern
            
        print(f"         {' ' * start_pos}{pat_display}")
        step += 1
        
        if pattern[j] == text[i]:
            i += 1; j += 1
        if j == m:
            print(f"         {' ' * start_pos}{'^' * m} MATCH FOUND!")
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    # 3. Rabin-Karp Hash Match Visualisation
    print("\n[ 3. RABIN-KARP HASH WINDOWS ]")
    print(f"Text: {text}")
    for s in range(n - m + 1):
        window = text[s:s+m]
        print(f"Window {s+1:02d}: {' ' * s}[{window}]{' ' * (n - s - m)} -> Checking hash alignment")

    print("="*60)

visual_trace_search(text, pattern)
