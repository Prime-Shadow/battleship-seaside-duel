# Battleship Game with GUI
# Battleship — Seaside Duel (GUI)

Lightweight Battleship game with a Tkinter GUI. This repository contains the game logic, a Canvas-driven GUI, and a small helper script to start the application.

## Prerequisites

- Python 3.8+ installed
- Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Run the game

Automatic (recommended)

- From the project root you can start the game via the provided script. On Unix-like systems or from Git Bash / WSL on Windows run:

```bash
./start_battleship.sh
```

- On Windows PowerShell (without a Unix shell), run the script with `bash`:

```powershell
bash ./start_battleship.sh
```

Manual

- You can also run the main Python entry point directly. From the project root run:

```bash
python src/main.py
```

or (depending on your environment):

```bash
python -m src.main
```

Notes

- The `start_battleship.sh` script performs the same action as running the Python entry point and is provided for convenience.
- If the script is not executable on your platform, use `bash` as shown above or run the Python command directly.

Enjoy the game — press `o` to toggle ship orientation and `r` to reset while playing.

## Overview
This project implements a Battleship game where players can compete against a computer opponent. The game features a graphical user interface (GUI) built with Python, allowing for an interactive gameplay experience.

## Game Rules
- Each player secretly places five ships on a 10x10 grid.
- Players take turns calling coordinates (e.g., B4) to hit opponent ships.
- The opponent responds with "hit" or "miss."
- Players track their shots on separate grids using pegs (red for hit, white for miss).
- Ships cannot touch each other.
- When a ship's last spot is hit, the player announces, "You sunk my [ship name]!"
- If a player hits a ship, they are allowed a second try.

## Project Structure
```
battleship-seaside-duel
├── src
│   ├── main.py          # Entry point of the application
│   ├── game
│   │   ├── __init__.py  # Initializes the game module
│   │   ├── board.py     # Manages the game grid and hit detection
│   │   ├── ship.py      # Defines the Ship class
│   │   ├── player.py    # Manages player actions
│   │   └── ai.py        # Implements AI logic for the computer player
│   ├── gui
│   │   ├── __init__.py  # Initializes the GUI module
│   │   ├── app.py       # Sets up the main application window
│   │   └── widgets.py    # Defines GUI components
│   └── utils
│       ├── __init__.py  # Initializes the utils module
│       └── coords.py     # Utility functions for coordinate handling
├── tests
│   ├── test_board.py    # Unit tests for the Board class
│   └── test_ai.py       # Unit tests for the AI class
├── requirements.txt      # Lists project dependencies
├── LICENSE             # License
└── README.md             # Project documentation
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd battleship-gui
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the game:
   ```
   python src/main.py
   ```

## Gameplay Instructions
- Launch the application and follow the on-screen instructions to place your ships.
- Take turns with the computer to guess the coordinates of the opponent's ships.
- Keep track of your hits and misses on the provided grids.
- Aim to sink all of the computer's ships before it sinks yours!

Enjoy the game!

## License & Contribution

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

**Mihai Sirbu**

- GitHub: [Prime-Shadow](https://github.com/Prime-Shadow)
- Email: mihaisirbu28@gmail.com

---