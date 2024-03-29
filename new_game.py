import eric_AI_2 as eric_bot
import nick_AI as nick_bot
import time
import sys
import numpy as np
from pprint import pprint
from game_state import GameState
from graphics import Graphics
from __init__ import *

# BLACK = 1 = UPPER
# WHITE = 0 = LOWER

# TODO: Check if move is valid should be done by calling get_piece_moves() and checking if the move is in the list
# TODO: Make get_valid_moves() return a dictionary with keys based on the pieces on the board
# TODO: change endgame logic for dictionary
# TODO: fix the helper functions to not use the old global variables

''' 
0 is white (lowercase), 1 is black (uppercase)

board_string = "<A1><A2><A3>...<H7><H8> <color's turn> <Castling Rights> <en passant target square> <halfmove clock> <fullmove number>"
        - Castling Rights (ex: KQkq) - K = white king side, Q = white queen side, k = black king side, q = black queen side
        - en passant target square (ex: e3) - if pawn moves two squares, this is the square behind it
        - halfmove clock (ex: 0) - number of halfmoves since last capture or pawn advance, used for 50 move rule
        - full move: current turn number

board_state = 8x8 string matrix 
        
move: str 
    <From Pos><To Pos> for example C3C5

'''


def run(DEBUG=False):
    # Initialize board state and turn counter 
    gs = GameState()

    graphics = Graphics(
        display_index=1,
        fullscreen=False
    )
    

    # Check and verify initial board state
    valid_moves = gs.get_valid_moves()

    p1 = eric_bot.AI()
    # p2 = eric_bot.AI()
    p2 = nick_bot.AI(True)

    players = (p2, p1)

    move = None

    while True:
        if DEBUG: 
            print(f"PLAYER: {gs.get_player_turn()}")
            print("-----------------------------------")
            print("-----------------------------------")

        if not graphics.running:
            gs.tick()
            graphics.draw(gs)
            continue

        # Update game time
        gs.tick()
        turn = gs.get_player_turn()



        # get potential move from player
        move = players[turn].get_ai_move(valid_moves)

        # If the players move is None, we have not received a new move, so just draw
        if move is None:  # TODO: this needs to check if the move is the same as the last?
            graphics.draw(gs)
            continue

        move_tuple = translate_move_s2t(move)
        move_from = move_tuple[0]
        move_to = move_tuple[1]

        if move_to in valid_moves[move_from]:
            # Update game board state
            gs.update(move)
            # Send updated move to the other player ai
            # NOTE: on turn 1, white's move is None at this line, so black will not recieve the first move... 
            players[not turn].recieve(move)
            graphics.draw(gs)
            
            # Checks new board state for valid moves
            valid_moves = gs.get_valid_moves()

            # Check for endgame conditions TODO: remove this it is being called in gs.draw()
            gs.handle_end_game(valid_moves)

        if DEBUG:        
            print("gs board")
            print_board(gs.board)
            print("-----------------------------------")
        
        time.sleep(.3)


if __name__ == "__main__":
    # import cProfile
    # import re
    # cProfile.run('run()', sort='tottime')
    # for i in range(10):
    run()