import argparse, os, re
# from get_hint import genHint

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Treasure Island')
    parser.add_argument('--read', type=str, default='data/input/', help='Input file directory')
    parser.add_argument('--gen_map', type=bool, default=False, help='Generating map')
    
    args = parser.parse_args()
    
    if args.gen_map:
        pass
    
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
            mapSize = [int(item) for item in f.readline().split()] # contain weight and height
            revealRound = int(f.readline()) # defines the round number that the pirate reveal location
            freeRound = int(f.readline()) # defines the round number that the pirate is free
            numOfRegions = int(f.readline()) # defines the number of regions
            treasureLocation = [int(item) for item in f.readline().split()]
            _map = []
            
            for i in range(mapSize[1]):
                _map.append(f.readline().replace(' ', '').replace('\n', '').split(';'))
                
            print(_map)