import random

def genHint(_h: int, _w: int, _numOfRegions: int, _treasureLocation: int, _pirateLocation: int, _agentLocation: int, _map: list, _weights: list) -> tuple:
    """
    *args:
        @_h: Height.
        @_w: Width.
        @_numOfRegions: Number of regions that the map has.
        @_treasureLocation: The location of treasure.
        @_pirateLocation: The location of pirate.
        @_agentLocation: The location of agent.
        @_map: The game map.
        @_weights: A list Of N (N is the number Of hints) weights to random hint.
    
    *return:
        First argument: Indicates the hint number.
        Second argument: The tiles/regions/area that hint involves.
        Third argument: The hint is a truth or not.
        Fourth argument: The string format of hint that will be printed out later.
    """
    numOfHints = 16
    
    hint = random.choices(range(1, numOfHints + 1), weights = _weights, k = 1);
    hint = hint[0]
    
    if hint in [1, 2]: # "A list Of tiles ? that doesn't contain the treasure." and "A list Of tiles ? that contains the treasure."
        numOfTiles = random.randrange(2, int(_w * _h / 8) + 1)
        listOfTiles = random.sample(range(_w * _h), numOfTiles)
        
        isTruth = (hint == 1) ^ (_treasureLocation in listOfTiles)
        
        return (hint, listOfTiles, isTruth, f"A list of tiles {listOfTiles} " + ("does not contain the treasure." if hint == 1 else "contains the treasure."))
    elif hint == 3: # "? regions that 1 of them has the treasure."
        numOfRegions = random.randrange(2, min(_numOfRegions, 6))
        listOfRegions = random.sample(range(1, _numOfRegions), numOfRegions)
        
        listOfTiles = []
        
        for i in range(_h):
            for j in range(_w):
                if int(_map[i][j][0]) in listOfRegions: listOfTiles.append(i * _w + j)
        
        isTruth = _treasureLocation in listOfTiles
        
        return (hint, listOfTiles, isTruth, f"One of region in {listOfRegions} has the treasure.")
    elif hint == 4: # "? regions that do not contain the treasure."
        numOfRegions = random.randrange(1, min(_numOfRegions, 4))
        listOfRegions = random.sample(range(1, _numOfRegions), numOfRegions)
        
        listOfTiles = []
        
        for i in range(_h):
            for j in range(_w):
                if int(_map[i][j][0]) in listOfRegions: listOfTiles.append(i * _w + j)
        
        isTruth = _treasureLocation not in listOfTiles
        
        return (hint, listOfTiles, isTruth, f"All regions in {listOfRegions} do not have the treasure.")
    elif hint == 5: # "A rectangle area ? that has the treasure.",
        x1 = random.randrange(int(_h / 4)  + 1)
        y1 = random.randrange(int(_w / 4)  + 1)
        x2 = random.randrange(x1 + int(_h * 3 / 8), _h)
        y2 = random.randrange(y1 + int(_w * 3 / 8), _w)
        
        isTruth = (x1 <= _treasureLocation // _w and _treasureLocation // _w <= x2) and (y1 <= _treasureLocation % _w and _treasureLocation % _w <= y2)
        listOfTiles = []
        
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                listOfTiles.append(i * _w + j)
        
        return (hint, listOfTiles, isTruth, f"There is treasure in the rectangle area {[x1, y1, x2, y2]}.")
    elif hint == 6: # "A rectangle area ? that doesn't have the treasure.",
        x1 = random.randrange(_h - 4)
        y1 = random.randrange(_w - 4)
        x2 = random.randrange(x1 + 1, x1 + 3)
        y2 = random.randrange(y1 + 1, y1 + 3)
        
        isTruth = ~((x1 <= _treasureLocation // _w and _treasureLocation // _w <= x2) and (y1 <= _treasureLocation % _w and _treasureLocation % _w <= y2))
        
        listOfTiles = []
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                listOfTiles.append(i * _w + j)
        
        return (hint, listOfTiles, isTruth, f"There is no treasure in the rectangle area {[x1, y1, x2, y2]}.")
    elif hint == 7: # "The pirate tells that you are the nearest person to the treasure.",
        listOfTiles = []
        
        isTruth = (abs(_treasureLocation // _w - _agentLocation // _w) + abs(_treasureLocation % _w - _agentLocation % _w)) < (abs(_treasureLocation // _w - _pirateLocation // _w) + abs(_treasureLocation % _w - _pirateLocation % _w))
        
        for i in range(_h):
            for j in range(_w):
                if (abs(i - _agentLocation // _w) + abs(j - _agentLocation % _w)) < (abs(i - _pirateLocation // _w) + abs(j - _pirateLocation % _w)):
                    listOfTiles.append(i * _w + j)
                    
        return (hint, listOfTiles, isTruth, "The pirate tells that you are the nearest person to the treasure.")
    elif hint == 8: # "A column and/or a row that contain the treasure." (rare),
        row, column = False, False
        
        while not row and not column:
            if random.random() < 0.5: row = True
            if random.random() < 0.5: column = True
        
        r, c = -1, -1
        if row: r = random.randrange(min(0, _treasureLocation // _w - 2), min(_h, _treasureLocation // _w + 3))
        if column: c = random.randrange(min(0, _treasureLocation % _w - 2), min(_w, _treasureLocation % _w + 3))
        
        isTruth = False
        
        listOfTiles = []
        
        if row and column: 
            s = f"Column {c} and row {r} contain the treasure."
            isTruth = (r == _treasureLocation // _w) and (c == _treasureLocation % _w)
            
            listOfTiles.append(r * _w + c)
        elif row: 
            s = f"Row {r} contains the treasure."
            isTruth = (r == _treasureLocation // _w)
            
            for j in range(_w): listOfTiles.append(r  * _w + j)
        else: 
            s = f"Column {c} contains the treasure."
            isTruth = (c == _treasureLocation % _w)
            
            for i in range(_h): listOfTiles.append(i * _w + c)
        
        return (hint, listOfTiles, isTruth, s)
    elif hint == 9: # "A column and/or a row that don't contain the treasure.",
        row, column = False, False
        
        while not row and not column:
            if random.random() < 0.5: row = True
            if random.random() < 0.5: column = True
        
        r, c = -1, -1
        if row: r = random.randrange(_h)
        if column: c = random.randrange(_w)
        
        isTruth = False
        
        listOfTiles = []
        
        if row and column: 
            s = f"Column {c} and row {r} do not contain the treasure."
            isTruth = (r != _treasureLocation // _w) or (c != _treasureLocation % _w)
            listOfTiles.append(r * _w + c)
        elif row: 
            s = f"Row {r} does not contain the treasure."
            isTruth = (r != _treasureLocation // _w)
            
            for j in range(_w): listOfTiles.append(r  * _w + j)
        else: 
            s = f"Column {c} does not contain the treasure."
            isTruth = (c != _treasureLocation % _w)
            
            for i in range(_h): listOfTiles.append(i * _w + c)
            
        return (hint, listOfTiles, isTruth, s)
    elif hint == 10: # "The treasure is somewhere in the boundary of 2 regions ?.",
        adjacent = [(-1, 0), (1, 0), (0, 1), (0, - 1)]
        regionPairs = dict()
        
        for i in range(_h):
            for j in range(_w):
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
                                regionPairs[(region_1, region_2)] = [j+ i * _w ]
                            else:
                                regionPairs[(region_1, region_2)].append(j + i * _w)
        
        regionPair, listOfTiles = random.choice(list(regionPairs.items()))
        
        isTruth = (_treasureLocation) in listOfTiles
        
        return (hint, set(listOfTiles), isTruth, f"The treasure is somewhere in the boundary of 2 regions {regionPair}")
    elif hint == 11: # "The treasure is somewhere in a boundary of 2 regions.",
        adjacent = [(-1, 0), (1, 0), (0, 1), (0, - 1)]
        setOfTiles = set()
        
        for i in range(_h):
            for j in range(_w):
                for tup in adjacent:
                    if i + tup[0] >= 0 and i + tup[0] < _w and j + tup[1] >= 0 and j + tup[1] < _h:
                        region_1 = int(_map[i][j][0])
                        region_2 = int(_map[i + tup[0]][j + tup[1]][0])
                        
                        if region_1 == 0 or region_2 == 0:
                            continue
                        
                        if region_1 != region_2:
                            setOfTiles.add(j + i * _w)
        
        isTruth = (_treasureLocation) in setOfTiles
        
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
        
        for i in range(_h):
            for j in range(_w):
                if _map[i][j] == "0":
                    for tup in bounded:
                        if i + tup[0] >= 0 and i + tup[0] < _w and j + tup[1] >= 0 and j + tup[1] < _h:
                            setOfTiles.add((i + tup[0]) * _w + (j + tup[1]))
                            
        isTruth = (_treasureLocation) in setOfTiles
        
        return (hint, setOfTiles, isTruth, f"The treasure is somewhere in an area bounded by {sizeOfBoundedArea} tiles from sea.")
    elif hint == 13: # A half of the map without treasure (rare)
        direction = random.randrange(4)
        
        xl, yl, xr, yr = 0, 0, _w - 1, _h - 1
        d = ["down", "up", "left", "right"]

        if direction == 0: xl = int(_w / 2) # South
        if direction == 1: xr = int(_w / 2) # North
        if direction == 2: yr = int(_h / 2) # West
        if direction == 3: yl = int(_h / 2) # East
        
        isTruth = ~(xl <= _treasureLocation // _w and _treasureLocation // _w <= xr and yl <= _treasureLocation % _w and _treasureLocation % _w <= yr)
        
        listOfTiles = []
        for i in range(xl, xr + 1):
            for j in range(yl, yr + 1):
                listOfTiles.append(i * _w + j)
        
        return (hint, listOfTiles, isTruth, f"Half {d[direction]} side of the map does not have the treasure.")
    elif hint == 14: # (From the center of the map)/(from the prison that he's staying), he tells you a direction that has the treasure (W, E, N, S or SE, SW, NE, NW), the shape Of area when the hints are (W, E, N, S) is triangle
        choice = random.randrange(2)
        
        x, y = 0, 0
        if choice == 0:
            x, y = int(_w / 2), int(_h / 2)                
        else:
            x, y = _pirateLocation // _w, _pirateLocation %_w
            
        setOfTiles = set()     
        
        direction = random.randrange(8)
        d = ['E', 'W', 'N', 'S', 'SE', 'SW', 'NE', 'NW']
        
        if direction in [0, 1]: # East and West
            l, r = x, x
            while (direction == 0 and y < _h) or (direction == 1 and y >= 0):
                for i in range(max(l, 0), min(r, _w)):
                    setOfTiles.add(y + i * _w)
                l -= 1
                r += 1
                y += (-1 if direction == 1 else 1)
        if direction in [2, 3]: # South and North
            l, r = y, y
            while (direction == 2 and x < _w) or (direction == 3 and x >= 0):
                for i in range(max(l, 0), min(r, _h)):
                    setOfTiles.add(i + x * _w)
                l -= 1
                r += 1
                x += (-1 if direction == 3 else 1)
        if direction in [4, 5, 6, 7]:
            xl, yl, xr, yr = 0, 0, _w - 1, _h - 1
        
            if direction == 4: # SE
                xl, yl = x, y
            if direction == 5: # SW
                xl, yr = x, y
            if direction == 6: # NE
                xr, yl = x, y
            if direction == 7: # NW
                xr, yr = x, y
            
            for i in range(xl, xr + 1):
                for j in range(yl, yr + 1):
                    setOfTiles.add(j + i * _w)
                
        isTruth = (_treasureLocation) in setOfTiles
            
        return (hint, setOfTiles, isTruth, ("From center of the map" if choice == 0 else "From the prison that the pirate's staying") + f", he tells you that direction {d[direction]} has the treasure.")
    elif hint == 15: # 2 squares that are different in size, the small one is placed inside the bigger one, the treasure is somewhere inside the gap between 2 squares. (rare)
        x1 = random.randrange(2, max(3, _h - 4))
        y1 = random.randrange(2, max(3, _w - 4))
        x2 = random.randrange(x1 + 1, min(_h, x1 + 3))
        y2 = random.randrange(y1 + 1, min(_w, y1 + 3))
        
        x3 = random.randrange(x1)
        x4 = random.randrange(min(_h - 1, x2 + 1), _h)
        y3 = random.randrange(y1)
        y4 = random.randrange(min(_w - 1, y2 + 1), _w)
        
        setOfTiles = set()
        
        for i in range(x3, x4 + 1):
            for j in range(y3, y4 + 1):
                if i in (x1, x2 + 1) and j in range(y1, y2 + 1): continue
                setOfTiles.add(j + i * _w)
        
        isTruth = (_treasureLocation) in setOfTiles
        
        return (hint, setOfTiles, isTruth, f"The treasure is somewhere inside the gap between {[x1, y1, x2, y2]} and {[x3, y3, x4, y4]}.")
    else: # The treasure is in a region that has mountain.
        _temp = dict()
        regions = set()
        
        for i in range(_h):
            for j in range(_w):
                if len(_map[i][j]) > 1 and _map[i][j][1] == 'M': regions.add(_map[i][j][0])
                
                if _map[i][j][0] not in _temp.keys(): _temp[_map[i][j][0]] = [i * _w + j]
                else: _temp[_map[i][j][0]].append(i * _w + j)
        
        listOfTiles = []
        for r in regions:
            listOfTiles = listOfTiles + _temp[r]
            
        isTruth = (_treasureLocation) in listOfTiles
        
        return (hint, listOfTiles, isTruth, "The treasure is in a region that has mountain.")

# print(genHint(5, 5, 3, (3, 4), (1, 2), (5, 5), [['0', '0', '0', '0', '0'], ['0', '1', '1M', '1P', '1'], ['0', '1P', '2M', '2', '2'], ['0', '3', '3M', '3', '3'], ['0', '0', '0', '0', '0']], []))