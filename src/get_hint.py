import random

def genHint(_w: int, _h: int, _numOfRegions: int, _treasureLocation: list, _map: list, _weights: list) -> tuple:
    """
    *args:
        @_w: Weight.
        @_h: Height.
        @_numOfRegions: Number of regions that the map has.
        @_treasureLocation: The location of treasure.
        @_map: The game map.
        @_weights: A list Of N (N is the number Of hints) weights to random hint.
    
    *return:
        First argument: Indicates the hint number.
        Second argument: The tiles/regions/area that hint involves.
        Third argument: The hint is a truth or not.
        Fourth argument: The string format of hint that will be printed out later.
    """
    numOfHints = 16
    
    hint = 11#random.choices(range(1, numOfHints + 1), weights = _weights, k = 1);
    
    if hint in [1, 2]: # "A list Of tiles ? that doesn't contain the treasure." and "A list Of tiles ? that contains the treasure."
        numOfTiles = random.randrange(int(_w * _h / 8) + 1)
        listOfTiles = random.sample(range(_w * _h), numOfTiles)
        
        isTruth = (hint == 1) ^ (_treasureLocation[0] * _treasureLocation[1] in listOfTiles)
        
        return (hint, listOfTiles, isTruth, f"A list of tiles {listOfTiles} " + ("does not contain the treasure." if hint == 1 else "contains the treasure."))
    elif hint == 3: # "? regions that 1 of them has the treasure."
        numOfRegions = random.randrange(2, min(_numOfRegions, 6))
        listOfRegions = random.sample(range(1, _numOfRegions), numOfRegions)
        
        isTruth = int(_map[_treasureLocation[0], _treasureLocation[1]][0]) in listOfRegions
        
        return (hint, listOfRegions, isTruth, f"One of region in {listOfRegions} has the treasure.")
    elif hint == 4: # "? regions that do not contain the treasure."
        numOfRegions = random.randrange(1, min(_numOfRegions, 4))
        listOfRegions = random.sample(range(1, _numOfRegions), numOfRegions)
        
        isTruth = int(_map[_treasureLocation[0], _treasureLocation[1]][0]) not in listOfRegions
        
        return (hint, listOfRegions, isTruth, f"All regions in {listOfRegions} do not have the treasure.")
    elif hint == 5: # "A rectangle area ? that has the treasure.",
        x1 = random.randrange(int(_w / 4)  + 1)
        y1 = random.randrange(int(_h / 4)  + 1)
        x2 = random.randrange(x1 + int(_w * 3 / 8), _w)
        y2 = random.randrange(y1 + int(_h * 3 / 8), _h)
        
        isTruth = (x1 <= _treasureLocation[0] and _treasureLocation[0] <= x2) and (y1 <= _treasureLocation[1] and _treasureLocation[1] <= y2)
        
        return (hint, [x1, y1, x2, y2], isTruth, f"There is treasure in the rectangle area {[x1, y1, x2, y2]}.")
    elif hint == 6: # "A rectangle area ? that doesn't have the treasure.",
        x1 = random.randrange(_w - 4)
        y1 = random.randrange(_h - 4)
        x2 = random.randrange(x1 + 1, x1 + 3)
        y2 = random.randrange(y1 + 1, y1 + 3)
        
        isTruth = ~((x1 <= _treasureLocation[0] and _treasureLocation[0] <= x2) and (y1 <= _treasureLocation[1] and _treasureLocation[1] <= y2))
        
        return (hint, [x1, y1, x2, y2], isTruth, f"There is no treasure in the rectangle area {[x1, y1, x2, y2]}.")
    elif hint == 7: # "The pirate tells that you are the nearest person to the treasure.",
        # cai hint nay dan qua, de tinh sau.
        pass
    elif hint == 8: # "A column and/or a row that contain the treasure." (rare),
        row, column = False, False
        
        while ~row and ~column:
            if random.random() < 0.5: row = True
            if random.random() < 0.5: column = True
        
        r, c = -1, -1
        if row: r = random.randrange(min(0, _treasureLocation[0] - 2), min(_w, _treasureLocation[0] + 3))
        if column: c = random.randrange(min(0, _treasureLocation[1] - 2), min(_h, _treasureLocation[1] + 3))
        
        isTruth = False
        
        if row and column: 
            s = f"Column {c} and row {r} contain the treasure."
            isTruth = (r == _treasureLocation[0]) and (c == _treasureLocation[1])
        elif row: 
            s = f"Row {r} contains the treasure."
            isTruth = (r == _treasureLocation[0])
        else: 
            s = f"Column {c} contains the treasure."
            isTruth = (c == _treasureLocation[1])
        
        return (hint, [r, c], isTruth, s)
    elif hint == 9: # "A column and/or a row that don't contain the treasure.",
        row, column = False, False
        
        while ~row and ~column:
            if random.random() < 0.5: row = True
            if random.random() < 0.5: column = True
        
        r, c = -1, -1
        if row: r = random.randrange(_w)
        if column: c = random.randrange(_h)
        
        isTruth = False
        
        if row and column: 
            s = f"Column {c} and row {r} do not contain the treasure."
            isTruth = (r != _treasureLocation[0]) or (c != _treasureLocation[1])
        elif row: 
            s = f"Row {r} does not contain the treasure."
            isTruth = (r != _treasureLocation[0])
        else: 
            s = f"Column {c} does not contain the treasure."
            isTruth = (c != _treasureLocation[1])
            
        return (hint, [r, c], isTruth, s)
    elif hint == 10: # "The treasure is somewhere in the boundary of 2 regions ?.",
        adjacent = [(-1, 0), (1, 0), (0, 1), (0, - 1)]
        regionPairs = dict()
        
        for i in range(_w):
            for j in range(_h):
                for tup in adjacent:
                    if i + tup[0] >= 0 and i + tup[0] < _w and j + tup[1] >= 0 and j + tup[1] < _h:
                        region_1 = int(_map[i][j][0])
                        region_2 = int(_map[i + tup[0]][j + tup[1]][0])
                        
                        if region_1 == 0 or region_2 == 0:
                            continue
                        
                        if region_1 != region_2:
                            if region_1 > region_2:
                                region_1, region_2 = region_2, region_1
                            if (region_1, region_2) not in regionPairs.keys():
                                regionPairs[(region_1, region_2)] = [(i, j)]
                            else:
                                regionPairs[(region_1, region_2)].append((i, j))
        
        regionPair, listOfTiles = random.choice(list(regionPairs.items()))
        
        isTruth = tuple(_treasureLocation) in listOfTiles
        
        return (hint, set(listOfTiles), isTruth, f"The treasure is somewhere in the boundary of 2 regions {regionPair}")
    elif hint == 11: # "The treasure is somewhere in a boundary of 2 regions.",
        adjacent = [(-1, 0), (1, 0), (0, 1), (0, - 1)]
        setOfTiles = set()
        
        for i in range(_w):
            for j in range(_h):
                for tup in adjacent:
                    if i + tup[0] >= 0 and i + tup[0] < _w and j + tup[1] >= 0 and j + tup[1] < _h:
                        region_1 = int(_map[i][j][0])
                        region_2 = int(_map[i + tup[0]][j + tup[1]][0])
                        
                        if region_1 == 0 or region_2 == 0:
                            continue
                        
                        if region_1 != region_2:
                            setOfTiles.add((i, j))
        
        isTruth = tuple(_treasureLocation) in setOfTiles
        
        for r in _map:
            print(r)
        
        return (hint, setOfTiles, isTruth, f"The treasure is somewhere in the boundary of 2 regions.")
    elif hint == 12: # "The treasure is somewhere in an area bounded by 1-3 tiles from sea"
        sizeOfBoundedArea = random.randrange(1, 4)
        bounded = []
        
        for i in range(1, sizeOfBoundedArea + 1):
            bounded.append((i, 0))
            bounded.append((-i, 0))
            bounded.append((0, i))
            bounded.append((0, -i))
        
        setOfTiles = set()
        
        for i in range(_w):
            for j in range(_h):
                if _map[i][j] == "0":
                    for tup in bounded:
                        if i + tup[0] >= 0 and i + tup[0] < _w and j + tup[1] >= 0 and j + tup[1] < _h:
                            setOfTiles.add((i + tup[0], j + tup[1]))
                            
        isTruth = tuple(_treasureLocation) in setOfTiles
        
        return (hint, setOfTiles, isTruth, f"The treasure is somewhere in an area bounded by {sizeOfBoundedArea} tiles from sea.")
    elif hint == 13: # A half of the map without treasure (rare)
        pass
    elif hint == 14: # (From the center Of the map)/(from the prison) that he's staying, he tells you a direction that has the treasure (W, E, N, S or SE, SW, NE, NW), the shape Of area when the hints are (W, E, N, S) is triangle
        pass
    elif hint == 15: # 2 squares that are different in size, the small one is placed inside the bigger one, the treasure is somewhere inside the gap between 2 squares. (rare)
        pass
    else: # The treasure is in a region that has mountain.
        pass

print(genHint(5, 5, 3, [3, 4], [['0', '0', '0', '0', '0'], ['0', '1', '1M', '1P', '1'], ['0', '1P', '2M', '2', '2'], ['0', '3', '3M', '3', '3'], ['0', '0', '0', '0', '0']], []))