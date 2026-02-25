import sys
from clingo import Application, clingo_main, Model
from clingo.symbol import Symbol
from typing import Callable
from sudoku_board import Sudoku


SUDOKU_ENCODING = """
sudoku(R,C,V) :- initial(R,C,V).

{ sudoku(R,C,V) : V = 1..9 } = 1 :- R = 1..9, C = 1..9.

:- sudoku(R,C1,V), sudoku(R,C2,V), C1 != C2.

:- sudoku(R1,C,V), sudoku(R2,C,V), R1 != R2.

:- sudoku(R1,C1,V), sudoku(R2,C2,V),
   R1 != R2, C1 != C2,
   (R1-1)/3 == (R2-1)/3,
   (C1-1)/3 == (C2-1)/3.

#show sudoku/3.
"""
import clingo

class Context:

    def __init__(self, board: Sudoku):
        self.board = board
        
    def initial(self) -> list[Symbol]:
        result = []
        for (row, col), value in self.board.sudoku.items():
            symbol = clingo.Function("", [
                clingo.Number(row),
                clingo.Number(col),
                clingo.Number(value)
            ])
            result.append(symbol)
        return result


class SudokuSolver(Application):
    def __init__(self):
        self.program_name = "sudoku"

    def print_model(self, model: Model, printer: Callable[[], None]) -> None:
        sudoku = Sudoku.from_model(model)
        print(str(sudoku), end='')
        sys.stdout.flush()

    def main(self, ctl, files):
        with open(files[0], 'r') as f:
            content = f.read()

        board = Sudoku.from_str(content)
        context = Context(board)

        ctl.add("base", [], SUDOKU_ENCODING)
        ctl.load("sudoku_py.lp")
        ctl.ground([("base", [])], context)
        ctl.solve()

if __name__ == "__main__":
    clingo_main(SudokuSolver())
    


