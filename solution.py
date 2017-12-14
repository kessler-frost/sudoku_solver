assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'


def assign_value(values, box, value):
    """
    Use this function to update the values dictionary.
    Assigns a value to a given box.
    """

    # Not wasting memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def common_peers(values, ntwinpair):
    # Function to find the common peers of a naked twin pair
    cpeers = []
    for p1 in peers[ntwinpair[0]]:
        if p1 in peers[ntwinpair[1]]:
            cpeers.append(p1)
    return cpeers

def naked_twins(values):
    """Eliminating values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # This finds the list of all naked twin pairs and store them in a nested list 'ntw'
    ntw = [[box,p] for box in values.keys() if len(values[box])==2 for p in peers[box] if len(values[p])==2 and (values[box] in values[p])]

    # This takes care of elimination of possibilities from their common peers
    for ntwinpair in ntw:
        for st in values[ntwinpair[0]]:
            for p in common_peers(values, ntwinpair):
                if st in values[p]:
                    values = assign_value(values, p, values[p].replace(st, ''))

    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows,cols)
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
"""
This part is for the addition of diagonal sudoku's solution
"""
diagonal_units1 = []
diagonal_units2 = []
diagonal_units_all = []
i=0
for r in row_units:
    diagonal_units1.append(r[i])
    diagonal_units2.append(r[-i-1])
    i+=1
diagonal_units_all.append(diagonal_units1)
diagonal_units_all.append(diagonal_units2)

unitlist = row_units + col_units + square_units + diagonal_units_all
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def grid_values(grid):
    """
    Converts grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for v in grid:
        if v in digits:
            chars.append(v)
        if v=='.':
            chars.append(digits)
    assert len(chars)==81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    
    # Elimination of solved values from it's peer boxes
    
    solved_boxes = [box for box in values.keys() if len(values[box])==1]

    for box in solved_boxes:
        digit = values[box]
        for p in peers[box]:
            if digit in values[p]:
                values = assign_value(values, p, values[p].replace(digit, ''))
    return values

def only_choice(values):
    
    # Elimination of possibilities by assigning the only possible choice for a box
    
    for unit in unitlist:
        for digit in '123456789':
            digit_places = [box for box in unit if digit in values[box]]
            if len(digit_places)==1:
                values = assign_value(values, digit_places[0], digit)
    return values

def reduce_puzzle(values):
    
    # Reducing the whole puzzle by various strategies
    
    stalled  = False

    while not stalled:
        solved_before = len([box for box in values.keys() if len(values[box])==1])
        values = eliminate(values)
        values = only_choice(values)
        
        # Here the naked twins elimination strategy has been implemented
        
        values = naked_twins(values)
        solved_after = len([box for box in values.keys() if len(values[box])==1])
        stalled = solved_before==solved_after
        if len([box for box in values.keys() if len(values[box])==0]):
            return False

    return values

def search(values):

    values = reduce_puzzle(values)
    if values is False:
        return False

    if all(len(values[box]) == 1 for box in boxes):
        return values

    l,m = min((len(values[m]), m) for m in boxes if len(values[m]) > 1)

    for v in values[m]:
        new_values = values.copy()
        new_values[m] = v
        final_values = search(new_values)
        if final_values:
            return final_values

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    return search(grid_values(grid))


if __name__ == '__main__':
    
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    
    #Insert any custom diagonal sudoku grid as :-
    #diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('Could not visualize your board due to a pygame issue. Not a problem, the solution is already printed.')
