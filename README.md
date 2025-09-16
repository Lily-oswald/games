# Games Collection

This repository contains various simple games you can play in the terminal.

## Available Games

### Card Guessing Game (`cardgame.py`)
The goal is to correctly guess card properties step by step until you win.
A full standard 52-card deck is simulated, and cards are drawn randomly.

### Pi Guessing Game (`pieceofpi.py`)
Try to guess the digits of π one at a time. The game continues until you make a mistake.

### Number Guessing Game (`number-guessing-game/`)
A classic number guessing game where you try to guess a randomly generated number between 1 and 100.

### Web Card Game (`card-game-web/`)
A web-based version of the card guessing game built with Flask.

## Card Guessing Game - How to Play
The game progresses in four steps:

Red or Black
The player guesses whether the first card will be Red (Hearts/Diamonds) or Black (Clubs/Spades).
If correct, the game continues. 
If wrong, the game restarts.

Higher or Lower
The player guesses if the next card will be higher or lower in rank compared to the first card.
Ranks go from Ace → King.
If correct, the game continues. 
If wrong, the game restarts.

In Between or Outside
The third card is drawn, and the player guesses whether its rank is in between or outside the first two cards’ values.
Example: If the first two cards are 5 and Jack, and the third card is 8, the correct answer is In Between.
If correct, move to the final step in the game. 
If wrong, the game restarts.

Guess the Suit
The player guesses the exact suit of the third card (Hearts, Diamonds, Clubs, Spades).
If correct, you Win!
If wrong, the game restarts.
