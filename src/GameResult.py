from enum import Enum

class GameResult(Enum):
    '''
    Static vars to represent different game states
    '''
    NOT_FINISHED = 0
    RED_WIN = 1
    BLACK_WIN = -1
    DRAW = 2
