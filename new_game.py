import eric_AI as eric_bot
import nick_AI as nick_bot
import time
import sys
import os
import numpy as np
from pprint import pprint

# BLACK = 1 = UPPER
# WHITE = 0 = LOWER

# TODO: make 'game_state' class that tracks board_state, turn_num, player_turn, en passant logic, move_archives, 

# TODO: should everything be global? If so, how do we handle graphics. If not, where is the line between in and out of class?

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

def string_to_board() -> np.array:
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

def print_board(board: np.array=None):
    if board is None:
        global board_state
        pprint(board_state)
    else:
        pprint(board)

def row_col_to_pos(row: int, col: int) -> str:
    ''' Converts row and col to chess position 
        example: row 0, col 0 -> A1
                row 7, col 7 -> H8
    '''
    ans = ""
    ans += chr(col + 65)
    ans += str(row + 1)
    return ans

def pos_to_row_col(notation: str) -> (int, int):
    ''' Converts string into a tuple of row and col
        example: A1 -> (0, 0)
                H8 -> (7, 7)
    '''
    col = ord(notation[0]) - 65
    row = int(notation[1]) - 1

    return (row, col)

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
    pass

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

    time.wait(1000)

    sys.exit()

###############################################################
# BOARD STATE FUNCTIONS
###############################################################

def convert_update_and_evaluate_archive(board_state):

    # get current board as a string
    board_str = board_to_string(board_state)

    # update history
    board_history.append(board_str)

    # evaluate history for three fold repetition
    if board_state_dict[board_str] in board_state_dict.keys():
        
        board_state_dict[board_str] += 1
        
        if board_state_dict[board_str] >= 3:
            return True
    
    else:
        board_state_dict[board_str] = 1

    return False

def get_valid_moves(board_state, current_player_turn):
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

# TODO: states
def get_moves_and_verify(board_state, current_player_turn):

    valid_moves_arr = get_valid_moves(board_state, current_player_turn)

    # checkmates and stalemates
    if valid_moves_arr == []:
        king_row, king_col = get_king_position(current_player_turn)
        
        if is_checked(board_state, king_row, king_col, current_player_turn):
            end_game("checkmate", not current_player_turn)
        
        else:
            end_game("stalemate")
        
            is_three_fold_repetition = convert_update_and_evaluate_archive(board_state)

            if is_three_fold_repetition:
                end_game("stalemate")
            
            if is_insufficient_material():
                end_game("stalemate")
            
            if is_fifty_move_rule():
                end_game("stalemate")
    
    return valid_moves_arr

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

def update_board(move):
    # TODO: update board based on move
    # TODO: promotion logic
    # TODO: reset/update EN PASSANT
    pass

def draw_board():
    # TODO: interact with pygame (part of decision with code layout)
    pass

def run():
    # Initialize board state and turn counter 
    board_state = init_empty_board()
    turn = 0

    get_valid_moves(board_state, 0)

    
    # remove this
    import eric_AI_2 as dummyai
    dummy_ai = dummyai.AI(board_state)
    exit()
    # end remove


    # Check and verify initial board state
    valid_moves, endgame_status = get_moves_and_verify()

    p1 = eric_bot.AI()
    p2 = nick_bot.AI()

    players = (p1, p2)

    while True:
        
        # Determine whose color it is
        current_player_turn = turn % 2

        # Get move from player ai
        move = players[current_player_turn].get_move()

        # Check if move is valid
        if move in valid_moves:
            
            # Update game board state
            board_state = update_board(move)
            
            # Checks new board state for valid moves
            # Also verifies game status for an endgame condition
            valid_moves, endgame_status = get_moves_and_verify(board_state, current_player_turn)

            # Send updated move to the other player ai
            players[not current_player_turn].recieve_opponent_move(move)

        # Update turn counter
        turn += 1

if __name__ == "__main__":
    run()