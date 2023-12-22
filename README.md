CHESS
created by Nicholas Olgado and Eric Nicholls

Goal: to create our own application for chess. the idea was just for fun. Over the years its took shape into a full client with a CPU as well.

Game.py holds all the logic for the chess game. Run this file

new_game.py is much better than game.py

# Thoughts to Ponder

- Would it make more sense to have the BOARD in the game_state, and put all the non-global functions (in new_game.py) in gamestate, then give AI's access to the gamestate class?
    - Advantage: OOP, game state knows the entire game state, not just some variables
    - Wouldn't make a huge difference. Is it cleaner though?


# TODO - Nick:

- [X] Getting the Game to Flow (Eric)
	- [X] checking if a move is valid (in run) should call get_piece_moves instead of get_valid_moves
	- [X] make the valid moves array a dictionary
    - [X] AI's making random valid moves (see gameplay on output)

- [ ] Move everything to game_state (board, functions)
    - [ ] rename board_state to board

- [X] Finish Update board (Eric)

- [ ] King Logic (Eric)
    - [ ] Move can't put/keep King in check
    - [ ] Castling logic
	- [ ] change end_game() logic

- Tests outline (Nick)
    - [x] helpers testing
    - [ ] valid move testing
    - [ ] endgame testing
    - [ ] castling testing
    - [ ] en passant testing
    - [ ] turn logic testing

- Graphics (Nick)
    - [x] initial display and board
    - [x] draw pieces
    - [ ] [NICE TO HAVE] turn counter
    - [x] [NICE TO HAVE] timer with real time
    - [ ] [NICE TO HAVE] move history
    - [ ] [NICE TO HAVE] move highlighting (current / past)

- [ ] Full Review, Comment, and Cleanup Session (Eric + Nick)

# GOALS

- Cleanup
    - [x] identify changes in the code

- Multiplayer online (PvP, PvAI, AIvAI)
    - [ ] dropdown for engine choice
    - [ ] identify multiplayer

- Custom game time

- 1v1 online using custom AI assistance
    - [ ] final integration and testing

