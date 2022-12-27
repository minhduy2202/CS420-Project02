import random

def genMap(_h: int, _w: int, numOfRegions: int, dataFolder: str):
    """
    *args:
        @_w: Width.
        @_h: Height.
        @_numOfRegions: Number of regions on the map (including the sea).
    
    *return:
        myMap: The game map.
        numOfRegions: The number of regions.
        treasureLocation: The location of treasure.
        agentLocation: The location of agent.
        pirateLocation: The location of pirate.
    """
    
    f = open("../"+ dataFolder + "genMap.txt", "w")
    # myMap = [['0', '0', '0', '0', '0'], ['0', '1', '1M', '1P', '1'], ['0', '1P', '2M', '2', '2'], ['0', '3', '3M', '3', '3'], ['0', '0', '0', '0', '0']]
    
    myMap = []
    
    for i in range(_h):
        row = []
        for j in range(_w):
            row.append("0")
        myMap.append(row)
    
    # generate random regions
    for i in range(1, numOfRegions):
        x = random.randint(1, _w - 2)
        y = random.randint(1, _h - 2)
        myMap[y][x] = str(i)
    
    # assign regions to cells
    for i in range(1, numOfRegions):
        for j in range(1, _h - 1):
            for k in range(1, _w - 1):
                if myMap[j][k] != "0":
                    continue
                if (myMap[j][k - 1] == str(i) or myMap[j][k + 1] == str(i) or myMap[j - 1][k] == str(i) or myMap[j + 1][k] == str(i)):
                    myMap[j][k] = str(i)
    
    # assign mountains
    mountanLocations = []
    for i in range(1, numOfRegions):
        x = random.randint(1, _w - 2)
        y = random.randint(1, _h - 2)
        while myMap[y][x] != str(i):
            x = random.randint(1, _w - 2)
            y = random.randint(1, _h - 2)
        
        mountanLocations.append([y, x])
        myMap[y][x] += "M"

    # assign some random prisons to map
    # prisons in not in the sea and not in mountains
    prisonLocations = []
    numOfPrisons = random.randint(2, numOfRegions - 1)
    for i in range(numOfPrisons):
        x = random.randint(1, _w - 2)
        y = random.randint(1, _h - 2)
        while "0" in myMap[y][x] or "M" in myMap[y][x] or "P" in myMap[y][x]:
            x = random.randint(1, _w - 2)
            y = random.randint(1, _h - 2)
        
        prisonLocations.append([y, x])
        myMap[y][x] += "P"

    # assign treasure
    x = random.randint(1, _w - 2)
    y = random.randint(1, _h - 2)
    while "0" in myMap[y][x] or "M" in myMap[y][x] or "P" in myMap[y][x]:
        x = random.randint(1, _w - 2)
        y = random.randint(1, _h - 2)
    
    treasureLocation = [y, x]

    # assign pirate
    pirateLocation = random.choice(prisonLocations)

    # assign agent
    x = random.randint(1, _w - 2)
    y = random.randint(1, _h - 2)
    while "0" in myMap[y][x] or "M" in myMap[y][x] or "P" in myMap[y][x] or [y, x] == treasureLocation:
        x = random.randint(1, _w - 2)
        y = random.randint(1, _h - 2)

    agentLocation = [y, x]
    
    # write map to file
    for i in range(_h):
        for j in range(_w - 1):
            f.write(myMap[i][j] + "; ")
        f.write(myMap[i][_h - 1])
        f.write("\n")
    f.close()

    return myMap, numOfRegions, treasureLocation, agentLocation, pirateLocation

# print(genMap(20, 20, 9, "data/input/"))
genMap(8, 8, 4, "data/input/")