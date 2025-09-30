import pyautogui
import tkinter as tk

def button_one_thing():
    print("YOU DID A THING")

def button_two_thing():
    print("YOU DID ANOTHER THING")

def screenshot_test():
    screenshot = pyautogui.screenshot(region=(490,690,946,844)) # left, top, width, and height of ss
    screenshot.save("board.png")

root = tk.Tk()

root.title("Screenshot Selection Menu")
root.geometry("1000x1000")

button_one = tk.Button(root, text="button",command= button_one_thing)
button_one.pack(pady=5)

button_two = tk.Button(root, text="button 2",command= button_two_thing)
button_two.pack(pady=5)

button_three = tk.Button(root, text="ScreenShot Cords", command=screenshot_test)
button_three.pack(pady=12,padx=19)
root.mainloop()



