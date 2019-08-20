from locals import *

class Piece:
    SIZE = 20

    def __init__(self, _id, rank=None, file=None):
        self._id = _id
        self.rank = rank
        self.file = file

        # Set colour
        if _id.isupper():
            self.colour = WHITE
        else:
            self.colour = BLACK

        # Set piece movements #
        # King
        if _id.lower() == "k":
            self.movements = [N, NE, E, SE, S, SW, W, NW]
            self.max_distance = 1
            self.name = KING

        # Queen
        if _id.lower() == "q":
            self.movements = [N, NE, E, SE, S, SW, W, NW]
            self.max_distance = 8
            self.name = QUEEN

        # Rook
        if _id.lower() == "r":
            self.movements = [N, E, S, W]
            self.max_distance = 8
            self.name = ROOK

        # Bishop
        if _id.lower() == "b":
            self.movements = [NE, SE, SW, NW]
            self.max_distance = 8
            self.name = BISHOP

        # Knight
        if _id.lower() == "n":
            self.movements = [[2, -1], [2, 1], [-2, -1], [-2, 1],
                              [1, -2], [1, 2], [-1, -2], [-1, 2]]
            self.max_distance = 1
            self.name = KNIGHT

        # Pawn
        if _id.lower() == "p":
            # If white
            if self.colour == WHITE:
                self.normal_movements = [N]
                self.capture_movements = [NE, NW]
            else:
                self.normal_movements = [S]
                self.capture_movements = [SE, SW]
            self.movements = []
            self.movements.extend(self.normal_movements)
            self.movements.extend(self.capture_movements)
            self.max_distance = 1
            self.name = PAWN

        self.image = f"{self.name}_{self.colour}"


    def __repr__(self):
        """ Print pgn letter name when printing to screen the board """
        return " " + self._id + " "
