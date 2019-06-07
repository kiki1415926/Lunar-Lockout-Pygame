# Look for #IMPLEMENT tags in this file. These tags indicate what has
# to be implemented to complete the LunarLockout  domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

# import os for time functions
from search import *  # for search engines
from lunarlockout import LunarLockoutState, Direction, \
    lockout_goal_state  # for LunarLockout specific classes and problems


# LunarLockout HEURISTICS
def heur_trivial(state):
    '''trivial admissible LunarLockout heuristic'''
    '''INPUT: a LunarLockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    return 0


def heur_manhattan_distance(state):
    # OPTIONAL
    '''Manhattan distance LunarLockout heuristic'''
    '''INPUT: a lunar lockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # Write a heuristic function that uses Manhattan distance to estimate distance between the current state and the goal.
    # Your function should return a sum of the Manhattan distances between each xanadu and the escape hatch.
    all_xanadus = state.xanadus
    center = int((state.width - 1) / 2)
    result = 0
    for xanadus in all_xanadus:
        result += distance(xanadus, (center, center))
    return result


def heur_L_distance(state):
    # IMPLEMENT
    '''L distance LunarLockout heuristic'''
    '''INPUT: a lunar lockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # Write a heuristic function that uses mahnattan distance to estimate distance between the current state and the goal.
    # Your function should return a sum of the L distances between each xanadu and the escape hatch.
    sum_distance = 0
    center = int((state.width - 1) / 2)
    if isinstance(state.xanadus[0], int):
        if state.xanadus[0] != center:
            sum_distance += 1
        if state.xanadus[1] != center:
            sum_distance += 1
    else:
        for robot in state.xanadus:
            tmp = list(robot)
            if tmp[0] != center:
                sum_distance += 1
            if tmp[1] != center:
                sum_distance += 1
    return sum_distance


def heur_alternate(state):
    # IMPLEMENT
    '''a better lunar lockout heuristic'''
    '''INPUT: a lunar lockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # Your function should return a numeric value for the estimate of the distance to the goal.
    # We start with the estimate cost we calculate using heur_L_distance.
    result = heur_L_distance(state)
    center = int((state.width - 1) / 2)
    all_chess = state.xanadus + state.robots
    row_positions = [chess[0] for chess in all_chess]
    col_positions = [chess[1] for chess in all_chess]
    largeRow = max(row_positions)
    smallRow = min(row_positions)
    largeCol = max(col_positions)
    smallCol = min(col_positions)
    for xanadus in state.xanadus:
        # For the dead states, add a pretty large number to the heuristic. Dead states includes xanadus's x value larger
        # or smaller than all other pieces and y value larger or smaller than all other pieces.
        if (xanadus[0] == largeRow or xanadus[0] == smallRow) and (xanadus[1] == largeCol or xanadus[1] == smallCol):
            return 9999999
        # When the xanadus is at (center, center), then it is at the escape hatch and was removed.
        if xanadus == (center, center):
            result -= 1
        # When there is no other piece in the same column or row, it needs helper robots to help it move.
        if row_positions.count(xanadus[0]) == 1:
            result += 1
        elif col_positions.count(xanadus[1]) == 1:
            result += 1
    # When there is a robots at the escape hatch, no xanadus can escape, so we need to move it.
    if (center, center) in state.robots:
        result += 1
    return result

def distance(position_one: tuple, position_two: tuple):
    """
    Return the distance between position_one and position_two.
    """
    return abs(position_one[0] - position_two[0]) + abs(position_one[1] - position_two[1])


def fval_function(sN, weight):
    # IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a LunarLockoutState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """

    # Many searches will explore nodes (or states) that are ordered by their f-value.
    # For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    # You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    # The function must return a numeric f-value.
    # The value will determine your state's position on the Frontier list during a 'custom' search.
    # You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return sN.gval + weight * sN.hval


def anytime_weighted_astar(initial_state, heur_fn, weight=4., timebound=2):
    # IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a lunar lockout state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    se = SearchEngine('custom')
    se.init_search(initial_state, goal_fn=lockout_goal_state, heur_fn=heur_fn,
                   fval_function=(lambda sN: fval_function(sN, weight)))
    final = se.search(timebound)
    return final


def anytime_gbfs(initial_state, heur_fn, timebound=2):
    # OPTIONAL
    '''Provides an implementation of anytime greedy best-first search.  This iteratively uses greedy best first search,'''
    '''At each iteration, however, a cost bound is enforced.  At each iteration the cost of the current "best" solution'''
    '''is used to set the cost bound for the next iteration.  Only paths within the cost bound are considered at each iteration.'''
    '''INPUT: a lunar lockout state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    se = SearchEngine('best_first')
    se.init_search(initial_state, goal_fn=lockout_goal_state, heur_fn=heur_fn,
                   fval_function=(lambda sN: fval_function(sN, weight)))
    final = se.search(timebound)
    return final


PROBLEMS = (
    # 5x5 boards: all are solveable
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((0, 1),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((0, 2),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((0, 3),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((1, 1),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((1, 2),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((1, 3),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((1, 4),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((2, 0),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((2, 1),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (0, 2), (0, 4), (2, 0), (4, 0)), ((4, 4),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((4, 0),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((4, 1),)),
    LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((4, 3),)),
    # 7x7 BOARDS: all are solveable
    LunarLockoutState("START", 0, None, 7, ((4, 2), (1, 3), (6, 3), (5, 4)), ((6, 2),)),
    LunarLockoutState("START", 0, None, 7, ((2, 1), (4, 2), (2, 6)), ((4, 6),)),
    LunarLockoutState("START", 0, None, 7, ((2, 1), (3, 1), (4, 1), (2, 6), (4, 6)), ((2, 0), (3, 0), (4, 0))),
    LunarLockoutState("START", 0, None, 7, ((1, 2), (0, 2), (2, 3), (4, 4), (2, 5)), ((2, 4), (3, 1), (4, 0))),
    LunarLockoutState("START", 0, None, 7, ((3, 2), (0, 2), (3, 3), (4, 4), (2, 5)), ((1, 2), (3, 0), (4, 0))),
    LunarLockoutState("START", 0, None, 7, ((3, 1), (0, 2), (3, 3), (4, 4), (2, 5)), ((1, 2), (3, 0), (4, 0))),
    LunarLockoutState("START", 0, None, 7, ((2, 1), (0, 2), (1, 2), (6, 4), (2, 5)), ((2, 0), (3, 0), (4, 0))),
)

if __name__ == "__main__":

    # TEST CODE
    solved = 0;
    unsolved = [];
    counter = 0;
    percent = 0;
    timebound = 2;  # 2 second time limit for each problem
    print("*************************************")
    print("Running A-star")

    for i in range(len(
            PROBLEMS)):  # note that there are 40 problems in the set that has been provided.  We just run through 10 here for illustration.

        print("*************************************")
        print("PROBLEM {}".format(i))

        s0 = PROBLEMS[i]  # Problems will get harder as i gets bigger

        print("*******RUNNING A STAR*******")
        se = SearchEngine('astar', 'full')
        se.init_search(s0, lockout_goal_state, heur_alternate)
        final = se.search(timebound)

        if final:
            final.print_path()
            solved += 1
        else:
            unsolved.append(i)
        counter += 1

    if counter > 0:
        percent = (solved / counter) * 100

    print("*************************************")
    print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("*************************************")

    solved = 0;
    unsolved = [];
    counter = 0;
    percent = 0;
    print("Running Anytime Weighted A-star")

    for i in range(len(PROBLEMS)):
        print("*************************************")
        print("PROBLEM {}".format(i))

        s0 = PROBLEMS[i]
        weight = 4
        final = anytime_weighted_astar(s0, heur_alternate, weight, timebound)

        if final:
            final.print_path()
            solved += 1
        else:
            unsolved.append(i)
        counter += 1

    if counter > 0:
        percent = (solved / counter) * 100

    print("*************************************")
    print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("*************************************")

    solved = 0;
    unsolved = [];
    counter = 0;
    percent = 0;
    print("Running Anytime GBFS")

    for i in range(len(PROBLEMS)):
        print("*************************************")
        print("PROBLEM {}".format(i))

        s0 = PROBLEMS[i]
        final = anytime_gbfs(s0, heur_alternate, timebound)

        if final:
            final.print_path()
            solved += 1
        else:
            unsolved.append(i)
        counter += 1

    if counter > 0:
        percent = (solved / counter) * 100

    print("*************************************")
    print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("*************************************")
