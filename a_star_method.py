import time
import random
# check if board is solvable
# solution
# random numbers


# /* Test Cases */
_goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
# _start_grid = [4, 0, 1, 5, 3, 2, 6, 7, 8]  # Harder Puzzle
_start_grid = [5, 4, 1, 0, 2, 8, 3, 6, 7]  # Given Grid
# _start_grid = [3, 0, 7, 2, 1, 5, 4, 6, 8]  # Super hard 31 moves
# _start_grid = [8, 6, 7, 2, 5, 4, 3, 0, 1]  # another hard puzzle
# _start_grid = [8, 1, 2, 0, 4, 3, 7, 6, 5] # not possible


# Node Data
class Node:
    def __init__(self, grid, parent, data, depth, cost):
        self.grid = grid  # current grid
        self.parent = parent
        self.data = data  # h
        self.depth = depth  # g
        self.cost = cost  # f


####################
# Helper Functions #
####################

def calc_g(depth):
    return depth + 1  # g(n) + 1


def calc_f(depth, data):
    return data + depth  # h(n) + g(n)


def calc_h(grid):
    goal = _goal
    node_dist = 0
    # out_of_place = 0

    for i in grid:
        node_dist += abs(grid.index(i) - goal.index(i))
        # out_of_place += 1

    return node_dist  # h(n) # + out_of_place


# Possible boards
def possible_boards(grid):
    index = grid.index(0)
    # print(index)
    arr = []
    # Top
    if index - 3 >= 0:
        arr.append(grid.index(grid[index - 3]))
    # Bottom
    if index + 3 <= 8:
        arr.append(grid.index(grid[index + 3]))
    # Left
    if index - 1 >= 0 and index % 3 != 0:
        arr.append(grid.index(grid[index - 1]))
    # Right
    if index + 1 <= 8 and index % 3 != 2:
        arr.append(grid.index(grid[index + 1]))
    # print(arr)
    zero = index
    results = []
    # print(index)
    for n_index in arr:
        n_list = []
        for n in grid:
            n_list.append(n)
        n_list[n_index], n_list[zero] = n_list[zero], n_list[n_index]  # grid swap
        results.append(n_list)
        n_list = []  # clear for next grid
    # print(results)

    return results


# checks if solved
def is_solved(current_grid):
    goal = _goal
    if current_grid == goal:
        return True
    return False


############
# Apply A* #
###########


def a_star(initial_grid):

    path = []
    solution = []
    visited = []
    init = Node(initial_grid, None, 0, 0, 0)  # Root
    path.append(init)

    nodes_no = 0

    while True:
        current_node = path[0]
        start_index = 0

        for i in range(len(path)):
            if path[i].cost < current_node.cost:
                current_node = path[i]
                start_index = i

        path.remove(path[start_index])
        visited.append(current_node)

        # check solved
        if is_solved(current_node.grid):
            # print("Solved")
            print(f"Start: {_start_grid}")
            print(f"Solved in: {current_node.depth} moves")
            print(f"Nodes #: {nodes_no}")
            print(f"Goal: {current_node.grid}")
            return solution  # data needed to be provided

        children = []
        moves = possible_boards(current_node.grid)  # grid possibilities

        for i in range(len(moves)):
            child = Node(moves[i], current_node, 0, calc_g(current_node.depth), 0)
            children.append(child)
            nodes_no += 1

        children_len = len(children)
        if children_len > 0:
            for child in children:
                seen = False

                for explored_child in visited:
                    if explored_child.grid == child.grid:
                        seen = True
                        break
                if seen:
                    continue

                child.data = calc_h(child.grid)  # find h(n)
                child.cost = calc_f(child.depth, child.data)  # find f(n)

                should_add_to_path = True
                for pending_child in path:
                    if pending_child.grid == child.grid:
                        should_add_to_path = False
                        break
                if should_add_to_path:
                    path.append(child)


# checks if gris is possible
def is_grid_possible(grid):
    inv_count = 0
    empty_square = -1
    for i in range(len(grid)):
        for j in range(i + 1, len(grid)):
            if grid[j] != empty_square and grid[i] != empty_square and grid[i] > grid[j]:
                inv_count += 1
    # if inv_count > 3: # try another method
    if inv_count % 2 == 0:
        print("Not solvable")
        return
    else:
        return a_star(grid)


# grid randomizer
def random_board(grid):
    random.shuffle(grid)
    print(grid)
    return is_grid_possible(grid)


if __name__ == '__main__':
    startTime = time.time()
    base_grid = _start_grid
    # is_solved(base_grid)
    a_star(base_grid)  # THis is the base problem being solved.
    # is_grid_possible(base_grid)  # This take a grid and checks to see if its solvable and if so it solves it
    # random_board(base_grid)  # Randomizes the array input and runs it through the checker and runs it after
    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(executionTime))

    #######################################
    # side note the random board seems to #
    # generate a lot of bad boards and I  #
    # could not tell if this was due to   #
    # how I checked if it was solvable    #
    # or if truly that many boards are    #
    # not possible.                       #
    #######################################
