import argparse, os, re
from preprocessing import preprocessing
from getActions import getActions
from get_hint import genHint

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Treasure Island')
    parser.add_argument('--read', type=str, default='data/input/', help='Input file directory')
    
    args = parser.parse_args()
    
    inputFolder = args.read
    
    os.chdir('..')
    
    if not os.path.exists(inputFolder):
        print('Input folder not found')
        exit()
    
    inputFilePattern = re.compile('MAP_\d+\.txt')
    
    for file in os.listdir(inputFolder):
        if not re.match(inputFilePattern, file): continue
        testNum = file[4:-4]

        with open(os.path.join(inputFolder, file), 'r') as f:
            print(f'Solving map {testNum}')
            
            ## Input
            mapSize = [int(item) for item in f.readline().split()] # contain width and height
            revealRound = int(f.readline()) # defines the round number that the pirate reveal location
            freeRound = int(f.readline()) # defines the round number that the pirate is free
            numOfRegions = int(f.readline()) # defines the number of regions
            treasure = [int(item) for item in f.readline().split()]
            treasure = treasure[0] * mapSize[0] + treasure[1]
            _map = []
            
            for i in range(mapSize[1]):
                _map.append(f.readline().replace(' ', '').replace('\n', '').split(';'))
            
            f.close()

        agent, pirate, path = preprocessing(mapSize[0], mapSize[1], treasure, _map)
        path.pop(0)
        if pirate == -1:
            print("There does not exist any path from the prisons to treasure.")
            continue
    
        for r in _map:
            print(r)
        
        round = 1
        hints = []
        removedTiles = set()
        w, h = mapSize[0], mapSize[1]
        for i in range(mapSize[1]):
            for j in range(mapSize[0]):
                if _map[i][j] == '0' or 'M' in _map[i][j]:
                    removedTiles.add(i * mapSize[1] + j)
        
        hintWeights = [1, 1, 1, 1, 1, 1, 0, 0.5, 1, 1, 1, 1, 0.5, 1, 0.5, 1]
        canTele = True
        knowTreasure = False
        freed = False
        prevMove = pirate
        
        while True:
            if round == revealRound:
                hintWeights = [1, 1, 1, 1, 1, 1, 1, 0.5, 1, 1, 1, 1, 0.5, 1, 0.5, 1]
                print(f"The location of pirate is {(pirate // w, pirate % w)}.")
            if round == freeRound:
                print("The pirate has been freed.")
                freed = True
            
            # getHint
            hint = genHint(mapSize[0], mapSize[1], numOfRegions, treasure, pirate, agent, _map, hintWeights)
            if round == 1:
                while ~hint[2]:
                    hint = genHint(mapSize[0], mapSize[1], numOfRegions, treasure, pirate, agent, _map, hintWeights)
                    
                if hint[0] in [1, 4, 6, 9, 13]:
                    for tile in hint[1]:
                        removedTiles.add(tile)
                else:
                    for tile in range(mapSize[0] * mapSize[1]):
                        if tile not in hint[1]:
                            removedTiles.add(tile)
            else: hints.append((hint, round))
            print("The pirate tells you a hint: " + hint[-1])
                
            # getActions
            action = getActions(w, h, freed, canTele, knowTreasure, treasure, agent, pirate, prevMove, removedTiles, hints, _map)
            if action[1] == "teleport":
                canTele = False
                agent = action[2]
                print(f"Teleport to {(agent // w, agent % w)}")
            if action[1] == "move":
                print(f"Move from {(agent // w, agent % w)} to location {((agent + action[2]) // w, (agent + action[2]) % w)}")
                agent += action[2]
            if action[1] == "move and small scan":
                print(f"Move from {(agent // w, agent % w)} to location {((agent + action[2]) // w, (agent + action[2]) % w)} and scan 3x3 area.")
                agent += action[2]
                for i in range(agent // w - 1, agent // w + 2):
                    for j in range(agent % w - 1, agent % w + 2):
                        if 0 <= i < mapSize[1] and 0 <= j < mapSize[0] and i * mapSize[1] + j not in removedTiles:
                            removedTiles.add(i * w + j)
            if action[1] == "large scan":
                for i in range(agent // w - 2, agent // w + 3):
                    for j in range(agent % w - 2, agent % w + 3):
                        if 0 <= i < mapSize[1] and 0 <= j < mapSize[0] and i * mapSize[1] + j not in removedTiles:
                            removedTiles.add(i * w + j)
                print(f"Agent large scans at {(agent // w, agent % w)}")
            if action[1] == "verify":
                hint, hRound = action[2]
                if hint[2]:
                    if hint[0] in [1, 4, 6, 9, 13]:
                        for tile in hint[1]:
                            removedTiles.add(tile)
                    else:
                        for tile in range(mapSize[0] * mapSize[1]):
                            if tile not in hint[1]:
                                removedTiles.add(tile)
                else:
                    if hint[0] not in [1, 4, 6, 9, 13]:
                        for tile in hint[1]:
                            removedTiles.add(tile)
                    else:
                        for tile in range(mapSize[0] * mapSize[1]):
                            if tile not in hint[1]:
                                removedTiles.add(tile)
                print(f"Verify hint at {hRound}, the hint is {hint[2]}.")
            if treasure in removedTiles:
                print("WIN")
                break
            if len(removedTiles) == w * h - 1:
                knowTreasure = True          
            action = getActions(w, h, freed, canTele, knowTreasure, treasure, agent, pirate, prevMove, removedTiles, hints, _map)
            if action[1] == "teleport":
                canTele = False
                agent = action[2]
                print(f"Teleport to {(agent // w, agent % w)}")
            if action[1] == "move":
                print(f"Move from {(agent // w, agent % w)} to location {((agent + action[2]) // w, (agent + action[2]) % w)}")
                agent += action[2]
            if action[1] == "move and small scan":
                print(f"Move from {(agent // w, agent % w)} to location {((agent + action[2]) // w, (agent + action[2]) % w)} and scan 3x3 area.")
                agent += action[2]
                for i in range(agent // w - 1, agent // w + 2):
                    for j in range(agent % w - 1, agent % w + 2):
                        if 0 <= i < mapSize[1] and 0 <= j < mapSize[0] and i * mapSize[1] + j not in removedTiles:
                            removedTiles.add(i * w + j)
            if action[1] == "large scan":
                for i in range(agent // w - 2, agent // w + 3):
                    for j in range(agent % w - 2, agent % w + 3):
                        if 0 <= i < mapSize[1] and 0 <= j < mapSize[0] and i * mapSize[1] + j not in removedTiles:
                            removedTiles.add(i * w + j)
                print(f"Agents large scan at {(agent // w, agent % w)}")
            if action[1] == "verify":
                hint, hRound = action[2]
                if hint[2]:
                    if hint[0] in [1, 4, 6, 9, 13]:
                        for tile in hint[1]:
                            removedTiles.add(tile)
                    else:
                        for tile in range(mapSize[0] * mapSize[1]):
                            if tile not in hint[1]:
                                removedTiles.add(tile)
                else:
                    if hint[0] not in [1, 4, 6, 9, 13]:
                        for tile in hint[1]:
                            removedTiles.add(tile)
                    else:
                        for tile in range(mapSize[0] * mapSize[1]):
                            if tile not in hint[1]:
                                removedTiles.add(tile)
                print(f"Verify hint at {hRound}, the hint is {hint[2]}.")
            if treasure in removedTiles:
                print("WIN")
                break
            if len(removedTiles) == w * h - 1:
                knowTreasure = True
            if round >= freeRound:
                prevMove = pirate
                pirate = path[0]
                path.pop(0)
                print(f"The pirate move to location {(pirate // w, pirate % w)}")

            round += 1
            # check finish
            if pirate == treasure:
                print("LOSE")
                break
            