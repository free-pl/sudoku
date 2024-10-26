# Sudoku Trainer - my 2024 A-Level NEA

The primary goal of this project was to create a Sudoku game with Python which solves some of the computational issues associated with the puzzle, namely puzzle generation and automated solving/verifying of puzzles. To accompany this, I also hosted a database server using SSMS to allow users to save and access their game data from any device or location, though this is no longer running since it only served as a proof of concept.


## Knowledge representation

To be able to work with the puzzles, I first had to create suitable data types in which they could be represented. The file _knowledge.py_ contains two classes. _Knowledge_ is a simple class, with an object representing a single cell in the puzzle and the potential values (candidates) it could be. They can be checked for equality, which is useful in other functionalities, and the candidates can be reduced as more information is revealed about the puzzle. _Puzzle_ is slightly more complex since it represents an entire puzzle. The constructor method takes in a 2D list and uses that to represent the puzzle in all useful forms (split by row/column/block) and create an initial knowledge base of _Knowledge_ objects, which is updated further as values are inserted using the _addValue()_ method.


## Creating a puzzle solver

Part of the scope of this project was to create an "AI helper" which could help the user with a puzzle by giving partial solutions, in addition to verifying that puzzles are solvable at a certain skill level (useful for puzzle generation). I did this by implementing the _SudokuAI_ class in _ai.py_ which contains methods to search for and resolve predictable patterns in a given puzzle, in addition to being able to make a single move on the puzzle (i.e., inserting a single value) or solve the entire puzzle to verify that there is a unique solution. Breaking down the class into individual patterns to search for means that it can give more specific help to the user by describing the patterns used for a partial solution. Whilst there are faster methods to verify a puzzle such as brute force, they lack the ability to give partial solutions in greater detail and to verify difficulty, given that a puzzle's difficulty is not always linked to the number of empty cells.


## Generating puzzles

Puzzles are difficult to generate at runtime due to the trade-off described above, so I instead generated a set of puzzle templates using the code in _generatePuzzle.py_, generating 100 templates of each difficulty from easy, medium and hard for a total of 300. A completed puzzle is first generated. This is done by doing a circular shift on a random list of numbers 1-9 and further rearranging rows and columns to abstract the pattern. A random amount of values are then removed from the puzzle. After a certain number of values have been removed, the _SudokuAI_ attempts to solve the puzzle in that state; the program continues with this puzzle only if it can be solved at the given difficulty, and the puzzle is discarded if a solution is not found or if it is solved at a different difficulty level. Once that puzzle is verified, the template is created by assigning each number to a character and storing a string of 81 characters in a text file, which are all included in the repository.

The idea of using templates is that there are a series of transformations that can be applied at random to create many different puzzles from the same template, hence using less storage than a bank of complete puzzles, and less time/memory than generating an entirely new puzzle at runtime. See the below calculations for how many puzzles can be obtained per template:
9! ways to assign numbers 1-9 to letters a-i = 362,880
*4 since there are 4 orientations of the entire puzzle (rotate by 90 degrees) = 1,451,520
*3^2 since the 3x3 blocks can be shifted 0-2 times both horizontally and vertically = 13,063,680
*2 since the puzzle can also be reflected = 26,127,360 puzzles per template
*300 = 7,838,208,000 puzzles total from all 300 tempaltes

Because these transformations still preserve the patterns that were used to solve the puzzle, any transformation will theoretically remain solvable.
