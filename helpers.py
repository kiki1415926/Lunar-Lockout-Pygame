from search import *  # for search engines
from lunarlockout import LunarLockoutState, Direction, \
    lockout_goal_state  # for LunarLockout specific classes and problems


def all_pos_can_move(chess_pos: tuple, state):
    """
    >>> state = LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((0, 1),))
    >>> all_pos_can_move((0, 1), state)
    [(0, 3)]
    """
    result = []
    all_chess = state.xanadus + state.robots
    x = chess_pos[0]
    while x - 1 >= 0 and (x-1, chess_pos[1]) not in all_chess:
        x -= 1
    if x - 1 >= 0 and (x, chess_pos[1]) != chess_pos:
        result.append((x, chess_pos[1]))
    x = chess_pos[0]
    while x + 1 < state.width and (x + 1, chess_pos[1]) not in all_chess:
        x += 1
    if x + 1 < state.width and (x, chess_pos[1]) != chess_pos:
        result.append((x, chess_pos[1]))
    y = chess_pos[1]
    while y + 1 < state.width and (chess_pos[0], y+1) not in all_chess:
        y += 1
    if y + 1 < state.width and (chess_pos[0], y) != chess_pos:
        result.append((chess_pos[0], y))
    y = chess_pos[1]
    while y - 1 >= 0 and (chess_pos[0], y-1) not in all_chess:
        y -= 1
    if y - 1 >= 0 and (chess_pos[0], y) != chess_pos:
        result.append((chess_pos[0], y))
    return result

if __name__=='__main__':
    import doctest
    doctest.testmod(verbose=True)
