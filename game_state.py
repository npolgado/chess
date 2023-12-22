import numpy as np
import time
import sys
from __init__ import *

class GameState:
    def __init__(self, board=None, turn: int=1, DEBUG=False) -> None:
        self.board = board

        self.turn = turn
        self.bool_turn = (self.turn - 1) % 2
        
        self.enpassant_square = None
        self.castling_rights = {
            "w_Q": True,
            "w_K": True,
            "b_Q": True,
            "b_K": True
        }
 
        self.board_history = []
        self.board_dict = {}

        self.valid_moves = {}
        self.board_evaluation = evaluate_board(self.board)

        self.is_three_fold_repetition = False
        self.is_insufficient_material_bool = False
        self.is_fifty_move_rule_bool = False

        self.time = (0,0)
        self.start_time = time.monotonic()
        self.time_white = 0
        self.time_black = 0

    def update_castling_rights(self) -> None:
        # if the kings or rooks aren't in their starting position, update appropriate castling rights to False (never can be changed to True once False)
        if self.board[0][4] != 'k':
            if self.castling_rights['b_Q']:
                self.castling_rights['b_Q'] = False
            if self.castling_rights['b_K']:
                self.castling_rights['b_K'] = False
        if self.board[0][0] != 'r' and self.castling_rights['b_Q']:
            self.castling_rights['b_Q'] = False
        if self.board[0][7] != 'r' and self.castling_rights['b_K']:
            self.castling_rights['b_K'] = False

        if self.board[7][4] != 'K':
            if self.castling_rights['w_Q']:
                self.castling_rights['w_Q'] = False
            if self.castling_rights['w_K']:
                self.castling_rights['w_K'] = False
        if self.board[7][0] != 'R' and self.castling_rights['w_Q']:
            self.castling_rights['w_Q'] = False
        if self.board[7][7] != 'R' and self.castling_rights['w_K']:
            self.castling_rights['w_K'] = False

        # print(self.castling_rights, "\n")

    def get_player_turn(self):
        return self.bool_turn
    
    def get_board_history(self):
        return self.board_history

    def get_three_fold_repetition(self):
        return self.is_three_fold_repetition

    def get_fifty_moves(self):
        return self.is_fifty_move_rule_bool

    def get_insufficient_material(self):
        return self.is_insufficient_material_bool

    def get_en_passant_square(self):
        return self.enpassant_square

    def get_board_evaluation(self):
        self.board_evaluation = evaluate_board(self.board) 
        return self.board_evaluation

    def get_pawn_moves(self, row, col):
        player_turn = self.bool_turn
        en_passant = self.get_en_passant_square()
        if player_turn == 0:
            direc = 1
            starting_row = 1
            if row + direc > 7: # TODO: Handle promotion, possibly pass in the piece to promote to
                direc = -1
        else:
            direc = -1
            starting_row = 7

        moves = []

        # advances
        if self.board[row + direc][col] == "-":
            moves.append((row + direc, col))
            if row == starting_row and self.board[row + 2*direc][col] == "-":
                moves.append((row + 2*direc, col))
        
        # captures
        if col + 1 < 8:
            # right captures
            if self.board[row + direc][col + 1] != "-" and self.board[row + direc][col + 1].isupper() != player_turn:
                moves.append((row + direc, col + 1))
            # en passant
            if (row + direc, col + 1) == en_passant and self.board[row + direc][col + 1].isupper() != player_turn:
                moves.append((row + direc, col+1))

        if col - 1 >= 0:
            # left captures
            if self.board[row + direc][col - 1] != "-" and self.board[row + direc][col - 1].isupper() != player_turn:
                moves.append((row + direc, col - 1))
            # en passant
            if (row, col-1) == en_passant and self.board[row + direc][col - 1].isupper() != player_turn:
                moves.append((row + direc, col - 1))
        
        return moves

    def get_piece_moves(self, row, col, piece_str):
        piece_str = piece_str.lower()
        if piece_str == "r":
            directions = [(1,0), (0,1), (-1, 0), (0, -1)]   # down, up, left, right
            depth = 8
        elif piece_str == "b":
            directions = [(1,1), (-1,1), (-1, 1), (-1, -1)]   # down, up, left, right
            depth = 8
        elif piece_str == "n":
            directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]   # topleft, 
            depth = 1
        elif piece_str == "q" or piece_str == "k":
            directions =  [(1, 1), (-1, 1), (-1, 1), (-1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)]
            depth = 8 if piece_str == "queen" else 1
        elif piece_str == "p":
            return self.get_pawn_moves(row, col)

        else:
            print("error. piece str = ", piece_str)
            return []

        valid_moves = []

        for direc in directions:
            r = direc[0]
            c = direc[1]
            # loop each direction until you hit the end of board or a piece
            temp_depth = depth
            while (0 <= row + r < 8) and (0 <= col + c < 8) and temp_depth > 0:
                p = self.board[row + r][col + c]
                if p != "-":    # run into a piece
                    piece_color = p.isupper()
                    same_color = piece_color == self.bool_turn
                    if same_color:
                        break
                    else:
                        valid_moves.append((row + r, col + c))
                        break
                else:
                    valid_moves.append((row + r, col + c))
                r += direc[0]
                c += direc[1]
                temp_depth -= 1

        return valid_moves

    def get_king_position(self, current_player_turn):
        target_king = 'k' if current_player_turn == 0 else 'K'
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == target_king:
                    return r, c
        return None

    def get_valid_moves(self):
        current_player_turn = self.bool_turn
        valid_moves = {}
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece == "-":
                    continue
                if piece.isupper() == current_player_turn:  # is piece white == is turn white
                    a = self.get_piece_moves(r, c, piece)
                    valid_moves[(r,c)] = a

        self.valid_moves = valid_moves
        return valid_moves

    def set_en_passant_square(self, en_passant_square):
        self.enpassant_square = en_passant_square
        # print("En Passant Square = ", en_passant_square)

    def is_checked(self, king_row, king_col): # TODO:
        if king_col == None or king_row == None:
            return False

    def is_insufficient_material(self):  # TODO:
        ''' The insufficient mating material rule says that the game is
            immediately declared a draw if there is no way to end the game in checkmate. 

            There are other combinations that will cause a draw that are not as obvious:

            If both sides have any one of the following, and there are no pawns on the board: 

            A lone king 
            a king and bishop
            a king and knight
        '''
        # TODO: using board state check for the above conditions
        pass

    def archive(self):
        board_str = board_to_string(self.board)
        self.board_history.append(board_str)

        if board_str in self.board_dict:
            self.board_dict[board_str] += 1
            if self.board_dict[board_str] >= 3:
                self.is_three_fold_repetition = True # TODO: this is checking for three fold, do we need another function for it??
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

    def update(self, move):
        move_tuple = translate_move_s2t(move)
        move_from = move_tuple[0]
        move_from_row = move_from[0]
        move_from_col = move_from[1]
        move_to = move_tuple[1]
        move_to_row = move_to[0]
        move_to_col = move_to[1]

        piece_removed = self.board[move_to_row][move_to_col]
        moving_piece = self.board[move_from_row][move_from_col]
        self.board[move_to_row][move_to_col] = moving_piece
        self.board[move_from_row][move_from_col] = '-'

        # En Passant Update
        self.set_en_passant_square(None)
        if moving_piece == 'p' and abs(move_from_row - move_to_row) == 2:
            middle_row = (move_from_row + move_to_row) // 2
            self.set_en_passant_square((middle_row, move_from_col))

        # Promotion Logic (auto-queen)
        if moving_piece == 'p' and move_to_row == 7:
            self.board[move_to_row][move_to_col] = 'q'

        if moving_piece == 'P' and move_to_row == 0:
            self.board[move_to_row][move_to_col] = 'Q'

        self.update_castling_rights()
        self.archive()
        self.turn += 1
        self.bool_turn = not self.bool_turn

        return self.board

    def end_game(self, status_string, winner_player=-1):
        print(f"Game Ended in {status_string}. Player {winner_player} wins!")     # TODO: player_turn doesnt matter if stalemate
        time.sleep(1000)
        sys.exit()

    def handle_end_game(self):
        # if there are no valid moves, it's either checkmate and stalemate
        if self.valid_moves == []:
            king_row, king_col = self.get_king_position(self.bool_turn)
            
            if self.is_checked(king_row, king_col, self.bool_turn):
                self.end_game("checkmate", not self.bool_turn)
            
            else:
                self.end_game("stalemate") #TODO: remove this? it would exit file before checking three fold or other endgame conditions

        # if there are valid moves, check for other enforced endgame conditions
        if self.get_three_fold_repetition() or self.get_insufficient_material() or self.get_fifty_moves(): 
            self.end_game("stalemate")