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


def run(p1, p2, DEBUG=False):
    # Initialize board state and turn counter 
    gs = GameState()

    graphics = Graphics(
        display_index=0,
        fullscreen=False
    )
    
    # Check and verify initial board state
    valid_moves = gs.get_valid_moves()

    players = (p1, p2)

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
        side = "Black" if turn else "White"

        # get potential move from player
        move = players[turn].get_move(valid_moves)

        # If the players move is None, we have not received a new move, so just draw
        # TODO: this needs to check if the move is the same as the last?
        if move is None:  
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

        print(f"[GAME] Turn: {gs.turn_num} | Player: {side} | Move: {move} | Move Tuple: {move_tuple}")       

        if DEBUG: 
            print("gs board")
            print_board(gs.board)
            print("-----------------------------------")

if __name__ == "__main__":
    import cProfile
    import re
    import threading

    # lock = threading.Lock()

    # p1 = eric_bot.AI()
    # p2 = eric_bot.AI()
    p1 = nick_bot.AI(True)
    p2 = nick_bot.AI(True)
    
    try:
        p1.start()
        p2.start()
        # cProfile.run('run()', sort='tottime')
        run(p1, p2, False)
    except Exception as e:
        print(e)
        p1.on_exit()
        p2.on_exit()
        sys.exit()