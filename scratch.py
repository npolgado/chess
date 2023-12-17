

an_passant = (3, 4)

    
def get_pawn_moves(board_state, row, col, player_turn):

    if player_turn == 0:    # white - top to bottom
        poss_advances = (row + 1, col)
        poss_attacks = (row + 1, col + 1), (row + 1, col - 1)
        if row == 1:
            poss_advances.append(row + 2, col)






board_state = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], 
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['R', 'N', 'N', 'Q', 'K', 'B', 'N', 'R'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']]


print(get_pawn_moves(board_state, 7, 7, 0))