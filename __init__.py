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
    ans += chr(start_col + 65)
    ans += str(start_row + 1)
    ans += chr(end_col + 65)
    ans += str(end_row + 1)

    # print(ans)
    return ans

def translate_move_s2t(notation: str) -> (int, int):
    ''' Converts string into a tuple of row and col
        example: A1 -> (0, 0)
                H8 -> (7, 7)
        NOTE: Assumes "A1H8" (capital)
    '''
    start_col = ord(notation[0]) - 65
    start_row = int(notation[1]) - 1

    end_col = ord(notation[2]) - 65
    end_row = int(notation[3]) - 1

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
    empty_array = [
        ['-', '-', '-', '-', '-', '-', '-', '-'], 
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-'], 
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-'], 
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-'], 
        ['-', '-', '-', '-', '-', '-', '-', '-']
    ]
    puzzle_1 = [
        ['r', 'b', '-', '-', '-', 'r', 'k', '-'], 
        ['p', 'p', '-', 'q', '-', 'p', 'p', 'p'],
        ['-', '-', 'n', '-', '-', '-', '-', '-'], 
        ['-', 'N', 'p', 'p', '-', '-', 'N', '-'],
        ['-', '-', '-', '-', '-', '-', '-', 'P'], 
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['P', 'P', 'P', '-', 'Q', 'P', 'P', '-'], 
        ['-', '-', 'K', 'R', '-', '-', '-', 'R']
    ]
    puzzle_2 = [
        ['r', '-', '-', '-', 'k', '-', '-', 'r'], 
        ['p', 'p', 'p', '-', '-', 'p', 'p', 'p'],
        ['-', '-', 'n', '-', '-', '-', '-', '-'], 
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', 'B', 'P', 'p', '-', 'n', '-'], 
        ['-', '-', 'N', '-', 'P', '-', '-', '-'],
        ['P', 'P', '-', '-', '-', '-', 'P', 'q'], 
        ['R', '-', 'B', 'Q', 'R', 'K', '-', '-']
    ]
    
    return puzzle_1

def evaluate_board(board):
    # Evaluate based on piece values
    piece_values = {'P': 1, 'N': 3, 'B': 3.25, 'R': 5, 'Q': 9, 'K': 100}
    total_value = 0

    for row in board:
        for square in row:
            if square.islower():  # White piece
                total_value += piece_values[square.upper()]
            elif square.isupper():  # Black piece
                total_value -= piece_values[square]

    return total_value

def make_move(board, move):
    # given a board array and move of notation "A1H8", make the move and return the new board
    # handles en_passant (returns the square if relevant) and promotion
    if type(move) == str:
        start, end = translate_move_s2t(move)
    else:
        start, end = move[0], move[1]

    board[end[0]][end[1]] = board[start[0]][start[1]]
    board[start[0]][start[1]] = '-'

    # En Passant Update
    en_passant = None
    if board[end[0]][end[1]] == 'p' and abs(end[0] - start[0]) == 2:
        middle_row = (start[0] + end[0]) // 2
        en_passant = (middle_row, start[1])

    # Promotion Logic (auto-queen)
    if board[end[0]][end[1]] == 'p' and end[0] == 7:
        board[end[0]][end[1]] = 'q'

    if board[end[0]][end[1]] == 'P' and end[0] == 0:
        board[end[0]][end[1]] = 'Q'

    return board, en_passant
           


if __name__ == "__main__":
    import time

    b = init_empty_board()
    print_board(b)    
    print(evaluate_board(b))

    b, _ = make_move(b, "A2A3")
    print_board(b)
    print(evaluate_board(b))
    
    b, _ = make_move(b, "A1B1")
    print_board(b)
    print(evaluate_board(b))
    
    b, _ = make_move(b, "B1C1")
    print_board(b)
    print(evaluate_board(b))

    b, _ = make_move(b, "D1D8")
    print_board(b)
    print(evaluate_board(b))