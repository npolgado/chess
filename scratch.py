

en_passant = (3, 4)

    
def get_pawn_moves(board_state, row, col, player_turn):
    if player_turn == 0:
        direc = 1
        starting_row = 1
    else:
        direc = -1
        starting_row = 7

    moves = []

    # advances
    if board_state[row + direc][col] == "-":
        moves.append((row + direc, col))
        if board_state[row + 2*direc][col] == "-":
            moves.append((row + 2*direc, col))
    
    # captures
    if col + 1 < 8:
        # right captures
        if board_state[row + direc][col + 1] != "-":
            moves.append((row, col + 1))
        # en passant
        if (row, col+1) == en_passant:
            moves.append((row, col+1))

    if col - 1 >= 0:
        # left captures
        if board_state[row + direc][col - 1] != "-":
            moves.append((row, col - 1))
        # en passant
        if (row, col-1) == en_passant:
            moves.append((row, col - 1))
        
    return moves




board_state = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], 
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['R', 'N', 'N', 'Q', 'K', 'B', 'N', 'R'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']]


print(get_pawn_moves(board_state, 1, 1, 0))