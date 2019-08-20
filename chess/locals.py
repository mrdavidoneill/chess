from pygame.locals import *                 # for using pygame keywords like QUIT or KEYDOWN

###################### CHESS LOGIC KEYWORDS #######################

WHITE = "w"
BLACK = "b"

KING = "king"
QUEEN = "queen"
ROOK = "rook"
BISHOP = "bishop"
KNIGHT = "knight"
PAWN = "pawn"

PIECES = KING, QUEEN, ROOK, BISHOP, KNIGHT, PAWN

EMPTY = " - "

FILE = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
RANK = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7}

TO_FILE = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
TO_RANK = {0: "1", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6", 6: "7", 7: "8"}

N = [1, 0]
S = [-1, 0]
W = [0, -1]
E = [0, 1]
SE = [-1, 1]
NW = [1, -1]
SW = [-1, -1]
NE = [1, 1]

DRAW = "draw"
STALEMATE = "stalemate"
CHECKMATE = "checkmate"

PROMOTE = "promote"

###################### PYGAME KEYWORDS #######################


# =========== COLOURS =========== #
DARK = (125, 135, 150)
LIGHT = (232, 235, 239)
RED = (100, 0, 0)
RED_T = (100, 0, 0, 180)
YELLOW = (100, 100, 0)
YELLOW_T = (200, 200, 0, 180)
