import sv_ttk
import argparse
import os
import re
from preprocessing import preprocessing
from getActions import getActions
from get_hint import genHint
import globals
from visualization import Visualization


def fastestPath(agent: int, treasure: int, _map: list, _w: int, _h: int):
    queue = [[agent]]
    explored = [agent]

    while queue:
        path = queue.pop(0)

        if path[-1] == treasure:
            return path

        check = [False] * 4
        adjacent = [-1, 1, -_w, _w, -2, 2, -2*_w, 2 *
                    _w, -3, 3, -3*_w, 3*_w, -4, 4, -4*_w, 4*_w]
        for i in range(len(adjacent)):
            cell = path[-1] + adjacent[i]
            if cell < 0 or cell >= _w * _h or check[i % 4]:
                continue
            if cell in explored:
                continue
            if 'M' in _map[cell // _w][cell % _w] or '0' in _map[cell // _w][cell % _w]:
                check[i % 4] = True
                continue

            queue.append(path + [cell])
            explored.append(cell)

    return []


def writeLog2File(sFile, sLocation="data/output/"):
    f = open(sLocation + "LOG_" + sFile + ".txt", "w")

    f.write(str(len(globals.lst_logs)))
    f.write("\n")
    f.write(globals.lst_logs[-1])

    for x in globals.lst_logs:
        f.write("\n")
        f.write(x)

    f.close()


def printLog():
    print(str(len(globals.lst_logs)))
    print(globals.lst_logs[-1])

    for x in globals.lst_logs:
        print(x)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Treasure Island')
    parser.add_argument('--read', type=str,
                        default='data/input/', help='Input file directory')

    args = parser.parse_args()

    inputFolder = args.read

    os.chdir('..')

    if not os.path.exists(inputFolder):
        print('Input folder not found')
        exit()

    # inputFilePattern = re.compile('MAP_\d+\.txt')
    sInputFile = "MAP_05\.txt"
    inputFilePattern = re.compile(sInputFile)
    isVisualize = True

    for file in os.listdir(inputFolder):
        if not re.match(inputFilePattern, file):
            continue
        testNum = file[4:-4]

        with open(os.path.join(inputFolder, file), 'r') as f:
            print(f'Solving map {testNum}')

            # Input
            # contain width and height
            mapSize = [int(item) for item in f.readline().split()]
            # defines the round number that the pirate reveal location
            revealRound = int(f.readline())
            # defines the round number that the pirate is free
            freeRound = int(f.readline())
            numOfRegions = int(f.readline())  # defines the number of regions
            treasure = [int(item) for item in f.readline().split()]
            treasure = treasure[0] * mapSize[0] + treasure[1]
            _map = []

            for i in range(mapSize[1]):
                _map.append(f.readline().replace(
                    ' ', '').replace('\n', '').split(';'))

            f.close()

        agent, pirate, path = preprocessing(
            mapSize[0], mapSize[1], treasure, _map)
        w, h = mapSize[0], mapSize[1]
        visualize = Visualization(_map, numOfRegions)

        path.pop(0)
        if pirate == -1:
            globals.lst_logs.append(
                "There does not exist any path from the prisons to treasure.")
            # print("There does not exist any path from the prisons to treasure.")
            continue

        # Get Visualization
        if isVisualize:
            # visualize = MyVisualization(
            #     _map, numOfRegions, [agent // w, agent % w])
            visualize.createNewTab(
                0, agent, pirate, treasure, [], [], False, [])

        round = 1
        hints = []
        removedTiles = set()
        for i in range(mapSize[1]):
            for j in range(mapSize[0]):
                if _map[i][j] == '0' or 'M' in _map[i][j]:
                    removedTiles.add(i * mapSize[1] + j)

        hintWeights = [1, 1, 1, 1, 1, 1, 0, 0.5, 1, 1, 1, 1, 0.5, 1, 0.5, 1]
        canTele = True
        knowTreasure = False
        freed = False
        prevMove = pirate
        aPath = []

        isWin = True
        final_agent, final_pirate, final_isPirateFree, final_round, final_listOfTilesHint, final_removedTiles = agent, pirate, freed, 1, [], []

        while True:
            globals.lst_logs.append(f"Round {round}")
            logs = []
            # print(f"Round {round}")
            if round == revealRound:
                hintWeights = [1, 1, 1, 1, 1, 1, 1,
                               0.5, 1, 1, 1, 1, 0.5, 1, 0.5, 1]

                globals.lst_logs.append(
                    f"The location of pirate is {(pirate // w, pirate % w)}.")
                logs.append(
                    f"The location of pirate is {(pirate // w, pirate % w)}.")
                # print(f"The location of pirate is {(pirate // w, pirate % w)}.")
            if round == freeRound:

                globals.lst_logs.append("The pirate has been freed.")
                logs.append("The pirate has been freed.")
                # print("The pirate has been freed.")
                freed = True

            # getHint
            hint = genHint(mapSize[0], mapSize[1], numOfRegions,
                           treasure, pirate, agent, _map, hintWeights)

            final_listOfTilesHint = hint[1]

            if round == 1:
                while not hint[2]:
                    hint = genHint(
                        mapSize[0], mapSize[1], numOfRegions, treasure, pirate, agent, _map, hintWeights)

                if hint[0] in [1, 4, 6, 9, 13]:
                    for tile in hint[1]:
                        removedTiles.add(tile)
                else:
                    for tile in range(mapSize[0] * mapSize[1]):
                        if tile not in hint[1]:
                            removedTiles.add(tile)
                final_listOfTilesHint = hint[1]
            else:
                hints.append((hint, round))

            # Visualize the hint
            # if isVisualize:
            #     # visualize.updateHintToTab(_map, round, hint[1], [
            #     #     agent // w, agent % w], [pirate // w, pirate % w], freed)
            globals.lst_logs.append("The pirate tells you a hint: " + hint[-1])
            logs.append("The pirate tells you a hint: " + hint[-1])
            # print("The pirate tells you a hint: " + hint[-1])

            if round >= freeRound:
                prevMove = pirate
                pirate = path[0]
                path.pop(0)
                globals.lst_logs.append(
                    f"The pirate move to location {(pirate // w, pirate % w)}")
                logs.append(
                    f"The pirate move to location {(pirate // w, pirate % w)}")
                # print(f"The pirate move to location {(pirate // w, pirate % w)}")

            # getActions
            if knowTreasure:
                cnt = 0
                win = False
                if canTele:
                    cnt += 1
                    canTele = False
                    agent = treasure
                    win = True
                    globals.lst_logs.append(
                        f"Teleport to {(agent // w, agent % w)}")
                    logs.append(f"Teleport to {(agent // w, agent % w)}")
                if len(aPath) == 0:
                    globals.lst_logs.append(
                        f"Agent large scans at {(agent // w, agent % w)}")
                    win = True
                    logs.append(
                        f"Agent large scans at {(agent // w, agent % w)}")
                    # print(f"Teleport to {(agent // w, agent % w)}")
                while cnt < 2 and aPath and not win:
                    xAgent = agent // w
                    yAgent = agent % w
                    for x in range(xAgent - 2, xAgent + 3):
                        for y in range(yAgent - 2, yAgent + 3):
                            if 0 < x <= h and 0 < y <= w and x*w + y == treasure:
                                globals.lst_logs.append(
                                    f"Agent large scans at {(xAgent, yAgent)}")
                                logs.append(
                                    f"Agent large scans at {(xAgent, yAgent)}")
                                # print(f"Agent large scans at {(xAgent, yAgent)}")
                                win = True
                                break
                    if win:
                        break

                    new = aPath[0]
                    if new - agent in [-1, 1, -2, 2, -w, w, -2*w, 2*w]:
                        globals.lst_logs.append(
                            f"Move from {(agent // w, agent % w)} to location {(new // w, new % w)} and scan 3x3 area.")
                        logs.append(
                            f"Move from {(agent // w, agent % w)} to location {(new // w, new % w)} and scan 3x3 area.")
                        # print(f"Move from {(agent // w, agent % w)} to location {(new // w, new % w)} and scan 3x3 area.")
                        agent += action[2]
                        for i in range(new // w - 1, new // w + 2):
                            for j in range(new % w - 1, new % w + 2):
                                if 0 < x <= h and 0 < y <= w and x*w + y == treasure:
                                    win = True
                                    break
                    else:
                        globals.lst_logs.append(
                            f"Move from {(agent // w, agent % w)} to location {(new // w, new % w)}")
                        logs.append(
                            f"Move from {(agent // w, agent % w)} to location {(new // w, new % w)}")
                        # print(f"Move from {(agent // w, agent % w)} to location {(new // w, new % w)}")
                    aPath.pop(0)
                    cnt += 1
                    agent = new
                if win:
                    globals.lst_logs.append("WIN")
                    logs.append("WIN")
                    # print("WIN")
                    break
            else:
                action = getActions(w, h, freed, canTele, knowTreasure, treasure,
                                    agent, pirate, prevMove, removedTiles, hints, _map)
                if action[1] == "teleport":
                    canTele = False
                    agent = action[2]

                    globals.lst_logs.append(
                        f"Teleport to {(agent // w, agent % w)}")
                    logs.append(f"Teleport to {(agent // w, agent % w)}")
                    # print(f"Teleport to {(agent // w, agent % w)}")
                if action[1] == "move":
                    globals.lst_logs.append(
                        f"Move from {(agent // w, agent % w)} to location {((agent + action[2]) // w, (agent + action[2]) % w)}")
                    logs.append(
                        f"Move from {(agent // w, agent % w)} to location {((agent + action[2]) // w, (agent + action[2]) % w)}")
                    # print(f"Move from {(agent // w, agent % w)} to location {((agent + action[2]) // w, (agent + action[2]) % w)}")
                    agent += action[2]
                if action[1] == "move and small scan":
                    globals.lst_logs.append(
                        f"Move from {(agent // w, agent % w)} to location {((agent + action[2]) // w, (agent + action[2]) % w)} and scan 3x3 area.")
                    logs.append(
                        f"Move from {(agent // w, agent % w)} to location {((agent + action[2]) // w, (agent + action[2]) % w)} and scan 3x3 area.")
                    # print(f"Move from {(agent // w, agent % w)} to location {((agent + action[2]) // w, (agent + action[2]) % w)} and scan 3x3 area.")
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

                    globals.lst_logs.append(
                        f"Agent large scans at {(agent // w, agent % w)}")
                    logs.append(
                        f"Agent large scans at {(agent // w, agent % w)}")
                    # print(f"Agent large scans at {(agent // w, agent % w)}")
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
                    hints.remove(action[2])

                    globals.lst_logs.append(
                        f"Verify hint at round {hRound}, the hint is " + ("True." if hint[2] else "False."))
                    logs.append(
                        f"Verify hint at round {hRound}, the hint is " + ("True." if hint[2] else "False."))
                    # print(f"Verify hint at round {hRound}, the hint is " + ("True." if hint[2] else "False."))
                if treasure in removedTiles:
                    globals.lst_logs.append("WIN")
                    logs.append("WIN")
                    # print("WIN")
                    break
                if len(removedTiles) == w * h - 1:
                    aPath = fastestPath(agent, treasure, _map, w, h)
                    if aPath:
                        aPath.pop(0)
                    knowTreasure = True
                action = getActions(w, h, freed, canTele, knowTreasure, treasure,
                                    agent, pirate, prevMove, removedTiles, hints, _map)
                if action[1] == "teleport":
                    canTele = False
                    agent = action[2]
                    globals.lst_logs.append(
                        f"Teleport to {(agent // w, agent % w)}")
                    logs.append(f"Teleport to {(agent // w, agent % w)}")
                    # print(f"Teleport to {(agent // w, agent % w)}")
                if action[1] == "move":
                    globals.lst_logs.append(
                        f"Move from {(agent // w, agent % w)} to location {((agent + action[2]) // w, (agent + action[2]) % w)}")
                    logs.append(
                        f"Move from {(agent // w, agent % w)} to location {((agent + action[2]) // w, (agent + action[2]) % w)}")
                    # print(f"Move from {(agent // w, agent % w)} to location {((agent + action[2]) // w, (agent + action[2]) % w)}")
                    agent += action[2]
                if action[1] == "move and small scan":
                    globals.lst_logs.append(
                        f"Move from {(agent // w, agent % w)} to location {((agent + action[2]) // w, (agent + action[2]) % w)} and scan 3x3 area.")
                    logs.append(
                        f"Move from {(agent // w, agent % w)} to location {((agent + action[2]) // w, (agent + action[2]) % w)} and scan 3x3 area.")
                    # print(f"Move from {(agent // w, agent % w)} to location {((agent + action[2]) // w, (agent + action[2]) % w)} and scan 3x3 area.")
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

                    globals.lst_logs.append(
                        f"Agents large scan at {(agent // w, agent % w)}")
                    logs.append(
                        f"Agents large scan at {(agent // w, agent % w)}")
                    # print(f"Agents large scan at {(agent // w, agent % w)}")
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
                    hints.remove(action[2])

                    globals.lst_logs.append(
                        f"Verify hint at round {hRound}, the hint is " + ("True." if hint[2] else "False."))
                    logs.append(
                        f"Verify hint at round {hRound}, the hint is " + ("True." if hint[2] else "False."))
                    # print(f"Verify hint at round {hRound}, the hint is " + ("True." if hint[2] else "False."))
                if treasure in removedTiles:
                    globals.lst_logs.append("WIN")
                    logs.append("WIN")
                    # print("WIN")
                    break
                if len(removedTiles) == w * h - 1:
                    aPath = fastestPath(agent, treasure, _map, w, h)
                    if aPath:
                        aPath.pop(0)
                    knowTreasure = True

            # Add tab to Visualization
            if isVisualize:
                # visualize.addNewTab(_map, round + 1, removedTiles,
                #                     [agent // w, agent % w], [pirate // w, pirate % w], freed)
                visualize.createNewTab(
                    round, agent, pirate, treasure, hint[1], removedTiles, freed, logs)

            final_pirate, final_isPirateFree, final_round, final_removedTiles = pirate, freed, round, removedTiles

            if pirate == treasure:
                isWin = False
                globals.lst_logs.append("LOSE")
                logs.append("LOSE")
                # print("LOSE")
                break

            round += 1
            # print('------------------------------------')
            # check finish

        # write log to file before visualizing
        writeLog2File(file[4:-4], sLocation="data/output/")
        print("Done (output to log file)!")
        print("===================================")
        printLog()
        print("===================================")
        print("The visualization...")

        # show visualization
        if isVisualize:
            # if final_round > 1:
            #     visualize.updateLastHintToTab(final_round + 1, final_listOfTilesHint, [
            #         final_agent // w, final_agent % w], [final_pirate // w, final_pirate % w], final_isPirateFree)
            if(isWin):
                visualize.createNewTab(
                    round, agent, pirate, treasure, hint[1], removedTiles, freed, logs)
            visualize.addLastTab(isWin)

            visualize.showVisualization()
