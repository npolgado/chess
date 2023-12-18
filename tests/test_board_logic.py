# import new_game from outside test folder
import sys
sys.path.append("..")
from new_game import *

def test_get_pawn_moves():
    pass

def test_get_piece_moves():
    pass

def test_get_all_moves():
    pass

def test_get_king_position():
    pass

def test_is_checked():
    pass 

def test_is_insufficient_material():
    pass 

def test_is_fifty_move_rule():
    pass 

if __name__ == "__main__":
    test_get_pawn_moves()
    test_get_piece_moves()
    test_get_all_moves()
    test_get_king_position()
