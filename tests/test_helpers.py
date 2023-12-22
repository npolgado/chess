# import new_game from outside test folder
import sys
sys.path.append("..")
from __init__ import *

TEST_BOARD_1 = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['-', '-', '-', '-', '-', '-', '-', '-'], 
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'], 
    ['-', '-', '-', '-', '-', '-', '-', '-'], 
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]
TEST_BOARD_2 = [
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'], 
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'], 
    ['-', '-', '-', '-', '-', '-', '-', '-'], 
    ['-', '-', '-', '-', '-', '-', '-', '-'], 
    ['-', '-', '-', '-', '-', '-', '-', '-']
]
TEST_BOARD_3 = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', '-', 'p', 'p', 'p', 'p'],
    ['-', '-', '-', '-', '-', '-', '-', '-'], 
    ['-', '-', '-', 'p', '-', '-', '-', '-'],
    ['-', '-', '-', '-', 'P', '-', '-', '-'], 
    ['-', '-', '-', '-', '-', '-', '-', '-'], 
    ['P', 'P', 'P', 'P', '-', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

TEST_BOARD_STR_1 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
TEST_BOARD_STR_2 = "8/8/8/8/8/8/8/8"
TEST_BOARD_STR_3 = "rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR"

TEST_MOVE_1 = "E2E4"
TEST_MOVE_2 = "E7E5"
TEST_MOVE_3 = "E1E2"
TEST_MOVE_4 = "A1H8"
TEST_MOVE_5 = "A8H1"

TEST_MOVE_TUPLE_1 = ((4, 1), (4, 3)) # TODO: this is wrong, E2 should be 1, 4 and E4 should be 3, 4
TEST_MOVE_TUPLE_2 = ((4, 6), (4, 4))
TEST_MOVE_TUPLE_3 = ((4, 0), (4, 1))
TEST_MOVE_TUPLE_4 = ((0, 0), (7, 7))
TEST_MOVE_TUPLE_5 = ((0, 7), (7, 0))

def test_board_to_string():
    assert board_to_string(TEST_BOARD_1) == TEST_BOARD_STR_1
    assert board_to_string(TEST_BOARD_2) == TEST_BOARD_STR_2
    assert board_to_string(TEST_BOARD_3) == TEST_BOARD_STR_3

def test_string_to_board():
    test_1 = string_to_board(TEST_BOARD_STR_1)
    assert np.array_equal(test_1, TEST_BOARD_1)

    test_2 = string_to_board(TEST_BOARD_STR_2)
    assert np.array_equal(test_2, TEST_BOARD_2)

    test_3 = string_to_board(TEST_BOARD_STR_3)
    assert np.array_equal(test_3, TEST_BOARD_3)

def test_translate_move_s2t():
    assert translate_move_s2t(TEST_MOVE_1) == TEST_MOVE_TUPLE_1
    assert translate_move_s2t(TEST_MOVE_2) == TEST_MOVE_TUPLE_2
    assert translate_move_s2t(TEST_MOVE_3) == TEST_MOVE_TUPLE_3
    assert translate_move_s2t(TEST_MOVE_4) == TEST_MOVE_TUPLE_4
    assert translate_move_s2t(TEST_MOVE_5) == TEST_MOVE_TUPLE_5

def test_translate_move_t2s():
    assert translate_move_t2s(*TEST_MOVE_TUPLE_1[0], *TEST_MOVE_TUPLE_1[1]) == TEST_MOVE_1
    assert translate_move_t2s(*TEST_MOVE_TUPLE_2[0], *TEST_MOVE_TUPLE_2[1]) == TEST_MOVE_2
    assert translate_move_t2s(*TEST_MOVE_TUPLE_3[0], *TEST_MOVE_TUPLE_3[1]) == TEST_MOVE_3
    assert translate_move_t2s(*TEST_MOVE_TUPLE_4[0], *TEST_MOVE_TUPLE_4[1]) == TEST_MOVE_4
    assert translate_move_t2s(*TEST_MOVE_TUPLE_5[0], *TEST_MOVE_TUPLE_5[1]) == TEST_MOVE_5

if __name__ == "__main__":
    assert TEST_BOARD_1 == init_empty_board()
    test_board_to_string()
    test_string_to_board()
    test_translate_move_s2t()
    test_translate_move_t2s()
    print("All tests passed!")