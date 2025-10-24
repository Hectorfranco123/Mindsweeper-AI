import tkinter as tk
from tkinter import simpledialog, messagebox
import random
from minesweeper_solver import MinesweeperSolver

root = tk.Tk()
root.title("Minesweeper")
root.configure(bg="#1a1a2e")

#ask user for size
size = simpledialog.askinteger("Board size","Enter Number: ")
if size is None:
    size = 10
colors = {
    'bg': '#1a1a2e',
    'button_normal': '#16213e',
    'button_hover': '#0f3460',
    'button_revealed': '#e8e8e8',
    'mine': '#e94560',
    'safe': '#06ffa5',
    'flag': '#f39c12',
    'numbers': {
        1: '#2196F3',
        2: '#4CAF50',
        3: '#FF5722',
        4: '#9C27B0',
        5: '#FF9800',
        6: '#00BCD4',
        7: '#607D8B',
        8: '#F44336'
    }
}
#board size 
rows = cols = size 
num_mines = (rows * cols) // 6 #1/6 of board are mines

buttons = {} #button widgets
board =[] #2d list of buttons to store the game, named board 
mine_positions = set() #keep track of where mines are

game_over = False 
first_click = True

solver_running = False
solver_delay = 250  # milliseconds



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
    global mine_positions, game_over, first_click, solver_running


    solver_running = False
    first_click = True
    game_over = False 
    mine_positions= set()
    make_board()
    for button in buttons.values():
        button.config(text="", relief=tk.RAISED, state="normal", bg=colors['button_normal'], fg="white", activebackground=colors['button_hover'])

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
        for button in buttons.values():
            button.config(state="disabled")

    # see if win works
    # print(f"Unrevealed cells: {unrevealed_count}, Mines: {num_mines}")

    

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

    # testing mine placement
    # print(f"Total mines placed: {len(mine_positions)}")
    # print(f"Mine positions: {mine_positions}")
    # print(f"Expected mines: {num_mines}")


 
#recall that reveals empty cells
def reveal_cell(row, col):
    button = buttons[(row,col)]
    if button["state"] != "normal":
        return #stop if button is disabled/revealed
    
    button.config(relief=tk.SUNKEN, state="disabled", bg=colors['button_revealed']) #reveal and disable it
    
    if board[row][col] > 0:
        num = board[row][col]
        button.config(text=str(num), disabledforeground=colors['numbers'].get(num, '#000'))
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
        button.config(text="BOMB", bg=colors['mine'], fg="white")
        game_over = True
        messagebox.showinfo("Game over :(", "You clicked on a mine")

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
        button.config(text="",bg=colors['button_normal'])
    elif button["state"] == "normal":
        button.config(text="FLAG", bg=colors['flag'], fg="white")

def on_button_enter(event, row, col):
    button = buttons[(row, col)]
    if button["state"] == "normal":
        button.config(bg=colors['button_hover'])

def on_button_leave(event, row, col):
    button = buttons[(row, col)]
    current_text = button.cget("text")
    if button["state"] == "normal":
        if current_text == "FLAG":
            button.config(bg=colors['flag'])
        elif current_text != "BOMB":
            button.config(bg=colors['button_normal'])

def reset_cell_colors():
    for button in buttons.values():
        if button["state"] == "normal" and button.cget("text") != "FLAG":
            button.config(bg=colors['button_normal'])

def visual_solver(checked_cells, target_cells, color):
    #visualize the thinking of the solver
    """
    checked_cells: dict of souce cell and surounding neighbor cells analyzed
    target_cells: cells that will be acted upon
    color: color to highlight target cells
    """

    #highlight cells being analyzed 
    for source, neighbor_set in checked_cells.items():
        if neighbor_set:
            button = buttons[source]
            if button["state"] == "disabled":
                #change bg to yellow while its being checked
                original_bg = button.cget("bg")
                button.config(bg="yellow")


            for neighbor in neighbor_set:
                if neighbor in target_cells:
                    buttons[neighbor].config(bg="lightblue") #highlight target cells
    root.update()
    root.after(solver_delay) #pause for a moment to visualize

    for cell in target_cells:
        buttons[cell].config(bg=color)

    root.update()
    root.after(solver_delay) #pause for a moment to visualize

def solver_step():
    "performs one step of the solver algorithm."
    global game_over, solver_running, first_click

    # track how many cells have been revealed
    # revealed_count = 0
    # for button in buttons.values():
    # Check if the button is disabled/revealed
    # if button["state"] == "disabled":
    #    revealed_count += 1
    # print(f"Solver step - Revealed: {revealed_count}/{rows*cols}")

    if game_over or not solver_running:
        solver_running = False
        reset_cell_colors()
        return

    #if first click, pick a random cell
    if first_click:
        mid_row, mid_col = rows // 2, cols // 2
        on_left_click(mid_row, mid_col)
        root.after(solver_delay,solver_step)
        return

    #make instance of solver
    solver = MinesweeperSolver(board,buttons,rows,cols,mine_positions)

    #find next move 
    move_type, cells, checked_cells = solver.find_move()

    if move_type == "safe":
        #make safe thinking cells green
        visual_solver(checked_cells,cells,"lightgreen")

        #click all safe cells

        for cell in cells:
            row, col = cell
            on_left_click(row,col)

        reset_cell_colors()


        #continue 
        if not game_over:
            root.after(solver_delay, solver_step)

    elif move_type == "mine":
        #make cell orange for mines
        visual_solver(checked_cells, cells, "orange")

        #flag all mines
        for cell in cells:
            row, col = cell 
            button = buttons[cell]
            if button["state"]=="normal":
                button.config(text="FLAG", bg=colors['flag'], fg='white')


        reset_cell_colors()

        #continue 
        if not game_over:
            root.after(solver_delay, solver_step)

        

    else:
        #nothing found so make guess

        cell = solver.get_random_safe_cell()

        if cell:
            row, col = cell

            #highlight guess in yellow
            buttons[cell].config(bg="yellow")
            root.update()
            root.after(solver_delay)

            on_left_click(row, col)
            reset_cell_colors()

            if not game_over:
                root.after(solver_delay, solver_step)

        else:
            #no more moves
            solver_running = False
            reset_cell_colors()



def start_solver():
    global solver_running, game_over

    if game_over:
        messagebox.showinfo("Game done","Please start a new game first!")
        return
    if solver_running:
        messagebox.showinfo("Solver Running", "Solver is already running!")
        return
    
    solver_running = True
    solver_step()


def stop_solver():
    global solver_running
    solver_running = False
    reset_cell_colors()


game_frame = tk.Frame(root, bg=colors['bg'], padx=15, pady=15)
game_frame.grid(row=0, column=0)

for r in range(rows): #making the buttons grid
    for c in range(cols):
        button = tk.Button(game_frame,
            width=4, 
            height=2, 
            font=("Arial", 12, "bold"), 
            bg=colors["button_normal"],
            fg='white',  
            activebackground=colors['button_hover'], 
            relief=tk.RAISED,
            bd=1,
            command=lambda row=r, col=c: on_left_click(row,col)
        ) #claude gave me the lamba command so the buttom can remember its position
        button.grid(row=r,column=c,padx=1,pady=1)
        button.bind("<Button-3>", lambda event, row=r, col=c: on_right_click(event, row, col))
        button.bind("<Enter>", lambda event, row=r, col=c: on_button_enter(event, row, col))  
        button.bind("<Leave>", lambda event, row=r, col=c: on_button_leave(event, row, col))
        #using button as a dict to store key using the row and colloum
        buttons[(r,c)] = button


control_frame = tk.Frame(root, bg=colors["bg"])
control_frame.grid(row=rows, column=0, columnspan=cols, pady=10)

replay_button = tk.Button(control_frame, text="Replay", font=("Arial", 12, "bold"),
                          command=reset_board, bg=colors['safe'], padx=10, pady=5, cursor='hand2')
replay_button.pack(side=tk.LEFT, padx=5)

solver_button = tk.Button(control_frame, text="Start AI Solver", font=("Arial", 12, "bold"), 
                          command=start_solver, bg="lightblue", padx=10, pady=5,cursor='hand2')
solver_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(control_frame, text="Stop Solver", font=("Arial", 12, "bold"), 
                        command=stop_solver, bg="salmon", padx=10, pady=5,cursor='hand2')
stop_button.pack(side=tk.LEFT, padx=5)

root.mainloop()

