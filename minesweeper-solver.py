"""
Minesweeper Solver AI 
This algorithm uses a top-down approach to solve the Minesweeper game.
"""

class MinesweeperSolver:
    def __init__(self, board, buttons, rows, cols, mine_positions):
        self.board = board
        self.buttons = buttons
        self.rows = rows
        self.cols = cols
        self.mine_positions = mine_positions
        self.known_mines = set()
        self.known_safe = set()

    "get all valid neighboring cells of a given cell."
    def get_neighbors(self, row, col): 
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    neighbors.append((r, c))
        return neighbors

    "get the unrevealed neighboring cells of a given cell."
    def get_unrevealed_neighbors(self, row, col):
        neighbors = self.get_neighbors(row, col)
        result = []
        for n in neighbors:
            if self.buttons[n]["state"] == "normal":
                result.append(n)
        return result

    def get_flagged_neighbors(self, row, col):
        neighbors = self.get_neighbors(row, col)
        result = []
        for n in neighbors:
            if self.buttons[n].cget["text"] == "FLAG":
                result.append(n)
        return result

    def analyze_cell(self,row, col):
        