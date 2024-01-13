import random
from __init__ import *
import copy
import threading
import time
# Agent that plays chess

move = None

class AI (threading.Thread):

    def run(self):
        self.move = 0
        while True:
            print("Move:", self.move)
            time.sleep(1)
    

    def get_ai_move(self, valid_moves) -> tuple:

        count = 0
        for key in valid_moves:
            count += len(valid_moves[key])

        if count > 0:
            random_index = random.choice(range(count))
        else:
            return None

        for key in valid_moves:
            for value in valid_moves[key]:
                if random_index == 0:
                    random_move = (key, value)
                random_index -= 1

        move = translate_move_t2s(random_move[0][0], random_move[0][1], random_move[1][0], random_move[1][1])

        self.move = move
        return move

    def receive(self, move):
        print(f"Received {move}")