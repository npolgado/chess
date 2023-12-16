

import eric_AI as eric_bot
import nick_AI as nick_bot


board_state = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


# TODO: have we outlined everything?

# TODO: should everything be global? If so, how do we handle graphics. If not, where is the line between in and out of class?



board_history = ["board_state_1", "board_state_2", "board_state_1"]
board_state_dict = {"board_state_1": 3, "board_state_2":1}

def board_to_string():
    pass

def string_to_board():
    pass



def is_insufficient_material():
    pass


def convert_update_and_evaluate_archive(board_state):

    board_str = board_to_string(board_state)

    board_history.append(board_str)

    if board_state_dict[board_str] in board_state_dict.keys():
        board_state_dict[board_str] += 1
        if board_state_dict[board_str] >= 3:
            return True
    else:
        board_state_dict[board_str] = 1

    return False


def get_valid_moves(board_state, current_player_turn):

    # TODO: hard part: evaluate all valid moves
        # en passant
        # pawns direction (and if capture - diagonal)
        # move cant put king in check 
            # loop thru king as every other piece and see if it can capture oppoent of that type
            # evaluated after potential move is made, which is awkward?
            # pins
        # castling - cant move thru check
    pass

def get_check_status():
    pass

# TODO: need logic for whose turn it is
def get_moves_and_verify(board_state, current_player_turn):

    valid_moves_arr = get_valid_moves(board_state, current_player_turn)     # en passant

    # checkmates and stalemates
    if valid_moves_arr == []:
        if get_check_status(board_state):
            end_game("checkmate", not current_player_turn)
        else:
            end_game("stalemate")
        
    is_three_fold_repition = convert_update_and_evaluate_archive(board_state)

    if is_three_fold_repitition:
        end_game("stalemate")
    
    if is_insufficient_material():
        end_game("stalemate")
    
    return valid_moves_arr



def end_game(status_string, player_turn):

    print(f"Game Ended in {status_string}. Player {player_turn} wins!")     # TODO: player_turn doesnt matter if stalemate

    time.wait(1000)

    sys.exit()


def update_board(move):

    # TODO: update board based on move

    # TODO: promotion logic



def draw_board():

def print_board():


# 0 is white, 1 is black

def run():

    board_state = init_empty_board()
    turn = 0

    valid_moves, endgame_status = get_moves_and_verify()

    p1 = eric_bot.AI()
    p2 = nick_bot.AI()

    players = (p1, p2)

    while True:
        
        current_player_turn = turn % 2

        move = players[current_player_turn].get_move()

        if move in valid_moves:
            
            board_state = update_board(move)
            
            valid_moves, endgame_status = get_moves_and_verify(board_state, current_player_turn)

            players[not current_player_turn].recieve_opponent_move(move)

        turn += 1

def main():
    
    run()
