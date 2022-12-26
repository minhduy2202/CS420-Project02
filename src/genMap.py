import random

def generate_island_map(h, w, k):
  grid = [[0 for _ in range(w)] for _ in range(h)]  # Initialize grid with all 0s (sea)
  processed_cells = set()  # Set of cells that have already been processed
  
  for i in range(k):
    # Choose a random cell to start from
    start_row = random.randint(0, h - 1)
    start_col = random.randint(0, w - 1)
    
    while grid[start_row][start_col] != 0: #(start_row, start_col) in processed_cells and 
        start_row = random.randint(0, h - 1)
        start_col = random.randint(0, w - 1)
    queue = [(start_row, start_col)]
    
    processed_cells.add((start_row, start_col))
    
    p = random.randint(int(w * h / (k + 1)), int(w * h / k))
    while queue:
        row, col = queue.pop(0)

        grid[row][col] = i + 1
        
        for r, c in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
            if 0 <= r < h and 0 <= c < w and (r, c) not in processed_cells:
                if p:
                    processed_cells.add((r, c))
                    queue.append((r, c))
                    p -= 1       

  return grid

# Generate a map with 5 rows, 5 columns, and 3 regions
map = generate_island_map(8, 8, 4)

# Print map
for row in map:
  print(row)
