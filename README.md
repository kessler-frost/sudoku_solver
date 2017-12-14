# Diagonal Sudoku Solver
This project solves a given Diagonal Sudoku and returns the resulting grid.

## Question 1 (Naked Twins)
Q: How did I use constraint propagation to solve the naked twins problem?  
A: First we create a new list containing all of the naked twins instances in the whole board. We do this by traversing through the values dictionary and choosing just those 'box' with peer 'p' which have their length as 2 and have both the same elements, then pairing them up in a nested list.
After we get this list, we traverse through each pair of naked twins (which might get repeated sometimes) and then start eliminating each element of the 'naked twin box' iteratively from the common peers of the 'naked twin pair'. If this is applied recursively then each of the recursive calls will eliminate more possibilities by generating more naked twins from the previous call.

## Question 2 (Diagonal Sudoku)
Q: How did I use constraint propagation to solve the diagonal sudoku problem?  
A: First we divide the diagonals in two lists 'diagonal1' and 'diagonal2'. Now while traversing through rows for each row 'r' in row units,  we have two 'box' one for each diagonal (except for the center one, which is common for both). Thus, we store that 'box' in the respective diagonal's list and continue our traversal and storing process. Once each list has 9 elements or all of the rows have been traversed, we will add both of these diagonals in 'units list'. By doing this, the addition will automatically be made to the list of peers of a particular box and the no. of units corresponding to a particular box.

### Installation

This project requires **Python 3**.

I recommend installing [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project and all of my other projects.

### Pygame

If you want to visualize the solution you will have to install Pygame from [here](http://www.pygame.org/download.shtml).

## Run

You need to write the whole diagonal sudoku grid, in 'solution.py' under __main__, in format :-
```
diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
```

After that just execute from terminal or cmd (considering you have Python 3 and all the dependencies installed):-

``` 
python solution.py 
```
