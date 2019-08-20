import re

from locals import *


class Notation:



    @classmethod
    def moved_piece(cls, move):
        """ Return id of moved piece
            Usage: 1. e4
                   1... e5 """
        move = cls.split_notation(move)
        move_col = move[1]
        move_desc = move[2]

        # Pawn
        if move_desc[0].islower():
            piece = "P"
            return cls.get_case(piece, move_col)

        # Pieces
        return cls.get_case(move_desc[0], move_col)


    @classmethod
    def get_case(cls, piece, col):
        """ Return uppercase or lowercase of piece, depending on colour """
        if len(col) == 2:
            return piece.upper()
        else:
            return piece.lower()


    @classmethod
    def capture(cls, move):
        """ Return True if move involves capture, else False """
        move = cls.split_notation(move)
        if "x" in move[2]:
            return True
        return False

    @staticmethod
    def split_notation(move):
        return re.split("(\W+)", move)

    @staticmethod
    def fen_to_board(fen):
        """ converts FEN to board for importing """

        arr = []
        fen = fen.split(" ")
        board = fen[0]
        active_colour = fen[1]
        if fen[2] == "-":
            castling_rights = ["", "", "", ""]
        else:
            castling_rights = fen[2]
        if fen[3] == "-":
            en_passant_sq = None
        else:
            en_passant_sq = fen[3]

        # If no move counts
        if len(fen) != 6:
            half_move_count = 0
            move_count = 0
        else:
            half_move_count = fen[4]
            move_count = fen[5]

        board = re.split("(\W+)", board)

        for rank in reversed(board):
            arr_row = []
            if rank == "/":
                continue
            for piece in rank:
                if piece.isdigit():
                    for i in range(int(piece)):
                        arr_row.append(EMPTY)
                else:
                    arr_row.append(piece)
            arr.append(arr_row)
            if len(arr) == 8:
                break
        return arr, active_colour, castling_rights, en_passant_sq, half_move_count, move_count

    @staticmethod
    def game_to_fen(game):
        """ Converts a Board to a fen """
        fen = []
        fen.append(game.whose_move()[0].lower())
        fen.append("".join(game.castling_rights))
        fen.append(game.en_passant_sq)
        fen.append(game.half_move_count)
        fen.append(game.move_count)
        return fen


