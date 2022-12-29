import random

def preprocessing(_w: int, _h: int, _treasure: int, _map: list):
    """
    Args:
        _w (int): The width of map.
        _h (int): The height of map.
        _treasure (int): Location of the treasure.
        _map (list): The map of game.
        
    Return:
        Locations of player and pirate.
    """
    agent = random.randrange(_w * _h)
    
    while _map[agent // _w][agent % _w] == "0" or len(_map[agent // _w][agent % _w]) > 1:
        agent = random.randrange(_w * _h)
    
    pirates = []
    for i in range(_h):
        for j in range(_w):
            if "P" in _map[i][j]:
                pirates.append(i * _w + j)
                
    random.shuffle(pirates)
    for pirate in pirates:
        queue = [[pirate]]
        explored = [pirate]
        
        while queue:
            path = queue.pop(0)
            
            if path[-1] == _treasure: return (agent, pirate, path[::2] + ([path[-1]] if len(path) % 2 == 0 else []))
            
            # check = [False] * 4
            adjacent = [-1, 1, -_w, _w]
            for i in range(4):
                cell = path[-1] + adjacent[i]
                if cell < 0 or cell >= _w * _h: continue
                if cell in explored: continue
                if 'M' in _map[cell // _w][cell % _w] or '0' in _map[cell // _w][cell % _w]: continue
                
                queue.append(path + [cell])
                explored.append(cell)
                
    return (agent, -1, [])