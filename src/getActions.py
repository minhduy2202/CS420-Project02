import heapq

def calAvgTiles(_removed: set, _agent: int, _w: int, _h: int):
    cnt = 0
    x, y = 0, 0
    for i in range(_w * _h):
        if i not in _removed:
           x += i // _w
           y += i % _w
           cnt += 1
    if cnt: return abs(x / cnt - _agent // _w) + abs(y / cnt - _agent % _w)
    return 1000000000

def getBestAction(_agent: int, _w: int, _h: int, _hints: list, _removed: list, _map: list):
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
        
    if ac != 0: heapq.heappush(actions, (remove + min(_w * _h - len(_removed) + 1, 6), "move and small scan", ac))
    
    # large move
    moves = [(0, 3), (3, 0), (-3, 0), (0, -3), (4, 0), (0, 4), (-4, 0), (0, 4)]
    ac = 0
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
    
    if ac != 0: heapq.heappush(actions, (min(_w * _h - len(_removed) + 2, 8), "move", ac))
    
    return actions[-1]

def getActions(_w: int, _h: int, _freed: bool, _canTele: bool, _known: bool, _treasure: int, _agent: int, _pirate: int, _prevMove: int, _removed: set, _hints: list, _map: list, _prev: list):
    if _known and _treasure == _agent:
        return (0, "large scan", _agent)
    elif _known and _canTele:
        return (0, "teleport", _treasure)
    elif not _freed:
        return getBestAction(_agent, _w, _h, _hints, _removed, _map)
    else:
        if _canTele: return (0, "teleport", _pirate)
        if _pirate == _prevMove: return (0, "large scan", _agent)
        
        tiles = []
        inRangeOfPirate = []
        xPi = _pirate // _w
        yPi = _pirate % _w
        if _pirate - _prevMove in [1, 2]: # move right
            for x in range(_h):
                for y in range(yPi, _w):
                    if x * _w + y not in _removed:
                        tiles.append(x * _w + y)
                        if (x - xPi, y - yPi) in [(2, 0), (1, 1), (0, 2), (1, 0), (0, 1), (-1, 0), (-2, 0), (-1, 1)]:
                            inRangeOfPirate.append(x + _w + y)
        if _pirate - _prevMove in [-1, -2]: # move left
            for x in range(_h):
                for y in range(yPi + 1):
                    if x * _w + y not in _removed:
                        tiles.append(x * _w + y)
                        if (x - xPi, y - yPi) in [(2, 0), (1, -1), (0, 2), (1, 0), (0, -1), (-1, 0), (-2, 0), (-1, -1)]:
                            inRangeOfPirate.append(x + _w + y)
        if _pirate - _prevMove in [_w, 2*_w]: # move up
            for x in range(xPi + 1):
                for y in range(_w):
                    if x * _w + y not in _removed:
                        tiles.append(x * _w + y)
                        if (x - xPi, y - yPi) in [(-2, 0), (-1, 1), (0, 2), (-1, -1), (0, -2), (-1, 0), (0, 1), (0, -1)]:
                            inRangeOfPirate.append(x + _w + y)
        if _pirate - _prevMove in [-_w, -2*_w]: # move down
            for x in range(xPi, _h):
                for y in range(_w):
                    if x * _w + y not in _removed:
                        tiles.append(x * _w + y)
                        if (x - xPi, y - yPi) in [(2, 0), (1, 1), (0, 2), (1, -1), (0, -2), (1, 0), (0, 1), (0, -1)]:
                            inRangeOfPirate.append(x + _w + y)
        if _pirate - _prevMove == _w - 1: # down left
            for x in range(xPi, _h):
                for y in range(yPi + 1):
                    if x * _w + y not in _removed:
                        tiles.append(x * _w + y)
                        if (x - xPi, y - yPi) in [(2, 0), (0, -2), (1, 0), (0, -1), (1, -1)]:
                            inRangeOfPirate.append(x + _w + y)
        if _pirate - _prevMove == _w + 1: # down right
            for x in range(xPi, _h):
                for y in range(yPi, _w):
                    if x * _w + y not in _removed:
                        tiles.append(x * _w + y)
                        if (x - xPi, y - yPi) in [(2, 0), (0, 2), (1, 0), (0, 1), (1, 1)]:
                            inRangeOfPirate.append(x + _w + y)
        if _pirate - _prevMove == -_w - 1: # up left
            for x in range(xPi + 1):
                for y in range(yPi + 1):
                    if x * _w + y not in _removed:
                        tiles.append(x * _w + y)
                        if (x - xPi, y - yPi) in [(-2, 0), (0, -2), (-1, 0), (0, -1), (-1, -1)]:
                            inRangeOfPirate.append(x + _w + y)
        if _pirate - _prevMove == -_w + 1: # up right
            for x in range(xPi + 1):
                for y in range(yPi + 1):
                    if x * _w + y not in _removed:
                        tiles.append(x * _w + y)
                        if (x - xPi, y - yPi) in [(-2, 0), (0, 2), (-1, 0), (0, 1), (-1, 1)]:
                            inRangeOfPirate.append(x + _w + y)
        
        for i in range(_w * _h):
            if i not in tiles and i != _treasure:
                _removed.add(i)
        
        return getBestAction(_agent, _w, _h, _hints, _removed, _map)