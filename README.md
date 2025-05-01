    # Ultimate Tic-Tac-Toe

Ultimate Tic-Tac-Toe is an advanced version of the classic Tic-Tac-Toe game. It consists of a 3x3 grid of smaller Tic-Tac-Toe boards, where the goal is to win three small boards in a row, column, or diagonal to win the game.

## Features
- Implements the rules of Ultimate Tic-Tac-Toe.
- AI opponent using the Minimax algorithm with alpha-beta pruning.
- Supports human vs AI gameplay.

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/mahdiahmadi87/ultimate-tic-tac-toe.git
   ```
2. Navigate to the project directory:
   ```bash
   cd ultimate-tic-tac-toe
   ```
3. Run the program:
   ```bash
   python minimax.py
   ```

## Input Format
- Provide a 9x9 grid as input, where each cell is either `X`, `O`, or `.` (empty).
- Specify the next small board to play in using two integers (row and column indices).

Example input:
```
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
-1 -1
```

## Output
- The program outputs the best move for the AI in the format:
  ```
  big_row big_col small_row small_col
  ```
  If no move is possible, it outputs:
  ```
  -1 -1 -1 -1
  ```

## Dependencies
- Python 3.x

## License
This project is licensed under the MIT License.