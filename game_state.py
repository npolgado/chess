import numpy as np
import time
import sys

from __init__ import *


class GameState:
    def __init__(self) -> None:
        self.turn_num = 1

        self.player_turn = 0
        self.en_passant = None

        self.board = init_empty_board()

        self.board_history = []
        self.board_dict = {}
        self.is_three_fold_repetition = False
        self.castling_rights = {
            "w_Q": True,
            "w_K": True,
            "b_Q": True,
            "b_K": True
        }

        self.time = (0, 0)

    def update_castling_rights(self) -> None:
        # if the kings or rooks aren't in their starting position, update appropriate castling rights to False (never
        # can be changed to True once False)
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
    
    def get_board_history(self):
        return self.board_history

    def get_three_fold_repetition(self):
        return self.is_three_fold_repetition

    def archive(self):
        board_str = board_to_string(self.board)
        self.board_history.append(board_str)

        if board_str in self.board_dict:
            self.board_dict[board_str] += 1
            if self.board_dict[board_str] >= 3:
                self.is_three_fold_repetition = True
        else:
            self.board_dict[board_str] = 1

    def update(self, move):
        # if no move given, pass
        if move == None:
            return

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
        self.en_passant = None
        if moving_piece == 'p' and abs(move_from_row - move_to_row) == 2:
            middle_row = (move_from_row + move_to_row) // 2
            self.en_passant = (middle_row, move_from_col)

        # Promotion Logic (auto-queen)
        if moving_piece == 'p' and move_to_row == 7:
            self.board[move_to_row][move_to_col] = 'q'

        if moving_piece == 'P' and move_to_row == 0:
            self.board[move_to_row][move_to_col] = 'Q'

        self.update_castling_rights()
        self.archive()
        self.turn_num += 1
        self.player_turn = not self.player_turn

    def get_pawn_moves(self, row, col):
        if self.player_turn == 0:
            direc = 1
            starting_row = 1
        else:
            direc = -1
            starting_row = 7

        moves = []

        # advances
        if self.board[row + direc][col] == "-":
            moves.append((row + direc, col))
            if row == starting_row and self.board[row + 2 * direc][col] == "-":
                moves.append((row + 2 * direc, col))

        # captures
        if col + 1 < 8:
            # right captures
            if self.board[row + direc][col + 1] != "-" and self.board[row + direc][col + 1].isupper() != self.player_turn:
                moves.append((row + direc, col + 1))
            # en passant
            if (row + direc, col + 1) == self.en_passant and self.board[row + direc][col + 1].isupper() != self.player_turn:
                moves.append((row + direc, col + 1))

        if col - 1 >= 0:
            # left captures
            if self.board[row + direc][col - 1] != "-" and self.board[row + direc][col - 1].isupper() != self.player_turn:
                moves.append((row + direc, col - 1))
            # en passant
            if (row, col - 1) == self.en_passant and self.board[row + direc][col - 1].isupper() != self.player_turn:
                moves.append((row + direc, col - 1))

        return moves

    def get_piece_moves(self, row, col, piece_str):
        piece_str = piece_str.lower()
        if piece_str == "r":
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # down, up, left, right
            depth = 8
        elif piece_str == "b":
            directions = [(1, 1), (-1, 1), (-1, 1), (-1, -1)]  # down, up, left, right
            depth = 8
        elif piece_str == "n":
            directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]  # topleft,
            depth = 1
        elif piece_str == "q":
            depth = 8
            directions = [(1, 1), (-1, 1), (-1, 1), (-1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)]
        elif piece_str == "k":
            directions = [(1, 1), (-1, 1), (-1, 1), (-1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)]
            depth = 1
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
                if p != "-":  # run into a piece
                    piece_color = p.isupper()
                    same_color = piece_color == self.player_turn
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

    def get_king_position(self):
        target_king = 'k' if self.player_turn == 0 else 'K'
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == target_king:
                    return r, c
        return None

    def is_checked(self, king_row, king_col):
        # TODO
        if king_col is None or king_row is None:
            return False
        return True

    def is_insufficient_material(self):
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

    def is_fifty_move_rule(self):
        pass

    def end_game(self, status_string, winner_player = -1):
        print(
            f"Game Ended in {status_string}. Player {winner_player} wins!")  # TODO: player_turn doesnt matter if stalemate

        time.sleep(1000)

        sys.exit()

    def get_valid_moves(self):
        valid_moves = {}
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece == "-":
                    continue
                if piece.isupper() == self.player_turn:  # is piece white == is turn white
                    a = self.get_piece_moves(r, c, piece)
                    valid_moves[(r, c)] = a

        return valid_moves

    def handle_end_game(self, valid_moves):
        # if there are no valid moves, it's either checkmate and stalemate
        if valid_moves is []:
            king_row, king_col = self.get_king_position(self.player_turn)

            if self.is_checked(king_row, king_col, self.player_turn):
                self.end_game("checkmate", not self.player_turn)

            else:
                self.end_game("stalemate")
                # TODO: remove this? it would exit file before checking three fold or other endgame conditions
                #   ERIC: No because the game is over since a player has no valid moves

        if self.is_three_fold_repetition:
            self.end_game("stalemate")

        if self.is_insufficient_material():
            self.end_game("stalemate")

        if self.is_fifty_move_rule():
            self.end_game("stalemate")

    def get_player_turn(self):
        return self.player_turn
