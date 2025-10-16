import tkinter as tk
from tkinter import simpledialog
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

#make board with zeros
for r in range(rows):
    row = [] 
    for c in range(cols):
        row.append(0)
    board.append(row)

#TODO create function to place mines randomly on the board

def place_mines():
    global mine_positions #use predetermined variable 
    while len(mine_positions) < num_mines:
        r = random.randint(0,rows -1)
        c = random.randint(0, cols -1)
        if (r,c) not in mine_positions:
            mine_positions.add((r,c))
            board[r][c] = -1 #-1 means mine is located here
    
    #After mines are made, update surounding cells to count near mines
    for r,c in mine_positions:
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                nc, nr = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != -1:
                    board[nr][nc] += 1
 
#recall that reveals empty cells
def reveal_cell(row, col):
    if button["state"] != "normal":
        return #stop if button is disabled/revealed
    
    button.config(relief=tk.SUNKEN, state="disbaled", bg="lightgrey") #reveal and disable it
    
    if board[row][col] > 0:
        button.config(text=str(board[row][col]))
        return #dont reveal nieghbors of cells next to a mine

    for dr in (-1,0,1):
        for dc in (-1,0,1):
            nr,nc = row + dr, col +dc #neighbor cords
            if 0 <= nr < rows and 0 <= nc < cols: #bounds check
                neighbor = button[(nr,nc)]
                if neighbor["state"] == "normal":
                    reveal_cell(nr,nc) #recall


#left click reveal
def on_left_click(row, col):
    button = buttons[(row,col)]
    print("Button ", row,",",col," pressed")
    if board[row][col] == -1:
        button.config(text="BOMB", bg="red")
        messagebox.showinfo("Game over :(", "you clicked on a mine")
    else:
        reveal_cell(row, col)

#right click flag/unflag
def on_right_click(event, row, col):
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


place_mines()


root.mainloop()

