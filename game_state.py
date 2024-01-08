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
        self.time_control = 10 * 60

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
        # move = translate_move_s2t(move)
        self.board, self.en_passant = make_move(self.board, move)

        self.update_castling_rights()
        self.archive()
        self.turn_num += 1
        self.player_turn = not self.player_turn

    def get_pawn_moves(self, board_, row, col):
        if self.player_turn == 0:
            direc = 1
            starting_row = 1
        else:
            direc = -1
            starting_row = 7

        moves = []

        # advances
        if 0 <= row + direc < 8 and board_[row + direc][col] == "-":
            moves.append((row + direc, col))
            if row == starting_row and board_[row + 2 * direc][col] == "-":
                moves.append((row + 2 * direc, col))

        # captures
        if col + 1 < 8:
            # right captures
            if 0 <= row + direc < 8 and board_[row + direc][col + 1] != "-" and board_[row + direc][col + 1].isupper() != self.player_turn:
                moves.append((row + direc, col + 1))
            # en passant
            if (row + direc, col + 1) == self.en_passant and 0 <= row + direc < 8 and board_[row + direc][col + 1].isupper() != self.player_turn:
                moves.append((row + direc, col + 1))

        if col - 1 >= 0:
            # left captures
            if 0 <= row + direc < 8 and board_[row + direc][col - 1] != "-" and board_[row + direc][col - 1].isupper() != self.player_turn:
                moves.append((row + direc, col - 1))
            # en passant
            if (row, col - 1) == self.en_passant and 0 <= row + direc < 8 and board_[row + direc][col - 1].isupper() != self.player_turn:
                moves.append((row + direc, col - 1))

        return moves

    def get_piece_moves(self, board_, row, col, piece_str, player_turn):
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
            return self.get_pawn_moves(board_, row, col)

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
                p = board_[row + r][col + c]
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

    def get_king_position(self, board_, player_turn_):
        target_king = 'K' if player_turn_ == 0 else 'k'
        for r in range(8):
            for c in range(8):
                if board_[r][c] == target_king:
                    return r, c
        return None

    def is_king_safe(self, board_, player_turn_):
        king_row_col = self.get_king_position(board_, player_turn_)
        king_row, king_col = king_row_col[0], king_row_col[1]

        # see if pieces are lined up with king
        opp_pieces = ['q', 'n', 'b', 'r', 'k']
        if player_turn_ == 1:
            opp_pieces = ['Q', 'N', 'B', 'R', 'K']

        for opp_piece_char in opp_pieces:
            a = self.get_piece_moves(board_, king_row, king_col, opp_piece_char, not player_turn_)
            # print(f"\tKing | {opp_piece_char} | {a}")
            for r_c in a:
                if board_[r_c[0]][r_c[1]] == opp_piece_char:
                    # print(f"\tFound opponent piece at {r_c[0]}, {r_c[1]}")
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
                # print("\tPawn Attack")
                return False
            if 0 <= king_col + 1 < 8 and board_[king_row + row_dir][king_col + 1] == opp_pawn:
                # print("\tPawn Attack 2")
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
        white_count = 0
        black_count = 0
        for row in self.board:
            for el in row:
                if el == "-":
                    continue
                c = el.lower()
                if c == "p" or c == "q" or c == "r":
                    return False
                elif el == "B" or el == "N":
                    white_count += 1
                    if white_count >= 2:
                        return False
                elif el == "b" or el == "n":
                    black_count += 1
                    if black_count >= 2:
                        return False
        
        return True

    def is_fifty_move_rule(self):
        # TODO
        pass

    def end_game(self, status_string, winner_player=-1):
        print(
            f"Game Ended in {status_string}. Player {winner_player} wins!")  # TODO: player_turn doesnt matter if stalemate

        time.sleep(1000)

        sys.exit()

    def validate_valid_moves(self, valid_moves_dict):
        # for el in self.board:
        #     print(el)
        # print("\n")
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
                potential_board, _ = make_move(board_copy, move)
                if self.is_king_safe(potential_board, not self.player_turn):
                    arr.append(end)
                #     print("+", end=" ")
                # else:
                #     print("-", end=" ")

                # print(f"{potential_board[end[0]][end[1]]} {start} => {end}")

            new_dict[start] = arr

        # print("\n-------------------\n")
        return new_dict

    def get_valid_moves(self):
        valid_moves = {}
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece == "-":
                    continue
                if piece.isupper() == self.player_turn:  # is piece white == is turn white
                    a = self.get_piece_moves(self.board, r, c, piece, self.player_turn)
                    valid_moves[(r, c)] = a

        validated_valid_moves = self.validate_valid_moves(valid_moves)
        return validated_valid_moves

    def handle_end_game(self, valid_moves):
        # if there are no valid moves, it's either checkmate and stalemate
        no_valid_moves = True
        for k in valid_moves:
            if valid_moves[k] != []:
                no_valid_moves = False
        
        if no_valid_moves:
            # king_row, king_col = self.get_king_position(self.board, self.player_turn)

            if self.is_king_safe(self.board, self.player_turn):
                print("Checkmate")
                self.end_game("checkmate", not self.player_turn)

            else:
                print("No valid moves")
                self.end_game("stalemate")

        if self.is_three_fold_repetition:
            print("3 fold repitition")
            self.end_game("stalemate")

        if self.is_insufficient_material():
            print("Insufficient Material")
            self.end_game("stalemate")

        if self.is_fifty_move_rule():
            print("50 move rule")
            self.end_game("stalemate")
        
    def get_player_turn(self):
        return self.player_turn
    
    def tick(self):        
        # Capture elapsed time
        t = time.monotonic() - self.start_time
        self.start_time = time.monotonic()

        # update players time
        if self.player_turn: self.time_white += t
        else: self.time_black += t

        # update times
        self.time = (self.time_control - self.time_white, self.time_control - self.time_black)

# Debugging
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
