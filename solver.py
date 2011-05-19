# decorator to clone a board so we're not modifying arguments
def clone_board(func):
    def decorated(board): return func(board.clone())
    return decorated

@clone_board
def solve(board):
    remaining_tries = 2
    while remaining_tries > 0:
        changed = False
        for strat in [do_fill_single,do_blocking,do_enumeration]:
            board,changed = strat(board)
            if changed: remaining_tries = 2
        if not changed: remaining_tries -= 1
    return board

@clone_board
def do_fill_single(board):
    """ Fills in all spaces that are part of a struct with only one open space. """
    for struct in filter(lambda x: x.open_count() == 1,board.structs):
        space = struct.open_spaces()[0]
        val = struct.open_values().pop()
        board.replace(space,val)
        return board,True
    return board,False

@clone_board
def do_enumeration(board):
    """ Strategies that involve enumerating through all possibilities in a struct.

    We go through the structs (in ascending order by the number of open spaces
    they have) and fill in any spaces where one of the following is true:
    
    1. There is only one possibile value for that space
    2. The space can contain a value that can't fit into any of the other spaces
    """
    # start with the structs with the fewest open spaces
    for struct in sorted(board.structs,key=lambda x: x.open_count()):
        val_map = {val: [] for val in struct.open_values()}
        # enumerate possibilities in a space:
        # fill in any space where there's only 1 possible value
        for space in struct.open_spaces():
            vals = space.possible_values()
            if len(vals) == 1:
                val = vals.pop()
                board.replace(space,val)
                # if we change something, fill it in and move on
                return board,True
            for val in vals: val_map[val].append(space)
        # enumerate values: all of the values must be in this struct,
        # so if there's only one place a value can go, it must go there
        for val,spaces in val_map.items():
            if len(spaces) == 1:
                board.replace(spaces[0],val)
                return board,True
            # also, if the only possibilities for a given value in a box are in
            # a line, we can use that information later for blocking...
            elif struct.is_box():
                if len(set([s.row_num for s in spaces])) == 1:
                    spaces[0].row.block_on(val,spaces)
                elif len(set([s.col_num for s in spaces])) == 1:
                    spaces[0].col.block_on(val,spaces)
    return board,False

@clone_board
def do_blocking(board):
    """ Strategies that involve blocking off places on the board.

    To execute this strategy, we pick a number, and block off all of the rows,
    columns, and boxes that number appears in. Then, if there are any rows,
    columns, or boxes with only 1 unblocked space, we can fill them in.

    To fully execute this strategy, we continue doing this until we've filled
    in all of the spaces we can for all of the numbers.
    """
    done = False
    for i in range(1,10):
        blocked = board.block(i)
        for struct in blocked.structs:
            if struct.open_count() == 1:
                space = struct.open_spaces()[0]
                board.replace(space,i)
                return board,True
    return board,False

