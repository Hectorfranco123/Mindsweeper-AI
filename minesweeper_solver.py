"""
Minesweeper Solver AI 
This algorithm uses a top-down approach to solve the Minesweeper game. Along with Constraint Satisfaction 
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
            button = self.buttons[n]
            if button["state"] == "normal" and button.cget("text") != "FLAG":
                result.append(n)
        # print(f"Cell ({row},{col}) has {len(result)} unrevealed neighbors")
        return result

    "get the flagged neighboring cells of a given cell."
    def get_flagged_neighbors(self, row, col):
        neighbors = self.get_neighbors(row, col)
        result = []
        for n in neighbors:
            if self.buttons[n].cget("text") == "FLAG":
                result.append(n)
        return result
    "check a cell to find safe cells or mines."
    def analyze_cell(self, row, col):
        button = self.buttons[(row, col)]

        #print(f"Analyzing cell ({row}, {col})")

        #only check revealed cells
        if button["state"] != "disabled":
            return set(), set(), set() #no new info
        if button.cget("text") == "" or button.cget("text") == "FLAG":  # Skip empty/flagged
            return set(), set(), set() #no new info
        try:
            cell_value = int(button.cget("text"))
        except (ValueError, tk.TclError):
            return set(), set(), set() #not a number is retruned and prevents crash

        unrevealed = set(self.get_unrevealed_neighbors(row, col))
        flagged = set(self.get_flagged_neighbors(row, col))

        cells_checked = unrevealed.copy() #track cells we analyze


        #rule 1: if number of flagged neighbors = cell value, all other neighbors are safe
        if len(flagged) == cell_value:
            safe_cells = unrevealed - flagged
            return safe_cells, set(), cells_checked

        #rule 2: if flagged + unrevealed = cell value, all unrevealed are mines
        if len(unrevealed) + len(flagged) == cell_value:
            mine_cells = unrevealed
            return set(), mine_cells, cells_checked

        #test for solver logic
        # if len(flagged) == cell_value:
        #     safe_cells = unrevealed - flagged
        #     print(f"Found {len(safe_cells)} safe cells from rule 1")
        #     return safe_cells, set(), cells_checked


        return set(), set(), cells_checked

    "finds the next move based on current knowledge."
    def find_move(self):
        """
        returns: (move_type, cells, checked_cells)
        move_type: "safe" or "mine" or None
        cells: set of cells that are safe or mines
        checked_cells: dict of cells that were analyzed
        """
        all_safe = set()
        all_mines = set()
        checked_cells = {} #dict to track checked cells

        #check all revealed cells
        for r in range(self.rows):
            for c in range(self.cols):
                safe, mines, checked = self.analyze_cell(r, c)

                if safe or mines:
                    checked_cells[(r, c)] = checked
                
                all_safe.update(safe)
                all_mines.update(mines)
        
        if all_safe:
            return "safe", all_safe, checked_cells
        if all_mines:
            return "mine", all_mines, checked_cells

        #trying the advance method
        move_type, cells, checked_cells = self.find_advanced_move()
        if move_type:
            return move_type, cells, checked_cells

        return None, set(), checked_cells

    #Finding move using multiple cells - Constraint Satisfaction 
    def find_advanced_move(self):
        constraints = []


        for r in range(self.rows):
            for c in range(self.cols):
                button = self.buttons[(r,c)]
                if button["state"] != "disabled":#skip disabled cells
                    continue
                if button.cget("text") == "" or button.cget("text") == "FLAG":  # Skip empty/flagged
                    continue

                try: cell_value = int(button.cget("text"))
                except (ValueError, tk.TclError):
                    continue


                unrevealed = set(self.get_unrevealed_neighbors(r,c))
                flagged = set(self.get_flagged_neighbors(r,c))

                if unrevealed: #only add if there unreveaaled neeighbors
                    remaining_mines = cell_value - len(flagged)
                    constraints.append((unrevealed, remaining_mines))
        # print(f"Total constraints found: {len(constraints)}")
        # print(f"Constraints: {constraints}")

        for i in range(len(constraints)):
            cells1, mines1 = constraints[i]

            for j in range(len(constraints)):
                cells2, mines2 = constraints[j]

                #dont compare the same or reversed pairs

                if i >= j:
                    continue

                #check if cells1 in cells2
                is_subset = True
                for cell in cells1:
                    if cell not in cells2:
                        is_subset = False
                        break

                if is_subset:
                    #find difference (cells in cells2 but not cells1)
                    diff_cells = set()

                    for cell in cells2:
                        if cell not in cells1:
                            diff_cells.add(cell)

                    diff_mines = mines2 - mines1

                    #if all those extra cells must be mines 
                    if diff_mines == len(diff_cells) and len(diff_cells) >0:
                        return "mine", diff_cells, {}

                    #if all those extra cells must be safe
                    if diff_mines == 0 and len(diff_cells) > 0:
                        return "safe", diff_cells, {}

        return None, set(), {} #if nothing found


    def get_random_safe_cell(self):
        """
        When no logical move exists, pick a random unrevealed cell
        """
        unrevealed = []
        for r in range(self.rows):
            for c in range(self.cols):
                button = self.buttons[(r, c)]
                if button["state"] == "normal" and button.cget("text") != "FLAG":
                    unrevealed.append((r, c))

        print(f"Making random guess. Unrevealed cells remaining: {len(unrevealed)}")
        
        if unrevealed:
            return random.choice(unrevealed)
        return None

import random
import tkinter as tk