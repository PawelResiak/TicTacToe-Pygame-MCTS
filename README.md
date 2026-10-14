# M-N-K Game Engine with MCTS & Minimax AI

A professional, fully scalable engine for M-N-K games (Tic-Tac-Toe, Gomoku) built in Python. The project features a custom graphical user interface created with Pygame and implements advanced AI algorithms capable of playing on any board size.

## 🚀 Features

* **Dynamic Board Scaling:** Play classic 3x3 Tic-Tac-Toe, 5x5, 10x10, or even 19x19 Gomoku. The grid and UI automatically scale to fit the selected game mode.
* **Monte Carlo Tree Search (MCTS):** An advanced heuristic search algorithm implementation designed for large boards where traditional decision trees fail due to computational complexity.
* **Minimax Algorithm:** A mathematically perfect, unbeatable AI opponent optimized specifically for the classic 3x3 mode.
* **Clean MVC Architecture:** Strict separation of the game logic (`Board`, `Game`) from the presentation layer (`GameView`, `Button`). The core engine operates independently of Pygame, allowing for future cross-platform deployment or headless server execution.
* **Custom UI System:** A built-from-scratch interactive menu and button system without relying on heavy external UI frameworks.

## 📁 Project Structure

* `main.py` - The core application file containing the game logic, UI classes, and AI implementations.
* `.gitignore` - Standard git exclusions (virtual environments, cache).


## 🛠️ Installation & Running

1. Clone this repository:
   ```bash
   git clone [https://github.com/PawelResiak/TicTacToe-Pygame-MCTS.git](https://github.com/PawelResiak/TicTacToe-Pygame-MCTS.git)
