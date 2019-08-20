import sys, os
testdir = os.path.dirname(__file__)
print(testdir)
srcdir = '../chess'
print(srcdir)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
print(os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
from chess.chess.notation import Notation
from chess.chess.game import Game


class GameTests(unittest.TestCase):

    def test_moved_piece(self):
        """ Test for moved_piece """
        self.assertEqual(Notation.moved_piece("1. e4"), "P")
        self.assertEqual(Notation.moved_piece("1... e5"), "p")
        self.assertEqual(Notation.moved_piece("10. exd4"), "P")
        self.assertEqual(Notation.moved_piece("11... exd5"), "p")
        self.assertEqual(Notation.moved_piece("21. Ke4"), "K")
        self.assertEqual(Notation.moved_piece("33... Qe5"), "q")
        self.assertEqual(Notation.moved_piece("49. Bexd4"), "B")
        self.assertEqual(Notation.moved_piece("50... Nexd5"), "n")
        self.assertEqual(Notation.moved_piece("50... Rexd5"), "r")

    def test_capture(self):
        """ Test for capture """
        self.assertEqual(Notation.capture("1. e4"), False)
        self.assertEqual(Notation.capture("1... e5"), False)
        self.assertEqual(Notation.capture("10. exd4"), True)
        self.assertEqual(Notation.capture("11... exd5"), True)

    def test_fen_to_board(self):
        """ Test for fen_to_board() """
        self.assertEqual(Notation.fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")[0],
                        [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
                         ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                         [' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - '],
                         [' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - '],
                         [' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - '],
                         [' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - '],
                         ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                         ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']])

    def test_game_to_fen(self):
        """ Test for game_to_fen() """
        game = Game()
        pass


if __name__ == "__main__":
    unittest.main()
