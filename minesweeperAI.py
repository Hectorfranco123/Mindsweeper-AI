import tkinter as tk
from tkinter import simpledialog


root = tk.Tk()
root.title("minesweeper")

#ask user for size
size = simpledialog.askinteger("Board size","Enter Number: ")
#if user just doesnt for some reason 
if size is None:
    size = 10

#board size 
rows = cols = size 

buttons = {}
#TODO create a 2d list of buttons to store the game, named board 

#TODO create function to place mines randompomy on the board


#TODO make it so a left click and right click do different things
def on_click(row, col):
    button = buttons[(row,col)]
    button.config(bg="red")
    print("Button ", row,",",col," pressed")


for r in range(rows): #making the buttons grid
    for c in range(cols):
        button = tk.Button(root,width=3, height=1, font=("Arial", 10, "bold"), command=lambda row=r, col=c: on_click(row,col)) #claude gave me the lamba command so the buttom can remember its position
        button.grid(row=r,column=c,padx=1,pady=1)
        #using button as a dict to store key using the row and colloum
        buttons[(r,c)] = button


root.mainloop()

