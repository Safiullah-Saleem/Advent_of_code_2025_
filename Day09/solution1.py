def main():
    
    points = []
    with open('input.txt', 'r') as f:
        for line in f:
            if line.strip():
                x, y = map(int, line.strip().split(','))
                points.append((x, y))
    
    n = len(points)
    print(f"Read {n} points")
    
    max_area = 0
    
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            
            if x1 == x2 and y1 == y2:
                continue
                
            width = abs(x1 - x2)
            height = abs(y1 - y2)
            area = (width + 1) * (height + 1)
            
            if area > max_area:
                max_area = area
    
    print(f"Largest rectangle area: {max_area}")

if __name__ == "__main__":
    main()