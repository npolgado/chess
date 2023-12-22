import numpy as np
import time
from __init__ import board_to_string

class GameState:
    def __init__(self, turn: int=1) -> None:
        self.turn = turn

        self.bool_turn = (self.turn - 1) % 2
        self.enpassant_square = None
        
        self.board_history = []
        self.board_dict = {}
        self.is_three_fold_repetition = False
        self.castling_rights = {
            "w_Q": True,
            "w_K": True,
            "b_Q": True,
            "b_K": True
        }

        self.time = (0,0)
        self.start_time = time.monotonic()
        self.time_white = 0
        self.time_black = 0

    def update_castling_rights(self, board_state) -> None:
        # if the kings or rooks aren't in their starting position, update appropriate castling rights to False (never can be changed to True once False)
        if board_state[0][4] != 'k':
            if self.castling_rights['b_Q']:
                self.castling_rights['b_Q'] = False
            if self.castling_rights['b_K']:
                self.castling_rights['b_K'] = False
        if board_state[0][0] != 'r' and self.castling_rights['b_Q']:
            self.castling_rights['b_Q'] = False
        if board_state[0][7] != 'r' and self.castling_rights['b_K']:
            self.castling_rights['b_K'] = False

        if board_state[7][4] != 'K':
            if self.castling_rights['w_Q']:
                self.castling_rights['w_Q'] = False
            if self.castling_rights['w_K']:
                self.castling_rights['w_K'] = False
        if board_state[7][0] != 'R' and self.castling_rights['w_Q']:
            self.castling_rights['w_Q'] = False
        if board_state[7][7] != 'R' and self.castling_rights['w_K']:
            self.castling_rights['w_K'] = False

        # print(self.castling_rights, "\n")

    def get_player_turn(self):
        return self.bool_turn
    
    def get_board_history(self):
        return self.board_history

    def get_three_fold_repetition(self):
        return self.is_three_fold_repetition
    
    def get_en_passant_square(self):
        return self.enpassant_square

    def set_en_passant_square(self, en_passant_square):
        self.enpassant_square = en_passant_square
        print("En Passant Square = ", en_passant_square)

    def archive(self, board):
        board_str = board_to_string(board)
        self.board_history.append(board_str)

        if board_str in self.board_dict:
            self.board_dict[board_str] += 1
            if self.board_dict[board_str] >= 3:
                self.is_three_fold_repetition = True
        else:
            self.board_dict[board_str] = 1

    def tick(self):
        # # start time if it is turn 1
        # if self.turn == 0:
        #     self.start_time = time.monotonic()
        # else:
        
        # Capture elapsed time
        t = time.monotonic() - self.start_time
        self.start_time = time.monotonic()

        # update players time
        if self.bool_turn: self.time_white += t
        else: self.time_black += t

        # update time
        self.time = (self.time_white,self.time_black)

    def update(self, board):
        self.update_castling_rights(board)
        self.archive(board)
        self.turn += 1
        self.bool_turn = not self.bool_turn