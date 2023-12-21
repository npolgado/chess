CHESS
created by Nicholas Olgado and Eric Nicholls

Goal: to create our own application for chess. the idea was just for fun. Over the years its took shape into a full client with a CPU as well. All AI coding is done by Eric Nicholls

Game.py holds all the logic for the chess game. Run this file



# TODO - Nick:

- Getting the Game to Flow (Eric)
	- [X] checking if a move is valid (in run) should call get_piece_moves instead of get_valid_moves
	- [X] make the valid moves array a dictionary
    - [ ] AI's making random valid moves (see gameplay on output)
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
    - [ ] draw pieces
    - [ ] possible issue!!: redrawing properly (blit vs. flip)
    
    - [ ] [NICE TO HAVE] turn counter
    - [x] [NICE TO HAVE] timer with real time
    - [ ] [NICE TO HAVE] move history
    - [ ] [NICE TO HAVE] move highlighting (current / past)

# GOALS

- Cleanup
    - [x] identify changes in the code

- Multiplayer online
    - [ ] dropdown for engine choice
    - [ ] identify multiplayer

- Custom game time
- 1v1 online using custom AI assistance
    - [ ] final integration and testing

# ISSUES TO FIX
- [ ] AI vs. AI king can take king
- [ ] AI's crash
- [ ] AI's speed up at end game
