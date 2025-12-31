import argparse
import os
import sys

# Add repo root to path for profiler import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from profiler import profile


def get_args():
    """Argparse"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", action="store_true", help="Use real input for submission")
    return parser.parse_args()


def read(args):
    """Parse input - returns file content as string"""
    filepath = "input.txt" if args.submission else "example_input.txt"
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read().strip()


def printr(*results):
    """Print results"""
    print(f"-----{os.path.dirname(__file__).split(os.sep)[-1]}-----")
    for idx, result in enumerate(results):
        print(f"Part {idx+1}: {result}")
    print("-" * 20)

# ----------------------------------- #
# ----------- Custom Code ----------- #
# ----------------------------------- #
import re
from itertools import product
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


def parse_machine(line):
    """Parse a machine line into target state, buttons, and joltage requirements."""
    # Extract indicator lights [.##.]
    lights_match = re.search(r'\[([.#]+)\]', line)
    target = [1 if c == '#' else 0 for c in lights_match.group(1)]
    
    # Extract button schematics (0,1,2) or (3)
    buttons = []
    for match in re.finditer(r'\(([^)]+)\)', line):
        content = match.group(1)
        # Handle single numbers and comma-separated
        indices = [int(x.strip()) for x in content.split(',')]
        buttons.append(indices)
    
    # Extract joltage requirements {3,5,4,7}
    joltage_match = re.search(r'\{([^}]+)\}', line)
    joltage = [int(x.strip()) for x in joltage_match.group(1).split(',')]
    
    return target, buttons, joltage


def solve_part1(target, buttons):
    """Find minimum button presses to reach target state using GF(2) linear algebra."""
    n_lights = len(target)
    n_buttons = len(buttons)
    
    if n_buttons == 0:
        return 0 if all(t == 0 for t in target) else float('inf')
    
    # Build augmented matrix [A | b] where A[i][j] = 1 if button j affects light i
    # Rows = lights, Cols = buttons + 1 (for target)
    matrix = []
    for i in range(n_lights):
        row = [0] * (n_buttons + 1)
        for j, btn in enumerate(buttons):
            if i in btn:
                row[j] = 1
        row[n_buttons] = target[i]  # Augmented column
        matrix.append(row)
    
    # Gaussian elimination over GF(2)
    pivot_cols = []  # Track which columns have pivots
    pivot_row = 0
    
    for col in range(n_buttons):
        # Find pivot in this column
        found = False
        for row in range(pivot_row, n_lights):
            if matrix[row][col] == 1:
                # Swap rows
                matrix[pivot_row], matrix[row] = matrix[row], matrix[pivot_row]
                found = True
                break
        
        if not found:
            continue  # Free variable
        
        pivot_cols.append(col)
        
        # Eliminate all other 1s in this column
        for row in range(n_lights):
            if row != pivot_row and matrix[row][col] == 1:
                for c in range(n_buttons + 1):
                    matrix[row][c] ^= matrix[pivot_row][c]
        
        pivot_row += 1
    
    # Check for inconsistency (row of zeros with 1 in augmented column)
    for row in range(pivot_row, n_lights):
        if matrix[row][n_buttons] == 1:
            return float('inf')  # No solution
    
    # Find free variables (columns without pivots)
    free_vars = [c for c in range(n_buttons) if c not in pivot_cols]
    
    # Try all combinations of free variables to find minimum weight solution
    min_presses = float('inf')
    
    for free_vals in product([0, 1], repeat=len(free_vars)):
        # Build solution
        solution = [0] * n_buttons
        
        # Set free variables
        for i, col in enumerate(free_vars):
            solution[col] = free_vals[i]
        
        # Back-substitute to find pivot variables
        valid = True
        for i in range(len(pivot_cols) - 1, -1, -1):
            pivot_col = pivot_cols[i]
            # solution[pivot_col] = matrix[i][n_buttons] XOR sum of (matrix[i][j] * solution[j]) for j != pivot_col
            val = matrix[i][n_buttons]
            for j in range(n_buttons):
                if j != pivot_col:
                    val ^= matrix[i][j] * solution[j]
            solution[pivot_col] = val
        
        presses = sum(solution)
        min_presses = min(min_presses, presses)
    
    return min_presses


def solve_part2(buttons, joltage):
    """Find minimum button presses to reach joltage targets using ILP."""
    n_counters = len(joltage)
    n_buttons = len(buttons)
    
    if n_buttons == 0:
        return 0 if all(j == 0 for j in joltage) else float('inf')
    
    # Build matrix A where A[i][j] = 1 if button j affects counter i
    A = np.zeros((n_counters, n_buttons))
    for j, btn in enumerate(buttons):
        for i in btn:
            if i < n_counters:
                A[i][j] = 1
    
    # Objective: minimize sum of button presses (all coefficients = 1)
    c = np.ones(n_buttons)
    
    # Constraints: A @ x == joltage (equality constraints)
    constraints = LinearConstraint(A, joltage, joltage)
    
    # Bounds: x >= 0, no upper bound
    bounds = Bounds(lb=0, ub=np.inf)
    
    # All variables must be integers
    integrality = np.ones(n_buttons)  # 1 = integer constraint
    
    result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)
    
    if result.success:
        return int(round(result.fun))
    else:
        return float('inf')


def solve(data):
    """Solve both parts."""
    lines = data.strip().split('\n')
    
    total_presses_p1 = 0
    total_presses_p2 = 0
    
    for line in lines:
        if not line.strip():
            continue
        target, buttons, joltage = parse_machine(line)
        
        # Part 1: indicator lights (GF(2) linear algebra)
        presses1 = solve_part1(target, buttons)
        total_presses_p1 += presses1
        
        # Part 2: joltage counters (ILP)
        presses2 = solve_part2(buttons, joltage)
        total_presses_p2 += presses2
    
    return total_presses_p1, total_presses_p2

if __name__ == "__main__":
    opt = get_args()
    data = read(opt)

    with profile(opt.submission) as results:
        result1, result2 = solve(data)
        
        # Store results
        results["part1"] = result1
        results["part2"] = result2

    printr(result1, result2)
