import sys
from clingo import Application, clingo_main, Model
from typing import Callable



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

class SudokuSolver(Application):

    def __init__(self):
        self.program_name = "sudoku"

    
    def print_model(self, model: Model, printer: Callable[[], None]) -> None:
        print("{}".format(" ".join(str(s) for s in sorted(model.symbols(shown=True)))))
        sys.stdout.flush()

    def main(self, ctl, files):
        ctl.add("base", [], SUDOKU_ENCODING)

        for f in files:
            ctl.load(f)

        ctl.ground([("base", [])], [])
        ctl.solve()



if __name__ == "__main__":
    clingo_main(SudokuSolver())
    


