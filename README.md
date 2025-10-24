# Minesweeper with AI Solver

An interactive Minesweeper game built with Python and Tkinter, featuring an AI solver that uses constraint satisfaction algorithms to play the game automatically.

## Goal of the App

This application provides a classic Minesweeper gaming experience with an AI solver that demonstrates logical deduction and constraint satisfaction techniques to solve the puzzle. Players can either play manually or watch the AI solve the game step-by-step with visual highlighting to understand its decision-making process at any point of the game.

## Tech Stack

- **Language:** Python 
- **GUI Framework:** Tkinter (built-in with Python)
- **Algorithim Approach:** Constraint Satisfaction Problem (CSP) solving with logical deduction

## Target Users

- Students and developers interested in learning about AI algorithms and constraint satisfaction
- Anyone curious about how logical deduction can be automated to solve puzzle games

## Features

- Customizable board size (user-defined grid dimensions)
- Dark-themed, modern UI with color-coded number cells
- Right-click flagging system
- AI solver with visual step-by-step execution
- Hover effects and smooth animations
- Safe first-click guarantee (no mines near initial click)

## Set-Up Instructions

### Prerequisites

- Python 3.6 or higher installed on your system
- Tkinter (usually comes pre-installed with Python)

### Installation

1. **Clone or download the repository:**
```bash
   git clone <your-repository-url>
   cd <repository-folder>
```

2. **Verify Python installation:**
```bash
   python --version
```

### Running the Game

1. **Navigate to the project directory** in your terminal/command prompt

2. **Run the main game file:**
```bash
   python minesweeper.py
```


3. **Enter board size** when prompted (e.g., 10 for a 10×10 grid)

4. **Play the game:**
   - **Left-click** to reveal cells
   - **Right-click** to flag suspected mines
   - Click **"Start AI Solver"** to watch the AI play
   - Click **"Stop Solver"** to pause the AI
   - Click **"Replay"** to start a new game

## How the AI Solver Works

The AI uses two main strategies:

1. **Basic Logical Deduction:**
   - If a cell's number equals its flagged neighbors, all other neighbors are safe
   - If a cell's number equals flagged + unrevealed neighbors, all unrevealed are mines

2. **Constraint Satisfaction:**
   - Compares constraints from multiple cells
   - Finds subset relationships to deduce safe cells and mines
   - Makes guesses when logic alone isn't sufficient

Watch the color-coded visualization to see the AI's thinking process:
- **Yellow:** Cell being analyzed
- **Light Blue:** Target cells identified
- **Light Green:** Safe cells found
- **Orange:** Mines identified

## File Structure
```
├── minesweeper.py          # Main game file with UI and game logic
├── minesweeper_solver.py   # AI solver algorithm implementation
└── README.md               # This file
```

## Future Enhancements

- Probability-based guessing when no logical moves exist
- Difficulty levels with preset board configurations
- Game statistics and win/loss tracking
- Improved AI visualization options





Documantations I used:
-   https://pyautogui.readthedocs.io/en/latest/index.html

-   https://docs.python.org/3/library/tkinter.html