import argparse, os, re
from preprocessing import preprocessing
# from get_hint import genHint
from get_map import genMap

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Treasure Island')
    parser.add_argument('--read', type=str, default='data/input/', help='Input file directory')
    parser.add_argument('--gen_map', type=bool, default=False, help='Generating map')
    
    args = parser.parse_args()

    # python3 main.py --gen_map True
    if args.gen_map:
        map_gen, numOfRegions_gen, treasure_gen, agentLocation_gen, pirateLocation_gen = genMap(15, 15, numOfRegions=6, dataFolder=args.read)
    
    inputFolder = args.read
    
    os.chdir('..')
    
    print(os.getcwd())
    
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
            

            if args.gen_map:
                mapSize = [len(map_gen[0]), len(map_gen)]
                numOfRegions = numOfRegions_gen
                treasure = treasure_gen[0] * mapSize[0] + treasure_gen[1]
                _map = map_gen
            
            f.close()

        agent, pirate, path = preprocessing(mapSize[0], mapSize[1], treasure, _map)
        if pirate == -1:
            print("There does not exist any path from the prisons to treasure.")
            continue
        
        round = 1
        kBase = []
        hints = []
        removedTiles = set()
        
        while True:
            if round == revealRound:
                # adjust hint probability
                pass
            if round == freeRound:
                # free pirate
                pass
            # getHint
            # getActions
            # applyActions
            # Pirate moves if free
            # check finish