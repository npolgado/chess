CHESS
created by Nicholas Olgado and Eric Nicholls

Goal: to create our own application for chess. the idea was just for fun. Over the years its took shape into a full client with a CPU as well.

Game.py holds all the logic for the chess game. Run this file

new_game.py is much better than game.py

# Thoughts to Ponder

- Would it make more sense to have the BOARD in the game_state, and put all the non-global functions (in new_game.py) in gamestate, then give AI's access to the gamestate class?
    - Advantage: OOP, game state knows the entire game state, not just some variables
    - Wouldn't make a huge difference. Is it cleaner though?



# ERIC:

- [ ] figure out player turn logic (why is it backward what you think - gs.player_turn == white should be trying to maximize)

- [ ] Prune: create method that runs after minimax 
    - print out tree at each depth

- [ ] GS for ea. Node: Holding the gamestate for each node takes a lot of memory and probably time
    - imitate get_valid_moves() manually since thats all you need it for (board, player_turn, en_passant, etc.)
    - can identical GS objects be combined in the tree?
    - get valid moves should be part of init and should take in a board, en_passant, and castling rights



# TODO:

- Tests outline (Nick)
    - [x] helpers testing
    - [ ] valid move testing
    - [ ] endgame testing
    - [ ] castling testing
    - [ ] en passant testing
    - [ ] turn logic testing

- [ ] AI Threading
    - [ ] Thread function and get_function

- [ ] V1 of AI's work
    - [ ] time control (optional)
    - [ ] flesh out revice / get move logic / flow
    - [ ] Nick
    - [ ] Eric

- [ ] Full Review, Comment, and Cleanup Session (Eric + Nick)

# COMPLETE

- [x] Move everything to game_state (board, functions)

- [X] Getting the Game to Flow (Eric)
	- [X] checking if a move is valid (in run) should call get_piece_moves instead of get_valid_moves
	- [X] make the valid moves array a dictionary
    - [X] AI's making random valid moves (see gameplay on output)
    - [X] Finish Update board (Eric)

- [x] Graphics (Nick)
    - [x] initial display and board
    - [x] draw pieces
    - [ ] [NICE TO HAVE] turn counter
    - [x] [NICE TO HAVE] timer with real time
    - [ ] [NICE TO HAVE] move history
    - [ ] [NICE TO HAVE] move highlighting (current / past)

# GOALS

- Cleanup
    - [x] identify changes in the code

- Multiplayer online (PvP, PvAI, AIvAI)
    - [ ] dropdown for engine choice
    - [ ] identify multiplayer

- Custom game time

- 1v1 online using custom AI assistance
    - [ ] final integration and testing

