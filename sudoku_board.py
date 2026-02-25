from typing import Tuple
import clingo


class Sudoku:
    def __init__(self, sudoku: dict[Tuple[int, int], int]):
        self.sudoku = sudoku

    def __str__(self) -> str:
        s = ""
        for row in range(1, 10):
            for col in range(1, 10):
                value = self.sudoku[(row, col)]
                s += str(value)
                if col < 9:
                    if col % 3 == 0:
                        s += "  " 
                    else:
                        s += " "  
            s += "\n"
            if row % 3 == 0 and row < 9:
                s += "\n"

        return s

    @classmethod
    def from_str(cls, s: str) -> "Sudoku":
        sudoku = {}
        lines = [line for line in s.strip().split('\n') if line.strip() != '']
        for row_idx, line in enumerate(lines, start = 1):
            tokens = line.split()
            for col_idx, token in enumerate(tokens, start = 1):
                if token != '-':
                    sudoku[(row_idx, col_idx)] = int(token)
        return cls(sudoku)

    @classmethod
    def from_model(cls, model: clingo.solving.Model) -> "Sudoku":
        sudoku = {}
        for symbol in model.symbols(shown=True):
            if symbol.name == 'sudoku':
                row   = symbol.arguments[0].number
                col   = symbol.arguments[1].number
                value = symbol.arguments[2].number
                sudoku[(row, col)] = value
        return cls(sudoku)
