import sys, os
testdir = os.path.dirname(__file__)
print(testdir)
srcdir = '../chess'
print(srcdir)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
print(os.path.abspath(os.path.join(testdir, srcdir)))

import unittest

from unittest.mock import patch

from chess.chess.locals import *
from chess.chess.game import Game
from chess.chess.pieces import Piece


class GameTests(unittest.TestCase):


    def test_whose_move(self):
        """ Test for whose_move """
        game = Game()
        game.move_count = 0
        self.assertEqual(game.whose_move(), WHITE)
        game.move_count = 1
        self.assertEqual(game.whose_move(), BLACK)

    def test_get_possible_squares_king(self):
        """ Test for get_possible_squares("k") """
        game = Game()
        game.board.clear_board()
        game.move_count += 1
        game.castling_rights = ["", "", "", ""]
        game.board.place_piece("k", "E1")
        game.board.place_piece("K", "E8")
        # King on empty board on e1
        self.assertEqual(game.get_possible_squares("k", "E1"),
                         [[1, 4], [1, 5], [0, 5], [0, 3], [1, 3]])
        game.board.set_up_pieces()
        # King on e1 on starting board
        self.assertEqual(game.get_possible_squares("K", "E1"), None)

    def test_get_possible_squares_queen(self):
        """ Test for get_possible_squares("k") """
        game = Game()
        game.board.clear_board()
        game.move_count += 1
        game.board.place_piece("k", "E8")
        game.board.place_piece("K", "C8")
        game.board.place_piece("q", "D1")
        legal_moves = game.get_possible_squares("q", "D1")
        # Queen on empty board on d1
        self.assertEqual(legal_moves,
                         [[1, 3], [2, 3], [3, 3], [4, 3], [5, 3], [6, 3], [7, 3],
                          [1, 4], [2, 5], [3, 6], [4, 7],
                          [0, 4], [0, 5], [0, 6], [0, 7],
                          [0, 2], [0, 1], [0, 0],
                          [1, 2], [2, 1], [3, 0]])
        game.board.set_up_pieces()
        # Queen on d1 on starting board
        self.assertEqual(game.get_possible_squares("Q", "D1"), None)
        game.board.clear_board()
        game.board.place_piece("K", "D1")
        game.board.place_piece("k", "E8")
        self.assertEqual(game.get_possible_squares("q", "D2"),
                         [[2, 3], [3, 3], [4, 3], [5, 3], [6, 3], [7, 3],
                          [2, 4], [3, 5], [4, 6], [5, 7],
                          [1, 4], [1, 5], [1, 6], [1, 7],
                          [0, 4],
                          [0, 3],
                          [0, 2],
                          [1, 2], [1, 1], [1, 0],
                          [2, 2], [3, 1], [4, 0]])

    def test_get_possible_squares_rook(self):
        """ Test for get_possible_squares("r") """
        game = Game()
        game.board.clear_board()
        game.move_count += 1
        game.board.place_piece("k", "E8")
        game.board.place_piece("K", "C8")
        game.board.place_piece("r", "D1")
        legal_moves = game.get_possible_squares("r", "D1")
        # Rook on empty board on d1
        self.assertEqual(legal_moves,
                         [[1, 3], [2, 3], [3, 3], [4, 3], [5, 3], [6, 3], [7, 3],
                          [0, 4], [0, 5], [0, 6], [0, 7],
                          [0, 2], [0, 1], [0, 0]])
        game.board.set_up_pieces()
        # Black Rook on d1 on starting board
        self.assertEqual(game.get_possible_squares("r", "D1"), [[1, 3], [0, 4], [0, 2]])
        # White Rook on d1 on starting board
        game.move_count += 1
        self.assertEqual(game.get_possible_squares("R", "D1"), None)

        game.board.clear_board()
        game.castling_rights = ["", "", "", ""]
        game.board.place_piece("K", "D2")
        game.board.place_piece("q", "D4")
        game.board.place_piece("R", "D3")
        self.assertEqual(game.get_possible_squares("R", "D3"), [[3,3]])

    def test_get_possible_squares_bishop(self):
        """ Test for get_possible_squares("b") """
        game = Game()
        game.board.clear_board()
        game.move_count += 1
        game.board.place_piece("b", "D1")
        legal_moves = game.get_possible_squares("b", "D1")
        # Bishop on empty board on d1
        self.assertEqual(legal_moves,
                          [[1, 4], [2, 5], [3, 6], [4, 7],
                          [1, 2], [2, 1], [3, 0]])
        game.board.set_up_pieces()
        # Bishop on d1 on starting board
        self.assertEqual(game.get_possible_squares("B", "D1"), None)


    def test_get_possible_squares_knight(self):
        """ Test for get_possible_squares("n") """
        game = Game()
        game.board.clear_board()
        game.board.place_piece("N", "B1")
        legal_moves = game.get_possible_squares("N", "E5")
        # Knight on empty board on e4
        self.assertEqual(legal_moves,
                         [[6, 3], [6, 5], [2, 3], [2, 5], [5, 2], [5, 6], [3, 2], [3, 6]])
        game.board.set_up_pieces()
        # Knight on b1 on starting board
        self.assertEqual(game.get_possible_squares("N", "B1"),
                         [[2,0],[2,2]])
        # Knight on g1 on starting board
        self.assertEqual(game.get_possible_squares("N", "G1"),
                         [[2,5],[2,7]])

    def test_in_check(self):
        """ Test for in_check() """
        game = Game()
        game.board.clear_board()
        game.castling_rights = ["", "", "", ""]
        game.board.place_piece("K", "B1")
        game.board.place_piece("q", "B2")
        game.board.place_piece("k", "B3")
        self.assertEqual(game.in_check(WHITE), True)
        self.assertEqual(game.in_check(BLACK), False)

        game.board.clear_board()
        game.board.place_piece("K", "E1")
        game.board.place_piece("p", "D2")
        self.assertEqual(game.in_check(WHITE), True)

        game.board.clear_board()
        game.board.place_piece("K", "E3")
        game.board.place_piece("p", "D2")
        self.assertEqual(game.in_check(WHITE), False)


        game.board.clear_board()
        game.board.place_piece("K", "E1")
        game.board.place_piece("p", "D2")
        self.assertEqual(game.in_check(WHITE), True)

        game.board.clear_board()
        game.board.place_piece("k", "E3")
        game.board.place_piece("P", "D2")
        game.move_count = 1
        self.assertEqual(game.in_check(BLACK), True)
        game.move_count = 0

        game.board.clear_board()
        game.board.place_piece("k", "E3")
        game.board.place_piece("P", "D4")
        self.assertEqual(game.in_check(BLACK), False)

        game.board.clear_board()
        game.board.place_piece("k", "E3")
        game.board.place_piece("P", "E2")
        self.assertEqual(game.in_check(BLACK), False)

        game.board.clear_board()
        game.board.place_piece("k", "B1")
        game.board.place_piece("K", "B3")
        self.assertEqual(game.in_check(WHITE), False)


    def test_square_attacked_by(self):
        """ Test for square_attacked_by() """
        game = Game()
        game.board.clear_board()
        game.board.place_piece("Q", "B1")
        game.board.place_piece("N", "D3")
        game.board.place_piece("R", "B4")
        game.board.place_piece("B", "C3")
        game.board.place_piece("B", "C4")
        game.board.place_piece("k", "B2")
        game.board.place_piece("K", "D2")
        game.board.place_piece("b", "E3")
        self.assertEqual(game.square_attacked_by(game.board.locate_piece("k"), "R"), True)
        self.assertEqual(game.square_attacked_by(game.board.locate_piece("k"), "N"), True)
        self.assertEqual(game.square_attacked_by(game.board.locate_piece("k"), "Q"), True)
        self.assertEqual(game.square_attacked_by(game.board.locate_piece("k"), "B"), True)
        self.assertEqual(game.square_attacked_by(game.board.locate_piece("K"), "n"), None)
        self.assertEqual(game.square_attacked_by(game.board.locate_piece("K"), "b"), True)

    def test_mate_checkmate(self):
        """ Test for test_if_mate() checkmate """
        game = Game()
        game.castling_rights = ["", "", "", ""]
        game.board.remove_piece("D1")
        game.board.remove_piece("C1")
        game.board.place_piece("r", "C1")
        self.assertEqual(game.test_if_mate(), CHECKMATE)

    def test_mate_stalemate(self):
        """ Test for test_if_mate() stalemate """
        game = Game()
        game.board.clear_board()
        game.castling_rights = ["", "", "", ""]
        game.board.place_piece("K", "H8")
        game.board.place_piece("q", "G6")
        self.assertEqual(game.test_if_mate(), STALEMATE)

    @patch('chess.chess.game.Game.get_input', return_value='Q')
    def test_promote_queen(self, input):
        """ Test for promote() queen """
        game = Game(cmd_mode=True)
        self.assertEqual(game.promote().name, Piece("Q").name)

    @patch('chess.chess.game.Game.get_input', return_value='r')
    def test_promote_rook(self, input):
        """ Test for promote() rook """
        game = Game(cmd_mode=True)
        self.assertEqual(game.promote().name, Piece("r").name)

    @patch('chess.chess.game.Game.get_input', return_value='B')
    def test_promote_bishop(self, input):
        """ Test for promote() bishop """
        game = Game(cmd_mode=True)
        self.assertEqual(game.promote().name, Piece("B").name)

    @patch('chess.chess.game.Game.get_input', return_value='n')
    def test_promote_knight(self, input):
        """ Test for promote() knight """
        game = Game(cmd_mode=True)
        self.assertEqual(game.promote().name, Piece("n").name)

    @patch('chess.chess.game.Game.get_input', return_value='n')
    def test_request_draw_n(self, input):
        """ Test for request_draw() n """
        game = Game(cmd_mode=True)
        self.assertEqual(game.request_draw(), None)

    @patch('chess.chess.game.Game.get_input', return_value='y')
    def test_request_draw_y(self, input):
        """ Test for request_draw() y """
        game = Game(cmd_mode=True)
        self.assertEqual(game.request_draw(), True)

    def test_count_repetitions(self):
        """ Test for count_repetitions() starting position """
        game = Game(cmd_mode=True)
        self.assertEqual(game.count_repetitions(), 1)


if __name__ == "__main__":
    unittest.main()
