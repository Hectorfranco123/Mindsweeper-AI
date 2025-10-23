import tkinter as tk
from tkinter import simpledialog, messagebox
import random

root = tk.Tk()
root.title("minesweeper")

#ask user for size
size = simpledialog.askinteger("Board size","Enter Number: ")
#if user just doesnt for some reason 
if size is None:
    size = 10

#board size 
rows = cols = size 
num_mines = (rows * cols) // 6 #1/6 of board are mines

buttons = {} #button widgets
board =[] #2d list of buttons to store the game, named board 
mine_positions = set() #keep track of where mines are

game_over = False 
first_click = True

def make_board():
    global board
    board =[]
    for r in range(rows):
        row = []
        for c in range(cols):
            col = []
            row.append(0)
        board.append(row)

#make board with zeros
for r in range(rows):
    row = [] 
    for c in range(cols):
        row.append(0)
    board.append(row)


def reset_board():
    global mine_positions, game_over, first_click


    first_click = True
    game_over = False 
    mine_positions= set()
    make_board()
    for button in buttons.values():
        button.config(text="", relief=tk.RAISED, state="normal", bg="SystemButtonFace")

def check_win():
    global game_over

    #see how many cells are left
    unrevealed_count= 0
    for button in buttons.values():
        if button["state"]=="normal":
            unrevealed_count += 1

    #if unrevealed count = to number of mines they win 
    if unrevealed_count == num_mines:
        game_over = True
        messagebox.showinfo("You win! :)", "All mines have been found!")
        for button in buttons.value():
            button.config(state="disabled")

    

def place_mines(exclude_row,exclude_col):
    global mine_positions #use predetermined variable 
    mine_positions = set()

    #clear any exsiting mines
    for r in range(rows):
        for c in range(cols):
            board[r][c] = 0

    #place mines but not in clicked cell and around it
    excluded_cells = set()
    excluded_cells.add((exclude_row, exclude_col))
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            nr, nc = exclude_row + dr, exclude_col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                excluded_cells.add((nr, nc))
    
    while len(mine_positions) < num_mines:
        r = random.randint(0,rows -1)
        c = random.randint(0, cols -1)
        if (r,c) not in mine_positions and (r,c) not in excluded_cells:
            mine_positions.add((r,c))
            board[r][c] = -1 #-1 means mine is located here
    
    #After mines are made, update surounding cells to count near mines
    for r,c in mine_positions:
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != -1:
                    board[nr][nc] += 1
 
#recall that reveals empty cells
def reveal_cell(row, col):
    button = buttons[(row,col)]
    if button["state"] != "normal":
        return #stop if button is disabled/revealed
    
    button.config(relief=tk.SUNKEN, state="disabled", bg="lightgrey") #reveal and disable it
    
    if board[row][col] > 0:
        button.config(text=str(board[row][col]))
        return #dont reveal nieghbors of cells next to a mine

    for dr in (-1,0,1):
        for dc in (-1,0,1):
            if dr == 0 and dc == 0: 
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                reveal_cell(nr, nc)    
            


#left click reveal
def on_left_click(row, col):
    global game_over, first_click

    if first_click:
        place_mines(row,col)
        first_click = False

    if game_over:
        return
    button = buttons[(row,col)]
    print("Button ", row,",",col," pressed")
    if board[row][col] == -1:
        button.config(text="BOMB", bg="red")
        game_over = True
        messagebox.showinfo("Game over :(", "you clicked on a mine")

        for b in buttons.values():
            b.config(state="disabled")
    else:
        reveal_cell(row, col)
        check_win()

#right click flag/unflag
def on_right_click(event, row, col):
    if game_over:
        return
    button = buttons[(row, col)]
    current_text = button.cget("text")
    if current_text == "FLAG":
        button.config(text="")
    elif button["state"] == "normal":
        button.config(text="FLAG")
    


for r in range(rows): #making the buttons grid
    for c in range(cols):
        button = tk.Button(root,
            width=3, 
            height=1, 
            font=("Arial", 10, "bold"), 
            command=lambda row=r, col=c: on_left_click(row,col)
        ) #claude gave me the lamba command so the buttom can remember its position
        button.grid(row=r,column=c,padx=1,pady=1)
        button.bind("<Button-3>", lambda event, row = r, col=c: on_right_click(event,row,col))
        #using button as a dict to store key using the row and colloum
        buttons[(r,c)] = button



replay_button = tk.Button(root, text="Replay", font=("Arial", 12, "bold"), command=reset_board, bg="lightgreen", padx=10, pady=5)
replay_button.grid(row=rows, column=0, columnspan=cols, pady=10)


root.mainloop()

