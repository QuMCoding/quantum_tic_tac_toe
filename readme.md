# Quantum Tic Tac Toe with Pygame Backend

Welcome to Quantum Tic Tac Toe! This project combines the classic game of Tic Tac Toe with the fascinating principles of quantum mechanics. The game is built using the Pygame library to provide a visually engaging and interactive experience.

## Table of Contents

1. [Installation](#installation)
2. [Game Rule](#game-rule)
3. [How to Play](#how-to-play)
4. [Requirements](#requirements)

## Installation

To run Quantum Tic Tac Toe on your machine, follow these steps:

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/your-username/quantum-tic-tac-toe.git
   ```

2. Navigate to the project directory:
   ```
   cd quantum-tic-tac-toe
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the game:
   ```
   python quantum_tic_tac_toe.py
   ```

## Game Rule

This game combines the classic Tic Tac Toe with the intriguing principles of quantum mechanics. Here are the basic rules to make it easier to understand:

1. Move Rules:

    Each player takes turns placing a pair of "quantum entangled" letters in different cells, representing entanglement between those cells.
2. Superposition State:

    Before being "observed," the letters in the cells exist in an undetermined quantum superposition state.
3. Observation (collapse mode):

    When a set of "quantum entangled" cells forms a closed loop, it needs to be "observed."
    After observation, the quantum state of the letters collapses, determining the content of the cells.
    The observed symbol is sure to be "exist," and turned into a "determined" symbol, where the entanglement symbol is "vanished." When the box is determined, other symbols inside the box "vanished." When there's only one symbol left alone in the box or the symbol whose entanglement has vanished, that symbol is also "determined."

    You should choose the symbol that is inside the closed loop to observe.
4. Winning Conditions:

    Once the letters are determined, the game follows the traditional Tic Tac Toe rules.
    The first player to successfully connect three letters in a row wins.
5. Tiebreaker:

    In the case of a tie where both players achieve victory conditions simultaneously, the winner is determined by comparing the maximum subscript of the connected letters, with the smaller subscript winning.

## How to play

1. Making a move

    You need to place your symbol inside the boxes, simply click the box then click the action button to place one symbol. You need to place two of these every step.

2. observation move (collapse mode)

    If a closed loop occurs, the player who's going to make the next step should choose which symbol to observe. Click the symbol you want to observe, then click the action button.

3. Winning

    The program won't tell you who has won when the game ends, because I'm lazy.

## Requirements

- Python 3.5 or up
- Pygame library

