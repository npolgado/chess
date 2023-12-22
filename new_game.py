import eric_AI_2 as eric_bot
import nick_AI as nick_bot
import time
import numpy as np
from game_state import GameState
from graphics import Graphics
from __init__ import *

''' 
# BLACK = 1 = UPPER
# WHITE = 0 = LOWER

board_string = "<A1><A2><A3>...<H7><H8> <color's turn> <Castling Rights> <en passant target square> <halfmove clock> <fullmove number>"
        - Castling Rights (ex: KQkq) - K = white king side, Q = white queen side, k = black king side, q = black queen side
        - en passant target square (ex: e3) - if pawn moves two squares, this is the square behind it
        - halfmove clock (ex: 0) - number of halfmoves since last capture or pawn advance, used for 50 move rule
        - full move: current turn number

board_state = 8x8 string matrix 
        
move: str 
    <From Pos><To Pos> for example C3C5

'''

def run(DEBUG = False): # PLEASE USE THIS DEBUG INSTEAD OF COMMENTING OUT
    # Initialize board state and turn counter 
    gs = GameState(init_empty_board(), DEBUG=DEBUG)
    graphics = Graphics(
        display_index=1,
        fullscreen=False
    )

    # Check and verify initial board state
    valid_moves = gs.get_valid_moves()

    p1 = eric_bot.AI()
    p2 = eric_bot.AI()

    players = (p1, p2)

    move = None

    while True:
        # busy if graphics paused
        if not graphics.running: 
            graphics.handle_game_events()
            continue
        
        # Update game time
        gs.tick()
        
        # Get boolean for current players turn
        current_turn = gs.get_player_turn()

        # Send updated move to the other player ai
        players[not current_turn].recieve(move)

        # Get potential move from player
        move = players[current_turn].get_target_move(valid_moves)

        # If the players move is None, we have not recieved a new move, so just draw
        if move == None:
            graphics.draw(board_state, gs.time)
            continue
            
        # Translate move from tuple to string
        move_tuple = translate_move_s2t(move)
        move_from = move_tuple[0]
        move_to = move_tuple[1]
        
        if move_to in valid_moves[move_from]:
            # Update game board state
            board_state = gs.update(move)

            # Draw
            graphics.draw(board_state, gs.time)
            
            # Checks new board state for valid moves
            valid_moves = gs.get_valid_moves()

            # Check for endgame conditions
            gs.handle_end_game()

        if DEBUG:
            print("\n\n")
            print(move)
            print("\n\n")
            for el in valid_moves:
                print(el, valid_moves[el])
            print("\n\n")
            print(move_from, move_to)
            print("\n\n")
            print(evaluate_board(board_state))
            print("\n\n")
            print_board(board_state)
            print("\n\n")

        time.sleep(0.1) 

if __name__ == "__main__":
    DEBUG = True # PLEASE USE THIS INSTEAD OF COMMENTING OUT
    run(DEBUG)