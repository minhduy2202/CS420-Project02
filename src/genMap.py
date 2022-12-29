import argparse
import random
import os
import math

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
        
        p = random.randint(int((w * h - 2 * (w + h)) / (k + 1)), int((w * h - 2 * (w + h)) / k))
        if p <= 3: p = 4
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
    for i in range(int(k*1.5) - 1):
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
    grid[row][col] += 'T'

    return grid, treasureLocation

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Treasure Island input file.')
    parser.add_argument('--save_dir', type=str, required=False, default='data/input/', help='Input stored directory.')
    parser.add_argument('--width', type=int, required=True, help='Please define the width of map.')
    parser.add_argument('--height', type=int, required=True, help='Please define the height of map.')
    parser.add_argument('--region', type=int, required=True, help='Please define the number of regions.')
    
    args = parser.parse_args()
    
    savedFolder = args.save_dir
    w, h, k = args.width, args.height, args.region - 1
    
    os.chdir('..')
    if not os.path.exists(savedFolder):
        print('Folder not found')
        exit()
    
    _map, treasure = generate_island_map(w, h, k)
    count = len([entry for entry in os.listdir(savedFolder) if os.path.isfile(os.path.join(savedFolder, entry))])
    
    reveal = int(math.log2(max(w, h)))
    free = 2 * int(math.log2(max(w, h)))
    
    with open(os.path.join(savedFolder, 'MAP_' + str(count + 1).zfill(2) + '.txt'), 'w') as f:
        f.writelines(f"{w} {h}\n")
        f.writelines(f"{reveal}\n")
        f.writelines(f"{free}\n")
        f.writelines(f"{k + 1}\n")
        f.writelines(f"{treasure[0]} {treasure[1]}\n")
        for r in _map:
            f.writelines("; ".join(r) + '\n')
