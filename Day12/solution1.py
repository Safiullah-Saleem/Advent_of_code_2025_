from collections import defaultdict
import sys
import time

def parse_input(text):
    """Parse shapes and regions from input text"""
    shapes = {}
    regions = []
    
    lines = text.strip().splitlines()
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
            
        if line.endswith(':'):
            try:
                shape_id = int(line[:-1])
                i += 1
                
                shape_lines = []
    
                while i < len(lines) and lines[i].strip() and 'x' not in lines[i]:
                    shape_lines.append(lines[i].rstrip())
                    i += 1
                
                if shape_lines:
                    shapes[shape_id] = shape_lines
                    
                if len(shapes) >= 6:
                    break
            except ValueError:
                i += 1
        else:
            i += 1
    
    for j in range(i, len(lines)):
        line = lines[j].strip()
        if not line:
            continue
            
        if 'x' in line and ':' in line:
            try:
                parts = line.split(':')
                dims = parts[0].split('x')
                w, h = int(dims[0]), int(dims[1])
                counts = list(map(int, parts[1].strip().split()))
                
                if len(counts) < 6:
                    counts = counts + [0] * (6 - len(counts))
                elif len(counts) > 6:
                    counts = counts[:6]
                    
                regions.append((w, h, counts))
            except (ValueError, IndexError):
                continue
    
    return shapes, regions

def shape_to_coords(shape_lines):
    """Convert shape to normalized coordinates"""
    coords = []
    for r, row in enumerate(shape_lines):
        for c, ch in enumerate(row):
            if ch == '#':
                coords.append((r, c))
    
    if not coords:
        return frozenset()
    
    min_r = min(r for r, _ in coords)
    min_c = min(c for _, c in coords)
    return frozenset(((r - min_r, c - min_c) for r, c in coords))

def rotate_coords(coords):
    """Rotate 90 degrees clockwise"""
    rotated = [(c, -r) for r, c in coords]
    min_r = min(r for r, _ in rotated)
    min_c = min(c for _, c in rotated)
    return frozenset(((r - min_r, c - min_c) for r, c in rotated))

def flip_coords(coords):
    """Flip horizontally"""
    flipped = [(r, -c) for r, c in coords]
    min_r = min(r for r, _ in flipped)
    min_c = min(c for _, c in flipped)
    return frozenset(((r - min_r, c - min_c) for r, c in flipped))

def all_orientations(shape_lines):
    """Generate all unique rotations and reflections"""
    base = shape_to_coords(shape_lines)
    if not base:
        return {base}
    
    orientations = set()
    current = base
    
    for _ in range(4):
        orientations.add(current)
        orientations.add(flip_coords(current))
        current = rotate_coords(current)
    
    return orientations

def placements_for_orientation(coords, region_w, region_h):
    """Generate placements for a specific orientation"""
    if not coords:
        return []
    max_r = max(r for r, _ in coords)
    max_c = max(c for _, c in coords)
    
    placements = []
    
    for top in range(region_h - max_r):
        for left in range(region_w - max_c):
            row_masks = defaultdict(int)
            for r, c in coords:
                rr = top + r
                cc = left + c
                row_masks[rr] |= (1 << cc)
            
            placements.append(tuple(sorted(row_masks.items())))
    
    return placements

def placements_for_shape(shape_lines, region_w, region_h):
    """Generate all unique placements for a shape"""
    orientations = all_orientations(shape_lines)
    seen = set()
    all_placements = []
    
    for coords in orientations:
        placements = placements_for_orientation(coords, region_w, region_h)
        for placement in placements:
            if placement not in seen:
                seen.add(placement)
                all_placements.append(placement)
    
    return all_placements

def can_place_all(region_w, region_h, shapes, counts):
    """Optimized solver with better memoization and pruning"""
    shape_cells = {}
    for sid, lines in shapes.items():
        shape_cells[sid] = len(shape_to_coords(lines))
    
    total_cells_needed = sum(counts[i] * shape_cells[i] for i in range(len(counts)))
    if total_cells_needed > region_w * region_h:
        return False
    
    piece_list = []
    for i, cnt in enumerate(counts):
        piece_list.extend([i] * cnt)
    
    if not piece_list:
        return True
    
    placements_per_shape = {}
    for sid in set(piece_list):
        placements = placements_for_shape(shapes[sid], region_w, region_h)
        if not placements and counts[sid] > 0:
            return False
        placements_per_shape[sid] = placements
    
    piece_list_sorted = []
    for i, cnt in enumerate(counts):
        for _ in range(cnt):
            piece_list_sorted.append(i)
    
    piece_list_sorted.sort(key=lambda sid: (
        len(placements_per_shape[sid]),
        -shape_cells[sid] 
    ))
    
    occupancy = [0] * region_h
    
    memo = {}
    
    def dfs(idx):
        if idx == len(piece_list_sorted):
            return True
        
        state = (idx, tuple(occupancy))
        if state in memo:
            return memo[state]
        
        sid = piece_list_sorted[idx]
        
        # Try placements
        for placement in placements_per_shape[sid]:
            # Quick conflict check
            conflict = False
            for row, mask in placement:
                if occupancy[row] & mask:
                    conflict = True
                    break
            
            if not conflict:
                for row, mask in placement:
                    occupancy[row] |= mask
                
                if dfs(idx + 1):
                    memo[state] = True
                    return True
                
                for row, mask in placement:
                    occupancy[row] ^= mask
        
        memo[state] = False
        return False
    
    return dfs(0)

def solve_region_parallel(args):
    """Helper for parallel processing"""
    w, h, counts, shapes = args
    return can_place_all(w, h, shapes, counts)

def main():
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    else:
        fname = "input.txt"
    
    print(f"Reading input from {fname}...")
    
    with open(fname, 'r') as f:
        text = f.read()
    
    print("Parsing input...")
    shapes, regions = parse_input(text)
    
    print(f"Found {len(shapes)} shapes and {len(regions)} regions")

    shapes_dict = {}
    for i in range(6):
        if i in shapes:
            shapes_dict[i] = shapes[i]
        else:
            print(f"Warning: Shape {i} not found")
            shapes_dict[i] = []
    
    # Solve
    print(f"\nSolving {len(regions)} regions...")
    start_time = time.time()
    
    fit_count = 0
    total_regions = len(regions)
    
    # Process in batches for better progress reporting
    batch_size = 50
    
    for batch_start in range(0, total_regions, batch_size):
        batch_end = min(batch_start + batch_size, total_regions)
        batch_time = time.time()
        
        for i in range(batch_start, batch_end):
            w, h, counts = regions[i]
            
            # Ensure counts has 6 elements
            if len(counts) < 6:
                counts = counts + [0] * (6 - len(counts))
            
            if can_place_all(w, h, shapes_dict, counts):
                fit_count += 1
        
        elapsed = time.time() - start_time
        print(f"  Processed {batch_end}/{total_regions} regions, {fit_count} fit so far ({elapsed:.1f}s)")
    
    total_time = time.time() - start_time
    print(f"\nDone! Total time: {total_time:.2f} seconds")
    print(f"Total regions: {total_regions}")
    print(f"Solvable regions: {fit_count}")
    
    return fit_count

if __name__ == "__main__":
    result = main()
    print(f"\nAnswer: {result}")