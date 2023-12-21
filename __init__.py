import numpy as np
from pprint import pprint

def board_to_string(board_state) -> str:
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
                    space_count = 0
                string += letter

        # end of row also resets space count
        if space_count > 0:
            string += str(space_count)

        # terminate row with "/" except for last row
        if row != 7:
            string += "/"

    # print(string)
    return string

def string_to_board(board_string):
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
    ans += str(start_col + 1)
    ans += chr(end_row + 65)
    ans += str(end_col + 1)

    # print(ans)
    return ans

def translate_move_s2t(notation: str) -> (int, int):
    ''' Converts string into a tuple of row and col
        example: A1 -> (0, 0)
                H8 -> (7, 7)
        NOTE: Assumes "A1H8" (capital)
    '''
    start_row = ord(notation[0]) - 65
    start_col = int(notation[1]) - 1

    end_row = ord(notation[2]) - 65
    end_col = int(notation[3]) - 1

    # print((start_row, start_col), (end_row, end_col))
    return (start_row, start_col), (end_row, end_col)

def init_empty_board():
    # TODO: was this meant to be oriented as if you were white or black? right now it is black
    init_array = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['-', '-', '-', '-', '-', '-', '-', '-'], 
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-'], 
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    ]
    return init_array

def evaluate_board(board):
    # given the board and player's turn, return a score

    vals = {
        'p': 1,
        'n': 3,
        'b': 3,
        'r': 5,
        'q': 9,
        'k': 0
    }

    ans = 0

    for i in range(8):
        for j in range(8):
            piece = board[i][j]

            if piece == '-':
                continue

            if piece.isupper():
                key = piece.lower()
                ans -= vals[key]
            else:
                ans += vals[piece]
    
    return ans

def make_move(board, move):
    # given a board array and move of notation "A1H8", make the move and return the new board
    # NOTE: this accesses the board in col, row format
    start, end = translate_move_s2t(move)
    board[end[1]][end[0]] = board[start[1]][start[0]]
    board[start[1]][start[0]] = '-'
    return board

if __name__ == "__main__":
    import time

    b = init_empty_board()
    print_board(b)    
    print(evaluate_board(b))

    b = make_move(b, "A2A3")
    print_board(b)
    print(evaluate_board(b))
    
    b = make_move(b, "A1B1")
    print_board(b)
    print(evaluate_board(b))
    
    b = make_move(b, "B1C1")
    print_board(b)
    print(evaluate_board(b))