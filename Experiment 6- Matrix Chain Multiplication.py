def matrix_chain_order(dims):
    """
    Matrix Chain Multiplication using DP
    dims: list of dimensions, matrix i has dims[i-1] x dims[i]
    Time: O(n^3), Space: O(n^2)
    """
    n = len(dims) - 1
    # m[i][j] = minimum multiplications for matrices i..j
    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]

    # l is the chain length
    for l in range(2, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1
            m[i][j] = float('inf')
            for k in range(i, j):
                cost = m[i][k] + m[k+1][j] + dims[i-1] * dims[k] * dims[j]
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k
    return m, s

def print_optimal_parens(s, i, j):
    if i == j:
        return f'A{i}'
    k = s[i][j]
    left = print_optimal_parens(s, i, k)
    right = print_optimal_parens(s, k + 1, j)
    return f'({left} x {right})'

def print_dp_table(m, n):
    print('\nDP Cost Table m[i][j]:')
    print(f'{"":>6}', end='')
    for j in range(1, n + 1):
        print(f'A{j:>8}', end='')  # Fixed string formatting typo
    print()
    for i in range(1, n + 1):
        print(f'A{i:<5}', end='')
        for j in range(1, n + 1):
            if j < i: print(f'{"---":>9}', end='')
            else: print(f'{m[i][j]:>9}', end='')
        print()

# A1(10x30), A2(30x5), A3(5x60), A4(60x10)
dims = [10, 30, 5, 60, 10]
n    = len(dims) - 1
print(f'Matrix Dimensions:')
for i in range(n):
    print(f'  A{i+1}: {dims[i]} x {dims[i+1]}')

m, s = matrix_chain_order(dims)
print(f'\nMinimum scalar multiplications: {m[1][n]}')
print(f'Optimal parenthesization: {print_optimal_parens(s, 1, n)}')

# REMOVED: print_dp_table(m, n) has been commented out to prevent printing the old table
# print_dp_table(m, n)

# =====================================================================
# ADDITION: PURE PYTHON VISUALIZATION (NO IMPORTS REQUIRED)
# =====================================================================

def render_tree_ascii(s, i, j):
    """
    Recursively builds an ASCII binary tree representation 
    of the optimal matrix multiplication split.
    """
    if i == j:
        return [f"[A{i}]"]

    k = s[i][j]
    left_lines = render_tree_ascii(s, i, k)
    right_lines = render_tree_ascii(s, k + 1, j)

    root_label = f"(A{i}..A{j} | k={k})"
    
    # Calculate widths for centering layout
    w_left = max(len(line) for line in left_lines)
    w_right = max(len(line) for line in right_lines)

    # Pad lines to equal width per side
    left_padded = [line.ljust(w_left) for line in left_lines]
    right_padded = [line.ljust(w_right) for line in right_lines]

    # Combine tree levels
    combined = []
    max_depth = max(len(left_padded), len(right_padded))

    # Add branch connections
    branch = "/" + " " * (w_left + 1) + "\\"
    combined.append(branch.center(w_left + w_right + 3))

    for depth in range(max_depth):
        l_str = left_padded[depth] if depth < len(left_padded) else " " * w_left
        r_str = right_padded[depth] if depth < len(right_padded) else " " * w_right
        combined.append(f"{l_str}   {r_str}")

    return [root_label.center(w_left + w_right + 3)] + combined


def visualize_mcm(s, m, n):
    """Prints the ASCII Tree and Cost Grid directly in terminal."""
    print("\n" + "=" * 50)
    print(" 1. OPTIMAL MULTIPLICATION TREE ".center(50, "="))
    print("=" * 50 + "\n")

    tree_lines = render_tree_ascii(s, 1, n)
    for line in tree_lines:
        print(line)

    print("\n" + "=" * 50)
    print(" 2. DP COST MATRIX GRID (m[i][j]) ".center(50, "="))
    print("=" * 50 + "\n")

    # Header
    header = "       " + "".join([f"  A{j}   " for j in range(1, n + 1)])
    divider = "     +" + "-------+" * n
    
    print(header)
    print(divider)

    for i in range(1, n + 1):
        row_str = f"  A{i} |"
        for j in range(1, n + 1):
            if j < i:
                row_str += "  ---  |"
            else:
                row_str += f" {m[i][j]:>5} |"
        print(row_str)
        print(divider)


# Run the visualization
visualize_mcm(s, m, n)
