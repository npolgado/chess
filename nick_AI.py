import numpy as np
import threading
import asyncio
import time
import random

class AI :
    def __init__(self):
        self.target_move = None
        
    # has to be non-blocking, return none and thread the processing of the move
    def recieve(self, move: str) -> None:
        self.target_move = None

    def get_target_move(self, valid_moves):
        return self.target_move