import eric_AI as eric_bot
import nick_AI as nick_bot
import time
import sys
import numpy as np
from pprint import pprint
from game_state import GameState
from graphics import Graphics

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

# Board State should be a string representing the current position of pieces on the board
board_state = []
board_string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

# Board History is used to keep track of the moves played
board_history = ["board_state_1", "board_state_2", "board_state_1"]

# Board State Dict is used to keep track of the number of times a board state has existed during the game
board_state_dict = {"board_state_1": 3, "board_state_2":1}

###############################################################
# HELPER FUNCTIONS
###############################################################

def board_to_string() -> str:
    string = ""

    for row in range(8):
        
        space_count = 0
        
        for col in range(8):
            
            letter = board_state[row][col]
            
            # if space, keep count and add count once a piece is found
            if letter == "-":
                space_count += 1
            
            # if piece, add count if there was a space before it, then add piece
            else:
                if space_count > 0:
                    string += str(space_count)
                string += letter

        # end of row also resets space count
        if space_count > 0:
            string += str(space_count)

        # terminate row with "/" except for last row
        if row != 7:
            string += "/"

    return string

def string_to_board():
    arr = np.empty([8,8], dtype=object)

    # split string into "/"
    string_rows = board_string.split("/")

    for row in range(8):
        string_row = string_rows[row]
        col = 0
        
        for letter in string_row:

            # if the letter in the row is a number, we skip that many positions in the array
            if letter.isnumeric():
                
                skip = int(letter)
                
                # add - for every empty space
                for i in range(skip):
                    arr[row][col] = "-"
                    col += 1
            
            # if the letter is not numeric we add it to the array
            else:
                
                arr[row][col] = letter
                col += 1

    return arr

def print_board(board=None):
    pprint(board)

def translate_move_t2s(start_row: int, start_col: int, end_row: int, end_col: int) -> str:
    ''' Converts row and col to chess position 
        example: row 0, col 0 -> A1
                row 7, col 7 -> H8
    '''
    ans = ""
    ans += chr(start_row + 65)
    ans += str(start_row + 1)
    ans += chr(end_row + 65)
    ans += str(end_col + 1)
    return ans

def translate_move_s2t(notation: str) -> (int, int):
    ''' Converts string into a tuple of row and col
        example: A1 -> (0, 0)
                H8 -> (7, 7)
    '''
    start_col = ord(notation[0]) - 65
    start_row = int(notation[1]) - 1

    start_col = ord(notation[2]) - 65
    start_row = int(notation[3]) - 1

    return (start_row, start_col), (start_row, start_col)

def get_pawn_moves(board_state, row, col, player_turn):
    pass

def get_piece_moves(board_state, row, col, player_turn, piece_str):
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
        return get_pawn_moves(board_state, row, col, player_turn)

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
            p = board_state[row + r][col + c]
            if p != "-":    # run into a piece
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

def get_king_position(current_player_turn):
    target_king = 'k' if current_player_turn == 0 else 'K'
    for r in range(8):
        for c in range(8):
            if board_state[r][c] == target_king:
                return r, c
    return None

###############################################################
# ENDGAME CONDITIONS
###############################################################

def is_checked(board_state, king_row, king_col, player_turn):
    if king_col == None or king_row == None:
        return False

def is_insufficient_material():
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

def is_fifty_move_rule():
    pass

def end_game(status_string, winner_player=-1):

    print(f"Game Ended in {status_string}. Player {winner_player} wins!")     # TODO: player_turn doesnt matter if stalemate

    time.sleep(1000)

    sys.exit()

###############################################################
# BOARD STATE FUNCTIONS
###############################################################

def get_valid_moves(board_state, current_player_turn, en_passant_square=None):
    current_player_turn
    valid_moves_arr = []
    for r in range(8):
        for c in range(8):
            piece = board_state[r][c]
            if piece == "-":
                continue
            if piece.isupper() == current_player_turn:  # is piece white == is turn white
                a = get_piece_moves(board_state, r, c, current_player_turn, piece)
                valid_moves_arr.append( a )
                print(piece, ":", a)

    # print(valid_moves_arr)
    return valid_moves_arr

def handle_end_game(board_state, gs, valid_moves, current_player_turn):
    # if there are no valid moves, it's either checkmate and stalemate
    if valid_moves == []:
        king_row, king_col = get_king_position(current_player_turn)
        
        if is_checked(board_state, king_row, king_col, current_player_turn):
            end_game("checkmate", not current_player_turn)
        
        else:
            end_game("stalemate") #TODO: remove this? it would exit file before checking three fold or other endgame conditions

    # if there are valid moves, check for other enforced endgame conditions
    # is_three_fold_repetition = convert_update_and_evaluate_archive(board_state)
    is_three_fold_repetition = gs.get_three_fold_repetition()

    if is_three_fold_repetition:
        end_game("stalemate")
    
    if is_insufficient_material():
        end_game("stalemate")
    
    if is_fifty_move_rule():
        end_game("stalemate")

###############################################################
# GAME FUNCTIONS
###############################################################

def init_empty_board():
    init_array = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['-', '-', '-', '-', '-', '-', '-', '-'], 
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-'], 
        ['-', '-', '-', '-', '-', '-', '-', '-'], 
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'], 
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
    ]
    return init_array

def update_board(board_state, move, gs):
    # TODO: update board based on move
    # TODO: promotion logic
    # TODO: reset/update EN PASSAN
    # TODO: update castling rights

    # get new board

    gs.update(board_state, en_passant=None)
    return new_board_state

def run():
    # Initialize board state and turn counter 
    board_state = init_empty_board() 
    gs = GameState()
    graphics = Graphics()

    # Check and verify initial board state
    valid_moves = get_valid_moves(board_state, gs.get_player_turn())

    p1 = eric_bot.AI()
    p2 = nick_bot.AI()

    players = (p1, p2)

    while True:
        # Get move from player ai
        move = players[gs.get_player_turn()].get_move()

        # Check if move is valid
        # TODO: fix
        # if translate_move(move.end) in get_piece_moves(board_state, translate_move(move.start), col, player_turn, 'N'):
        if move in valid_moves: 
        
            # Update game board state
            board_state = update_board(move, gs)
            graphics.draw(board_state)
            
            # Checks new board state for valid moves
            valid_moves = get_valid_moves(board_state, gs.get_player_turn(), gs.enpassant_square)

            # Check for endgame conditions
            handle_end_game(board_state, gs, valid_moves, gs.get_player_turn())

            # Send updated move to the other player ai
            players[not gs.get_player_turn()].recieve_opponent_move(move)

if __name__ == "__main__":
    run()