import re
import itertools
import sys
from typing import List, Tuple

BRACKET_RE = re.compile(r"\[([^\]]*)\]")
PAREN_RE = re.compile(r"\(([^)]*)\)")

def parse_line(line: str) -> Tuple[str, List[List[int]]]:
    # First, let's print what we're parsing
    print(f"Parsing line: {line[:100]}...")
    
    b = BRACKET_RE.search(line)
    if not b:
        raise ValueError("No indicator pattern found in line: " + line)
    pattern = b.group(1).strip()
    print(f"Found pattern: '{pattern}'")

    # Remove everything after { if it exists
    line_before_brace = line.split('{')[0] if '{' in line else line
    
    buttons = []
    for g in PAREN_RE.findall(line_before_brace):
        s = g.strip()
        if s == "":
            buttons.append([])
            continue

        parts = [p.strip() for p in s.split(",") if p.strip() != ""]
        nums = [int(x) for x in parts]
        buttons.append(nums)
    
    print(f"Found {len(buttons)} button groups")
    return pattern, buttons

def gauss_rref(rows: List[int], rhs: List[int], n_vars: int):

    m = len(rows)
    r = 0
    pivot_row_to_col = {}
    pivot_cols_set = set()

    for col in range(n_vars):

        sel = None
        for i in range(r, m):
            if (rows[i] >> col) & 1:
                sel = i
                break
        if sel is None:
            continue

        if sel != r:
            rows[r], rows[sel] = rows[sel], rows[r]
            rhs[r], rhs[sel] = rhs[sel], rhs[r]

        for i in range(m):
            if i != r and ((rows[i] >> col) & 1):
                rows[i] ^= rows[r]
                rhs[i] ^= rhs[r]
        pivot_row_to_col[r] = col
        pivot_cols_set.add(col)
        r += 1
        if r == m:
            break

    return rows, rhs, pivot_row_to_col, pivot_cols_set

def solve_min_weight(rows_masks: List[int], rhs_bits: List[int], n_vars: int) -> int:
    
    rows = rows_masks[:]
    rhs = rhs_bits[:]   
    m = len(rows)

    rows, rhs, pivot_row_to_col, pivot_cols_set = gauss_rref(rows, rhs, n_vars)

    for i in range(m):
        if rows[i] == 0 and rhs[i] == 1:

            return 10**12

    x0 = 0

    for r, c in pivot_row_to_col.items():
        if rhs[r] & 1:
            x0 |= (1 << c)


    pivot_col_for_row = {c: r for r, c in pivot_row_to_col.items()}
    free_cols = [c for c in range(n_vars) if c not in pivot_cols_set]
    basis = [] 
    for f in free_cols:
        vec = 0

        vec |= (1 << f)

        r = pivot_col_for_row.get(f, None) 

        for prow, pcol in pivot_row_to_col.items():

            if ((rows[prow] >> f) & 1):
                vec |= (1 << pcol)
        basis.append(vec)


    if not basis:
        return x0.bit_count()


    k = len(basis)
    best = x0.bit_count()


    if best == 0:
        return 0

    basis_ints = basis

    if k <= 22:

        total = 1 << k
        for mask in range(total):
            comb = 0
            
            mm = mask
            idx = 0
            while mm:
                if mm & 1:
                    comb ^= basis_ints[idx]
                idx += 1
                mm >>= 1
            x = x0 ^ comb
            wc = x.bit_count()
            if wc < best:
                best = wc
                if best == 0:
                    return 0
        return best
    
    for w in range(1, k + 1):

        if w >= best:
            break
        for combo in itertools.combinations(range(k), w):
            comb = 0
            for idx in combo:
                comb ^= basis_ints[idx]
            x = x0 ^ comb
            wc = x.bit_count()
            if wc < best:
                best = wc
                if best == 0:
                    return 0

    return best

def solve_file(filename: str) -> None:
    machines_min = []
    with open(filename, "r", encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f if ln.strip() != ""]

    for idx, line in enumerate(lines):
        try:
            pattern, buttons = parse_line(line)
        except Exception as e:
            print(f"Error parsing line {idx+1}: {e}", file=sys.stderr)
            continue

        m = len(pattern)

        b_bits = [(1 if pattern[i] == "#" else 0) for i in range(m)]

        n = len(buttons)

        rows_masks = []
        for i in range(m):
            mask = 0
            for j, btn in enumerate(buttons):

                if i in btn:
                    mask |= (1 << j)
            rows_masks.append(mask)

        min_presses = solve_min_weight(rows_masks, b_bits, n)
        machines_min.append(min_presses)
        print(f"Machine {idx+1}: min presses = {min_presses}")

    total = sum(machines_min)
    print("\nTotal minimal presses across all machines:", total)

if __name__ == "__main__":
    FILE = "input.txt"
    try:
        solve_file(FILE)
    except FileNotFoundError:
        print(f"Input file '{FILE}' not found. Please create the file in the same directory and try again.")