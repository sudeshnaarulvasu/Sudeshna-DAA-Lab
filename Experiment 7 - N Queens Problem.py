def is_safe(board, row, col):
    for prev_row in range(row):
        placed = board[prev_row]
        if placed == col:  # Same column
            return False
        if abs(prev_row - row) == abs(placed - col):  # Diagonal
            return False
    return True

def solve_n_queens(n):
    board = [-1] * n
    solutions = []
    backtrack_count = [0]

    def backtrack(row):
        if row == n:
            solutions.append(board[:])
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1  # Undo
                backtrack_count[0] += 1

    backtrack(0)
    return solutions, backtrack_count[0]

def display_board(solution, n):
    print('  +' + '---+' * n)
    for row in range(n):
        print('  |', end='')
        for col in range(n):
            if solution[row] == col:
                print(' Q |', end='')
            else:
                print(' . |', end='')
        print()
        print('  +' + '---+' * n)

# --- Solve for N=4 (show all) and N=8 (count only) ---
for n in [4, 6, 8]:
    solutions, backtracks = solve_n_queens(n)
    print(f'N={n}: {len(solutions)} solutions, {backtracks} backtracks')
    if n == 4:
        print(f'\n  All solutions for {n}-Queens:')
        for i, sol in enumerate(solutions, 1):
            print(f'\n  Solution {i}: {sol}')
            display_board(sol, n)

# =====================================================================
# ADDITION: STANDARD ASCII VISUALIZATION (NO SPECIAL SYMBOLS)
# =====================================================================

def visualize_summary_plain(n_values):
    print("\n" + "=" * 55)
    print(" N-QUEENS COMPUTATIONAL SUMMARY VISUALIZATION ".center(55, "="))
    print("=" * 55)

    print("\n[Solutions Count per N]")
    for n in n_values:
        sols, _ = solve_n_queens(n)
        count = len(sols)
        bar = "#" * min(count, 40)
        print(f"  N={n:<2} | {bar:<40} ({count} solutions)")

    print("\n[Backtrack Attempts per N]")
    for n in n_values:
        _, backtracks = solve_n_queens(n)
        # Scale backtracks visually for clear display
        scaled_len = min(backtracks // 20 + 1 if backtracks > 0 else 0, 40)
        bar = "=" * scaled_len
        print(f"  N={n:<2} | {bar:<40} ({backtracks} backtracks)")

    print("=" * 55)


# Run summary visualization
visualize_summary_plain([4, 6, 8])
