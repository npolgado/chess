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
        self.start_time = time.monotonic()
        self.time_white = 0
        self.time_black = 0

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

        move = translate_move_s2t(move)
        self.board, self.en_passant = make_move(self.board, move)

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
        if 0 <= row + direc < 8 and self.board[row + direc][col] == "-":
            moves.append((row + direc, col))
            if row == starting_row and self.board[row + 2 * direc][col] == "-":
                moves.append((row + 2 * direc, col))

        # captures
        if col + 1 < 8:
            # right captures
            if 0 <= row + direc < 8 and self.board[row + direc][col + 1] != "-" and self.board[row + direc][col + 1].isupper() != self.player_turn:
                moves.append((row + direc, col + 1))
            # en passant
            if (row + direc, col + 1) == self.en_passant and 0 <= row + direc < 8 and self.board[row + direc][col + 1].isupper() != self.player_turn:
                moves.append((row + direc, col + 1))

        if col - 1 >= 0:
            # left captures
            if 0 <= row + direc < 8 and self.board[row + direc][col - 1] != "-" and self.board[row + direc][col - 1].isupper() != self.player_turn:
                moves.append((row + direc, col - 1))
            # en passant
            if (row, col - 1) == self.en_passant and 0 <= row + direc < 8 and self.board[row + direc][col - 1].isupper() != self.player_turn:
                moves.append((row + direc, col - 1))

        return moves

    def get_piece_moves(self, row, col, piece_str, player_turn):
        piece_str = piece_str.lower()
        if piece_str == "r":
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # down, up, left, right
            depth = 8
        elif piece_str == "b":
            directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]  # down, up, left, right
            depth = 8
        elif piece_str == "n":
            directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]  # top left,
            depth = 1
        elif piece_str == "q":
            depth = 8
            directions = [(1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)]
        elif piece_str == "k":
            directions = [(1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)]
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
                    same_color = piece_color == player_turn
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

    def get_king_position(self, player_turn_, board_):
        target_king = 'K' if player_turn_ == 0 else 'k'
        for r in range(8):
            for c in range(8):
                if board_[r][c] == target_king:
                    return r, c
        return None

    def is_king_safe(self, board_, player_turn_):
        king_row_col = self.get_king_position(player_turn_, board_)

        print("King RC:", king_row_col)
        # BLACK = 1 = UPPER
        # WHITE = 0 = LOWER
        print("Turn:", "Black (1)" if player_turn_ else "White (0)")

        king_row, king_col = king_row_col[0], king_row_col[1]

        # see if pieces are lined up with king
        opp_pieces = ['q', 'n', 'b', 'r', 'k']
        if player_turn_ == 1:
            opp_pieces = ['Q', 'N', 'B', 'R', 'K']

        for opp_piece_char in opp_pieces:
            a = self.get_piece_moves(king_row, king_col, opp_piece_char, not player_turn_)
            for r_c in a:
                if board_[r_c[0]][r_c[1]] == opp_piece_char:
                    # print(f"{opp_piece_char} checks at {r_c}")
                    return False

        # pawns
        if player_turn_ == 0:
            row_dir = -1
            opp_pawn = 'p'
        else:
            row_dir = 1
            opp_pawn = 'P'

        if 0 <= king_row + row_dir < 8:
            if 0 <= king_col - 1 < 8 and board_[king_row + row_dir][king_col - 1] == opp_pawn:
                # print(f"Pawn checks at {king_row + row_dir}, {king_col - 1}")
                return False
            if 0 <= king_col + 1 < 8 and board_[king_row + row_dir][king_col + 1] == opp_pawn:
                # print(f"Pawn checks at {king_row + row_dir}, {king_col + 1}")
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

    def end_game(self, status_string, winner_player=-1):
        print(
            f"Game Ended in {status_string}. Player {winner_player} wins!")  # TODO: player_turn doesnt matter if stalemate

        time.sleep(1000)

        sys.exit()

    def validate_valid_moves(self, valid_moves_dict):
        print("\n-------------------\n")
        for key in valid_moves_dict:
            print(self.board[key[0]][key[1]], ":", valid_moves_dict[key])
        for el in self.board:
            print(el)

        new_dict = {}
        for start in valid_moves_dict.keys():
            arr = []
            for end in valid_moves_dict[start]:
                board_copy = []
                for row in self.board:
                    a = []
                    for el in row:
                        a.append(el)
                    board_copy.append(a)

                move = (start, end)
                print(f"Move: {move}, !Player = {not self.player_turn}")
                potential_board, en_passant = make_move(board_copy, move)
                for el in potential_board:
                    print(el)
                if self.is_king_safe(potential_board, not self.player_turn):
                    print(f"King Safe")
                    arr.append(end)
                else:
                    print(f"NOT Safe")

                print("\n---------------------\n")

            new_dict[start] = arr
            print(self.board[start[0]][start[1]], ":", arr)

        return new_dict

    def get_valid_moves(self):
        valid_moves = {}
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece == "-":
                    continue
                if piece.isupper() == self.player_turn:  # is piece white == is turn white
                    a = self.get_piece_moves(r, c, piece, self.player_turn)
                    valid_moves[(r, c)] = a

        validated_valid_moves = self.validate_valid_moves(valid_moves)
        # print("Black" if self.player else "White")
        # for el in self.board:
        #     print(el)
        # print(valid_moves)
        # print("------")
        # print(validated_valid_moves)
        # print("\n\n\n")
        return validated_valid_moves

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
    


    def tick(self):
        # # start time if it is turn 1
        # if self.turn == 0:
        #     self.start_time = time.monotonic()
        # else:
        
        # Capture elapsed time
        t = time.monotonic() - self.start_time
        self.start_time = time.monotonic()

        # update players time
        if self.player_turn: self.time_white += t
        else: self.time_black += t

        # update time
        self.time = (self.time_white,self.time_black)


if __name__ == "__main__":
    test = [
        ['-', 'n', 'b', '-', '-', '-', 'r', '-'],
        ['-', '-', 'p', '-', 'b', '-', 'k', '-'],
        ['-', '-', 'p', 'p', '-', 'p', '-', '-'],
        ['-', '-', '-', '-', '-', '-', 'P', '-'],
        ['-', '-', '-', '-', '-', 'R', 'P', '-'],
        ['-', '-', 'P', '-', 'P', 'P', '-', '-'],
        ['Q', 'P', '-', '-', 'K', '-', '-', '-'],
        ['r', '-', 'B', '-', '-', '-', '-', 'q']
    ]
    gs = GameState()
    gs.board = test
    print(gs.is_king_safe(gs.board, 0))
