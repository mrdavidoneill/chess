from locals import *
from pieces import Piece

class Board:
    SQUARE_SIZE = 20
    DARK_COLOUR = (50, 50, 50)
    LIGHT_COLOUR = (150, 150, 150)
    FILES = RANKS = 8
    PIECES_START = ["r","n","b","q","k","b","n","r"]

    def __init__(self, arr=None):
        if not arr:
            self.set_up_pieces()
        else:
            self.import_board(arr)


    def clear_board(self):
        """ Wipes pieces from the board """
        self.BOARD = []
        for row in range(self.RANKS):
            self.BOARD.append([EMPTY for n in range(self.FILES)])

    def set_up_pieces(self):
        """ Clears board and places positions at start positions """
        self.clear_board()

        self.BOARD[0] = [Piece(piece.upper(), rank=0, file=i) for i, piece in
                        enumerate(self.PIECES_START)]
        self.BOARD[1] = [Piece("P", rank=1, file=i) for i in range(self.FILES)]
        self.BOARD[6] = [Piece("p", rank=6, file=i) for i in range(self.FILES)]
        self.BOARD[7] = [Piece(piece.lower(), rank=7, file=i) for i, piece in
                        enumerate(self.PIECES_START)]

    def import_board(self, arr):
        """ Imports 2d array or another Board and creates new Board copy """
        self.clear_board()
        for row, rank in enumerate(arr):
            for col, sq in enumerate(rank):
                # if str arr inputted
                if type(sq) is str:
                    if sq.lower() in Board.PIECES_START:
                        self.BOARD[row][col] = Piece(sq, rank=row, file=col)
                    elif sq.lower() == "p":
                        self.BOARD[row][col] = Piece(sq, rank=row, file=col)
                    else:
                        self.BOARD[row][col] = EMPTY
                # if Piece inputted
                else:
                    self.BOARD[row][col] = Piece(sq._id, rank=row, file=col)




    def print_board(self):
        """ Prints the board to the console """
        print()
        for rank in reversed(self.BOARD):
            for square in rank:
                print(square, end="")
            # Print new line
            print()

    def get_square_occupant(self, square):
        """ Gets occupant of square """
        file = FILE[square[0]]
        rank = RANK[square[1]]
        return self.BOARD[rank][file]

    def place_piece(self, piece, square):
        """ Places piece on board at square specified
            Input piece can be str(K) or Piece
            Input square can be one of:
                - str('E4'),
                - tuple of array coordinates((0,2))
                - Piece with file and rank properties """
        if type(square) is str:
            file = FILE[square[0]]
            rank = RANK[square[1]]
        elif type(square) is Piece:
            file = square.file
            rank = square.rank
        else:
            rank = square[0]
            file = square[1]

        if type(piece) is str:
            piece = Piece(piece, rank=rank, file=file)
        else:
            piece.rank = rank
            piece.file = file

        self.BOARD[rank][file] = piece


    def remove_piece(self, square):
        """ Removes piece from board
            Input can be one of:
                -   str ('E4')
                -   tuple ((0,2))
                -   Piece with file, rank properties """
        if type(square) is str:
            file = FILE[square[0]]
            rank = RANK[square[1]]
        elif type(square) is Piece:
            file = square.file
            rank = square.rank
        else:
            rank = square[0]
            file = square[1]

        self.BOARD[rank][file] = EMPTY

    def locate_piece(self, _id):
        """ Returns tuple of rank and file where piece is located """
        for row, rank in enumerate(self.BOARD):
            for col, piece in enumerate(rank):
                if type(piece) is Piece and piece._id == _id:
                    return piece


    @staticmethod
    def square_name(pos):
        """ Returns square name of 2d array coordinates
         eg. [0,2] returns 'C1' """
        return TO_FILE[pos[1]] + TO_RANK[pos[0]]




if __name__ == "__main__":
    board = Board()
    board.set_up_pieces()
    board.print_board()
    board.place_piece("Q", "E4")
    board.print_board()
    board.remove_piece("D1")
    board.print_board()




