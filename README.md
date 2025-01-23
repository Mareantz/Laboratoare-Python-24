# Laboratoare-Python-24

This repository contains the laboratories and the project for the Python Programming course conducted during the 1st semester of the 3rd year of the Bachelor's Degree at the Faculty of Computer Science Iași.

---

# Backgammon Multiplayer Game

A networked Backgammon game built with Python, featuring a graphical user interface (GUI) using Tkinter and real-time multiplayer capabilities via socket programming. Play against an AI opponent or compete against another human player over a local network.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Server](#running-the-server)
  - [Running the Clients](#running-the-clients)
  - [Automated Setup](#automated-setup)
- [Game Controls](#game-controls)

## Features

- **Graphical User Interface**: Intuitive and responsive UI built with Tkinter.
- **Multiplayer Support**: Play against another human player over a network.
- **AI Opponent**: Single-player mode against a simple AI.
- **Real-Time Updates**: Instantaneous synchronization of game state between clients and server.
- **Dice Mechanics**: Realistic dice rolling with visual representation.
- **Move Validation**: Ensures all moves adhere to Backgammon rules.
- **Bore Off Functionality**: Proper handling of bearing off pieces to win the game.
- **Logging**: Comprehensive logging for debugging and game tracking.

## Technologies

- **Python 3.x**
- **Tkinter**: For building the GUI.
- **Socket Programming**: For network communication between server and clients.
- **Pickle**: For serializing and deserializing game state data.
- **Threading**: To handle multiple client connections concurrently.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Mareantz/Laboratoare-Python-24
   cd BackgammonProject
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   This project uses only Python's standard libraries, so no additional installations are required.

## Usage

### Running the Server

1. **Navigate to the Project Directory**

   ```bash
   cd BackgammonProject
   ```

2. **Start the Server**

   ```bash
   python server.py
   ```

   The server will start and listen for incoming client connections on `127.0.0.1:12345`.

### Running the Clients

1. **Open a New Terminal Window for Each Client**

2. **Start the Client**

   ```bash
   python client.py
   ```

3. **Choose Game Mode**

   - **Play vs AI**: Play against the computer.
   - **Play vs Human**: Connect to the server and play against another human player.

4. **Select Your Color**

   Choose between White or Black when prompted.

### Automated Setup

A helper script `run_this.py` is provided to launch the server and two clients simultaneously in separate console windows.

1. **Run the Automated Script**

   ```bash
   python run_this.py
   ```

   **Note**: This script is designed for Windows due to the use of `creationflags=subprocess.CREATE_NEW_CONSOLE`. Modify accordingly for other operating systems.

## Game Controls

- **Roll Dice**: Click the "Roll Dice" button to initiate your turn.
- **Select and Move Pieces**: Click on a triangle (point) containing your pieces to select it, then click on a valid destination to move.
- **Bore Off**: Once all your pieces are in the home quadrant, use the "Bore Off" button to remove pieces from the board.
- **Dice Representation**: Used and unused dice are visually distinguished to track available moves.
