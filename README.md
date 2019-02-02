# sudokusolver

This sudokkusolver could apply on easy, medium, hard level.

* In the game of Sudoku, you are given a partially-filled 9 x 9 grid, grouped into a 3 x 3 grid of 3 x 3 blocks. 

* The objective is to fill each square with a digit from 1 to 9, subject to the requirement that each row, column, and block must contain each digit exactly once.

* I will implement the AC-3 constraint satisfaction algorithm for Sudoku, along with two extensions that will combine to form a complete and efficient solver.

       Function infer_ac3(self) that runs the AC-3 algorithm on the current board to narrow down each cell's set of values as much as possible. 
       Although this will not be powerful enough to solve all Sudoku problems, it will produce a solution for easy-difficulty puzzles
