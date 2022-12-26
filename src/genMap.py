import random

def generate_island_map(h, w, k):
  # number of regions is k+1
  grid = [[str(0) for _ in range(w)] for _ in range(h)]  # Initialize grid with all 0s (sea)
  processed_cells = set()  # Set of cells that have already been processed
  
  for i in range(k):
    # Choose a random cell to start from
    start_row = random.randint(1, h - 2)
    start_col = random.randint(1, w - 2)
    
    while grid[start_row][start_col] != '0': #(start_row, start_col) in processed_cells and 
        start_row = random.randint(1, h - 2)
        start_col = random.randint(1, w - 2)
    queue = [(start_row, start_col)]
    
    processed_cells.add((start_row, start_col))
    
    p = random.randint(int(w * h / (k + 1)), int(w * h / k))
    while queue:
        row, col = queue.pop(0)

        grid[row][col] = str(i + 1)
        
        for r, c in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
            if 1 <= r < h - 1 and 1 <= c < w - 1 and (r, c) not in processed_cells:
                if p:
                    processed_cells.add((r, c))
                    queue.append((r, c))
                    p -= 1       

  # random mountains
  for i in range(int(k*1.5)):
      row = random.randint(1, h - 2)
      col = random.randint(1, w - 2)
      while grid[row][col] == '0' or 'M' in grid[row][col]:
          row = random.randint(1, h - 2)
          col = random.randint(1, w - 2)
      grid[row][col] += 'M'

  # random prisons
  prisonLocations = []
  for i in range(2, k + 1):
      row = random.randint(1, h - 2)
      col = random.randint(1, w - 2)
      while "0" in grid[row][col] or "M" in grid[row][col] or "P" in grid[row][col]:
          row = random.randint(1, h - 2)
          col = random.randint(1, w - 2)

      prisonLocations.append([row, col])
      grid[row][col] += 'P'

  # assign treasure
  row = random.randint(1, h - 2)
  col = random.randint(1, w - 2)
  while "0" in grid[row][col] or "M" in grid[row][col] or "P" in grid[row][col]:
      row = random.randint(1, h - 2)
      col = random.randint(1, w - 2)
  treasureLocation = [row, col]

  # assign pirate
  pirateLocation = random.choice(prisonLocations)

  # assign agent
  row = random.randint(1, h - 2)
  col = random.randint(1, w - 2)
  while "0" in grid[row][col] or "M" in grid[row][col] or "P" in grid[row][col] or [row, col] == treasureLocation:
      row = random.randint(1, w - 2)
      col = random.randint(1, h - 2)
  agentLocation = [row, col]

  return grid, treasureLocation, agentLocation, pirateLocation

# Generate a map with 8 rows, 8 columns, and 5 regions
map,_,_,_ = generate_island_map(8, 8, 4)

# Print map
for row in map:
    print(row)