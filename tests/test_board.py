import sys, os
testdir = os.path.dirname(__file__)
print(testdir)
srcdir = '../chess'
print(srcdir)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
print(os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
import chess.chess.board
from chess.chess.pieces import Piece
from chess.chess.notation import Notation
from chess.chess.locals import *

STARTING_BOARD = [
                    [Piece('R'), Piece('N'), Piece('B'), Piece('Q'), Piece('K'), Piece('B'), Piece('N'), Piece('R')],
                    [Piece('P'), Piece('P'), Piece('P'), Piece('P'), Piece('P'), Piece('P'), Piece('P'), Piece('P')],
                    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                    [Piece('p'), Piece('p'), Piece('p'), Piece('p'), Piece('p'), Piece('p'), Piece('p'), Piece('p')],
                    [Piece('r'), Piece('n'), Piece('b'), Piece('q'), Piece('k'), Piece('b'), Piece('n'), Piece('r')],
                ]

BOARD_2 = [
                    [Piece('R'), Piece('N'), Piece('B'), Piece('Q'), Piece('K'), Piece('B'), EMPTY, Piece('R')],
                    [Piece('P'), Piece('P'), Piece('P'), Piece('P'), EMPTY, Piece('P'), Piece('P'), Piece('P')],
                    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, Piece('N'), EMPTY, EMPTY],
                    [EMPTY, EMPTY, EMPTY, EMPTY, Piece("P"), EMPTY, EMPTY, EMPTY],
                    [EMPTY, EMPTY, Piece('p'), EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                    [Piece('p'), Piece('p'), EMPTY, Piece('p'), Piece('p'), Piece('p'), Piece('p'), Piece('p')],
                    [Piece('r'), Piece('n'), Piece('b'), Piece('q'), Piece('k'), Piece('b'), Piece('n'), Piece('r')],
                ]

ARR_BOARD = [["R", "N", "B", "Q", "K", "B", "N", "R"],
             ["P", "P", "P", "P", "P", "P", "P", "P"],
             [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
             ["p", "p", "p", "p", "p", "p", "p", "p"],
             ["r", "n", "b", "q", "k", "b", "n", "r"]]

FEN_START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
FEN_2 = "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"

class BoardTests(unittest.TestCase):

    def test_clear_board(self):
        """ Test for clear_board """
        board = chess.chess.board.Board()
        board.clear_board()
        square_count = 0
        for rank in board.BOARD:
            for square in rank:
                square_count += 1
                self.assertEqual(square, EMPTY)
        self.assertEqual(square_count, 64)

    def test_set_up_pieces(self):
        """ Test for set_up_pieces """
        board = chess.chess.board.Board()
        for rank, row in enumerate(board.BOARD):
            for file, sq in enumerate(row):
                if sq != EMPTY:
                    self.assertEqual(sq._id, STARTING_BOARD[rank][file]._id)
                else:
                    self.assertEqual(sq, EMPTY)
    def test_get_square_occupant(self):
        """ Test for get_square_occupant """
        board = chess.chess.board.Board()
        self.assertEqual(board.get_square_occupant("A1")._id, "R")
        self.assertEqual(board.get_square_occupant("A8")._id, "r")
        self.assertEqual(board.get_square_occupant("D1")._id, "Q")
        self.assertEqual(board.get_square_occupant("D8")._id, "q")

    def test_place_piece(self):
        board = chess.chess.board.Board()
        board.place_piece("R", "D4")
        self.assertEqual(board.get_square_occupant("D4")._id, "R")

    def test_remove_piece(self):
        board = chess.chess.board.Board()
        board.remove_piece("D1")
        self.assertEqual(board.get_square_occupant("D1"), EMPTY)

    def test_square_name(self):
        board = chess.chess.board.Board()
        self.assertEqual(board.square_name((0,2)), "C1")

    def test_import_board(self):
        """ Test for import_board() """
        board = chess.chess.board.Board(ARR_BOARD)
        for rank, row in enumerate(board.BOARD):
            for file, sq in enumerate(row):
                if sq != EMPTY:
                    self.assertEqual(sq._id, STARTING_BOARD[rank][file]._id)
                else:
                    self.assertEqual(sq, EMPTY)

    def test_import_board_fen(self):
        """ Test for import_board() with fen """
        board = chess.chess.board.Board(Notation.fen_to_board(fen=FEN_START)[0])
        for rank, row in enumerate(board.BOARD):
            for file, sq in enumerate(row):
                if sq != EMPTY:
                    self.assertEqual(sq._id, STARTING_BOARD[rank][file]._id)
                else:
                    self.assertEqual(sq, EMPTY)

    def test_import_board_fen2(self):
        """ Test for import_board() with fen """
        board = chess.chess.board.Board(arr=Notation.fen_to_board(fen=FEN_2)[0])
        for rank, row in enumerate(board.BOARD):
            for file, sq in enumerate(row):
                if sq != EMPTY:
                    self.assertEqual(sq._id, BOARD_2[rank][file]._id)
                else:
                    self.assertEqual(sq, EMPTY)

    def test_locate_piece(self):
        """ Test for locate_piece() """
        board = chess.chess.board.Board()
        self.assertEqual(board.locate_piece("K")._id, "K")
        self.assertEqual(board.locate_piece("k")._id, "k")

if __name__ == "__main__":
    unittest.main()
