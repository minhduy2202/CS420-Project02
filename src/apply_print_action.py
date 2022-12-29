def applyPrintAction(_action: tuple, _removed: set, _w: int, _h: int):
    if _action[1] == "teleport":
        agent = _action[2]
        print(f"Teleport to {(agent // _w, agent % _w)}")
    if _action[1] == "move":
        print(f"Move from {(agent // _w, agent % _w)} to location {((agent + _action[2]) // _w, (agent + _action[2]) % _w)}")
        agent += _action[2]
    if _action[1] == "move and small scan":
        print(f"Move from {(agent // _w, agent % _w)} to location {((agent + _action[2]) // _w, (agent + _action[2]) % _w)} and scan 3x3 area.")
        agent += _action[2]
        for i in range(agent // _w - 1, agent // _w + 2):
            for j in range(agent % _w - 1, agent % _w + 2):
                if 0 <= i < _h and 0 <= j < _w and i * _h + j not in _removed:
                    _removed.add(i * _w + j)
    if _action[1] == "large scan":
        for i in range(agent // _w - 2, agent // _w + 3):
            for j in range(agent % _w - 2, agent % _w + 3):
                if 0 <= i < _h and 0 <= j < _w and i * _h + j not in _removed:
                    _removed.add(i * _w + j)