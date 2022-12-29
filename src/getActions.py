import heapq

def calAvgTiles(_removed: set, _agent: int, _w: int, _h: int):
    cnt = 0
    sum = 0
    for i in range(_w * _h):
        if i not in _removed:
           sum += abs(i - _agent)
           cnt += 1
    if cnt: return sum / cnt
    return 1000000000

def getBestMove(_agent: int, _w: int, _h: int, toRemove: list, _map: list):
    # scan 5x5
    xAgent = _agent // _w
    yAgent = _agent % _w
    
    cnt = 0
    for i in range(xAgent - 2, xAgent + 3):
        for j in range(yAgent - 2, yAgent + 3):
            if 0 <= i < _h and 0 <= j < _w and i * _w + j in toRemove:
                cnt += 1
    action = (cnt, "large scan", _agent)
    # small move
    check = [False] * 4
    moves = [(0, 1), (1, 0), (-1, 0), (0, -1), (0, 2), (2, 0), (-2, 0), (0, -2)]
    for i in range(8):
        move = moves[i]
        x, y = _agent // _w + move[0], _agent % _w + move[1]
        if x < 0 or x >= _h or y < 0 or y >= _w or check[i % 4]: continue
        if _map[x][y] == '0' or 'M' in _map[x][y]: 
            check[i % 4] = True
            continue
        
        cnt = 0
        for i in range(xAgent - 1, xAgent + 2):
            for j in range(yAgent - 1, yAgent + 2):
                if 0 <= i < _h and 0 <= j < _w and i * _w + j in toRemove:
                    cnt += 1
        if cnt > action[0]: action = (cnt, "move and small scan", move[0] * _w + move[1])
    
    if action[0] == 0:
        moves = [(0, 3), (3, 0), (-3, 0), (0, -3), (4, 0), (0, 4), (-4, 0), (0, 4)]
        action = (100000, "move", 1)
        for i in range(8):
            move = moves[i]
            x, y = _agent // _w + move[0], _agent % _w + move[1]
            if x < 0 or x >= _h or y < 0 or y >= _w or check[i % 4]: continue
            if _map[x][y] == '0' or 'M' in _map[x][y]: 
                check[i % 4] = True
                continue
            sum = 0
            for tile in toRemove:
                sum += abs(tile - x * _w + y)
            if sum < action[0]: action = (sum, "move", x * _w + y)
            
    return action
def getActions(_w: int, _h: int, _freed: bool, _canTele: bool, _known: bool, _treasure: int, _agent: int, _pirate: int, _prevMove: int, _removed: set, _hints: list, _map: list):
    if _known and _treasure == _agent:
        return (0, "large scan", _agent)
    elif _known and _canTele:
        return (0, "teleport", _treasure)
    elif not _freed:
        actions = []
        nRe = len(_removed)
        
        # verify action
        for hint in _hints:
            cnt = 0
            for tile in hint[0][1]:
                if tile not in _removed:
                    cnt += 1
            heapq.heappush(actions, (max(cnt, _w * _h - nRe - cnt), "verify", hint))
        
        # large scan
        xAgent = _agent // _w
        yAgent = _agent % _w
        cnt = 0
        for i in range(xAgent - 2, xAgent + 3):
            for j in range(yAgent - 2, yAgent + 3):
                if 0 <= i < _h and 0 <= j < _w and i * _w + j not in _removed:
                    cnt += 1
        
        heapq.heappush(actions, (cnt, "large scan", _agent))
        
        check = [False] * 4
        
        # small move
        moves = [(0, 1), (1, 0), (-1, 0), (0, -1), (0, 2), (2, 0), (-2, 0), (0, -2)]
        mn = 1000000
        remove = 0
        ac = 0
        for i in range(8):
            move = moves[i]
            x, y = _agent // _w + move[0], _agent % _w + move[1]
            if x < 0 or x >= _h or y < 0 or y >= _w or check[i % 4]: continue
            if _map[x][y] == '0' or 'M' in _map[x][y]: 
                check[i % 4] = True
                continue
            
            cnt = 0
            for i in range(xAgent - 1, xAgent + 2):
                for j in range(yAgent - 1, yAgent + 2):
                    if 0 <= i < _h and 0 <= j < _w and i * _w + j not in _removed:
                        cnt += 1
            temp = calAvgTiles(_removed, x * _w + y, _w, _h) - cnt
            if temp < mn:
                mn = temp
                ac = move[0] * _w + move[1]
                remove = cnt
            
        if ac != 0: heapq.heappush(actions, (remove + 6, "move and small scan", ac))
        
        # large move
        moves = [(0, 3), (3, 0), (-3, 0), (0, -3), (4, 0), (0, 4), (-4, 0), (0, 4)]
        ac = 0
        mn = 100000000
        for i in range(8):
            move = moves[i]
            x, y = _agent // _w + move[0], _agent % _w + move[1]
            if x < 0 or x >= _h or y < 0 or y >= _w or check[i % 4]: continue
            if _map[x][y] == '0' or 'M' in _map[x][y]: 
                check[i % 4] = True
                continue
            temp = calAvgTiles(_removed, x * _w + y, _w, _h)
            if temp < mn:
                mn = temp
                ac = move[0] * _w + move[1]
        
        if ac: heapq.heappush(actions, (12, "move", ac))
        
        return actions[-1]
    else:
        if _canTele: return (0, "teleport", _pirate)
        if _pirate == _prevMove: return (0, "large scan", _agent)
        
        tiles = []
        inRangeOfPirate = []
        xPi = _pirate // _w
        yPi = _pirate % _w
        if _pirate - _prevMove in [1, 2]: # move right
            for x in range(xPi, _h):
                for y in range(_w):
                    if x * _w + y not in _removed:
                        tiles.append(tile)
                        if (x - xPi, y - yPi) in [(2, 0), (1, 1), (0, 2), (1, 0), (0, 1), (-1, 0), (-2, 0), (-1, 1)]:
                            inRangeOfPirate.append(x + _w + y)
        if _pirate - _prevMove in [-1, -2]: # move left
            for x in range(xPi + 1):
                for y in range(_w):
                    if x * _w + y not in _removed:
                        tiles.append(tile)
                        if (x - xPi, y - yPi) in [(2, 0), (1, -1), (0, 2), (1, 0), (0, -1), (-1, 0), (-2, 0), (-1, -1)]:
                            inRangeOfPirate.append(x + _w + y)
        if _pirate - _prevMove in [_w, 2*_w]: # move up
            for x in range(_h):
                for y in range(yPi + 1):
                    if x * _w + y not in _removed:
                        tiles.append(tile)
                        if (x - xPi, y - yPi) in [(-2, 0), (-1, 1), (0, 2), (-1, -1), (0, -2), (-1, 0), (0, 1), (0, -1)]:
                            inRangeOfPirate.append(x + _w + y)
        if _pirate - _prevMove in [-_w, -2*_w]: # move down
            for x in range(_h):
                for y in range(yPi, _w):
                    if x * _w + y not in _removed:
                        tiles.append(tile)
                        if (x - xPi, y - yPi) in [(2, 0), (1, 1), (0, 2), (1, -1), (0, -2), (1, 0), (0, 1), (0, -1)]:
                            inRangeOfPirate.append(x + _w + y)
        if _pirate - _prevMove == _w - 1: # down left
            for x in range(xPi, _h):
                for y in range(yPi + 1):
                    if x * _w + y not in _removed:
                        tiles.append(tile)
                        if (x - xPi, y - yPi) in [(2, 0), (0, -2), (1, 0), (0, -1), (1, -1)]:
                            inRangeOfPirate.append(x + _w + y)
        if _pirate - _prevMove == _w + 1: # down right
            for x in range(xPi, _h):
                for y in range(yPi, _w):
                    if x * _w + y not in _removed:
                        tiles.append(tile)
                        if (x - xPi, y - yPi) in [(2, 0), (0, 2), (1, 0), (0, 1), (1, 1)]:
                            inRangeOfPirate.append(x + _w + y)
        if _pirate - _prevMove == -_w - 1: # up left
            for x in range(xPi + 1):
                for y in range(yPi + 1):
                    if x * _w + y not in _removed:
                        tiles.append(tile)
                        if (x - xPi, y - yPi) in [(-2, 0), (0, -2), (-1, 0), (0, -1), (-1, -1)]:
                            inRangeOfPirate.append(x + _w + y)
        if _pirate - _prevMove == -_w + 1: # up right
            for x in range(xPi + 1):
                for y in range(yPi + 1):
                    if x * _w + y not in _removed:
                        tiles.append(tile)
                        if (x - xPi, y - yPi) in [(-2, 0), (0, 2), (-1, 0), (0, 1), (-1, 1)]:
                            inRangeOfPirate.append(x + _w + y)
        
        if len(inRangeOfPirate) > 0:
            return getBestMove(_agent, _w, _h, inRangeOfPirate, _map)
        else:
            return getBestMove(_agent, _w, _h, tiles, _map)