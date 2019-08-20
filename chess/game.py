from random import randint
from collections import Counter

from locals import *
from board import Board
from pieces import Piece
from notation import Notation


class Game:
    """ Creates chess game, can use imported FEN, or else uses starting position
        if cmd_mode = True, the game will be played in the command line """

    def __init__(self, fen=None, cmd_mode=None):

        self.gameover = False
        self.promote_pawn = False
        self.claim_draw = False
        self.cmd_mode = cmd_mode
        self.fen = fen

        if fen:
            fen = Notation.fen_to_board(fen)
            self.board = Board(fen[0])
            self.active_colour = fen[1]
            self.castling_rights = [c for c in fen[2]]
            self.en_passant_sq = fen[3]
            self.half_move_count = int(fen[4])
            self.full_move_count = int(fen[5])

            if self.active_colour == WHITE:
                self.move_count = self.full_move_count * 2 - 2
            else:
                self.move_count = self.full_move_count * 2 - 1
            self.check = self.in_check(self.active_colour)

        else:
            self.check = False
            self.move_count = 0
            self.board = Board()
            self.active_colour = WHITE
            self.castling_rights = ["K", "Q", "k", "q"]
            self.en_passant_sq = None
            self.half_move_count = 0
            self.full_move_count = self.move_count // 2 + 1

        # Initialise for threefold repetition test
        self.positions = []

    def whose_move(self):
        """ Returns colour of whose turn it is """
        if self.move_count % 2 == 0:
            return WHITE
        else:
            return BLACK

    def white_to_move(self):
        """ Returns True if WHITE to move """
        if self.move_count % 2 == 0:
            return True

    def get_all_possible_moves(self):
        """ Returns a list of all possible moves on board """
        all_moves = []
        for row, rank in enumerate(self.board.BOARD):
            for col, piece in enumerate(rank):
                if piece is not EMPTY and piece.colour is self.whose_move():
                    possible_moves = self.get_possible_squares(piece=piece._id, square=(piece.rank, piece.file))
                    if possible_moves:
                        move = TO_FILE[col] + TO_RANK[row] + TO_FILE[possible_moves[0][1]] + TO_RANK[possible_moves[0][0]]
                        all_moves.append(move)
        return all_moves

    def get_random_move(self):
        """ Returns a random legal move for current active colour """
        moves = self.get_all_possible_moves()
        random_index = randint(0, len(moves) - 1)
        random_move = moves[random_index]
        return random_move

    def get_possible_squares(self, piece=None, square=None):
        """ Returns a list of possible squares availale to move to.
            Input needed: One of: piece or square, or both
            piece can be one of: string - 'K'
                                 Piece - Piece('K')
            square can be one of: string - 'E4'
                                  array coordinates - [3,5]
            Usage:  get_possible_squares(piece='K', square='E4')
                    get_possible_squares(square='E4')
                    get_possible_squares(piece=<Piece>)  // Piece with .file and .rank
                    get_possible_squares(square=<Piece>) // Piece with .file and .rank
            """
        #print(f"piece:{piece}, square:{square}")

        # if both piece and square are None
        if not piece and not square:
            return None

        # piece can be string or Piece object or empty
        if type(piece) is str:
            piece_obj = Piece(piece)
        elif type(piece) is Piece:
            piece_obj = piece
        else:
            piece_obj = self.board.BOARD[RANK[square[1]]][FILE[square[0]]]

        # square can be empty, string or array coordinates
        if not square:
            file = piece_obj.file
            rank = piece_obj.rank
        elif type(square) is str:
            file = FILE[square[0]]
            rank = RANK[square[1]]
        else:
            file = square[1]
            rank = square[0]

        # If no piece enterred and square is EMPTY:
        if not piece and self.board.BOARD[rank][file] is EMPTY:
            return None

        # If piece is newly created without file and rank
        if not piece_obj.file:
            piece_obj.file = file
            piece_obj.rank = rank

        # If not active colour
        if piece_obj.colour is not self.whose_move():
            return None

        #print(f"get_possible_squares({piece_obj._id} on {Board.square_name((piece_obj.rank, piece_obj.file))})")

        # Loop through directions of piece movements
        possible_squares = []
        for movement in piece_obj.movements:
            distance = 0
            possible_file = file
            possible_rank = rank
            max_distance = piece_obj.max_distance

            # Loop until range of piece is exceeded
            while distance != max_distance:

                # If pawn on starting position
                if piece_obj.name is PAWN:
                    if piece_obj.colour == WHITE and rank == 1 or \
                       piece_obj.colour == BLACK and rank == 6:
                        max_distance = 2

                # copy board for testing in_check conditions
                possible_board = Board(self.board.BOARD)
                possible_file += movement[1]
                possible_rank += movement[0]

                # If passed edge of board
                if possible_file < 0 or possible_file > 7 or \
                   possible_rank < 0 or possible_rank > 7:
                        #print("Can't move: off edge of board")
                        break

                possible_square = possible_board.BOARD[possible_rank][possible_file]

                # If square is occupied
                if possible_square is not EMPTY:
                    # If own piece in the way
                    if possible_square.colour == piece_obj.colour:
                        break
                    # If opposition piece in the way
                    else:
                        # If moving piece is a pawn
                        if piece_obj.name == PAWN:
                            # If forward pawn move
                            if movement in piece_obj.normal_movements:
                                break

                        # Test for putting self in check
                        possible_board.remove_piece((rank, file))
                        possible_board.place_piece(square=possible_square, piece=piece_obj._id)

                        if self.in_check(board=possible_board, colour=piece_obj.colour):
                            break
                        # Can capture piece
                        else:
                            possible_squares.append([possible_rank, possible_file])
                            break

                # Square not occupied
                else:
                    # If pawn
                    if piece_obj.name == PAWN:
                        # Can't move diagonal if not capturing unless en-passant
                        if movement in piece_obj.capture_movements:
                            if not self.en_passant_sq:
                                break
                            elif self.en_passant_sq and \
                                    Board.square_name((possible_rank, possible_file)) != self.en_passant_sq.upper():
                                break

                        # If not on 2nd rank(WHITE) or 7th rank(BLACK): Can't move two squares
                        if piece_obj.colour == WHITE and rank != 1 and distance == 1 or \
                           piece_obj.colour == BLACK and rank != 6 and distance == 1:
                            break

                    # If Castling King
                    if piece_obj.name is KING and piece_obj.colour is WHITE:
                        if movement is E and self.castling_rights[0]:
                            if max_distance == 1:
                                max_distance = 2
                        if movement is W and self.castling_rights[1]:
                            if max_distance == 1:
                                max_distance = 2
                    elif piece_obj.name is KING and piece_obj.colour is BLACK:
                        if movement is E and self.castling_rights[2]:
                            if max_distance == 1:
                                max_distance = 2
                        if movement is W and self.castling_rights[3]:
                            if max_distance == 1:
                                max_distance = 2

                    # Test for putting self in check
                    possible_board.remove_piece((rank, file))
                    possible_board.place_piece(square=(possible_rank, possible_file), piece=piece_obj._id)
                    if not self.in_check(board=possible_board, colour=piece_obj.colour):
                        possible_squares.append([possible_rank, possible_file])
                    else:
                        # Can't castle through a check
                        if piece_obj.name is KING:
                            max_distance = 1

                distance += 1
        if not possible_squares:
            return None
        else:
            return possible_squares

    def print_legal_moves(self, piece, square):
        """ Prints to console on board of all legal moves """
        display_board = Board(self.board.BOARD)
        legal_moves = self.get_possible_squares(piece, square)
        print("Legal moves: " + ", ".join([self.board.square_name(move) for move in legal_moves]))
        for move in legal_moves:
            display_board.BOARD[move[0]][move[1]] = " X "
        display_board.print_board()


    def in_check(self, colour, board=None):
        """ Returns True if King is in check, else False """
        if not board:
            board = self.board

        #print("in check?")
        #board.print_board()

        if colour == WHITE:
            king = "K"
            pieces = "rbnpk".lower()
        else:
            king = "k"
            pieces = "rbnpk".upper()

        king = board.locate_piece(king)

        # If no king on board - testing purposes
        if not king:
            return False

        for piece in pieces:
            #print(f"A {piece} attacking my {king._id}?")
            if self.square_attacked_by(king, piece, board=board):
                #print(f"in check from {piece}")
                return True
        #print("Not in check")
        return False

    def square_attacked_by(self, piece, attacker, board=None):
        """ Returns True if square is attacked by inputted piece """
        #print(f"Entered square_attacked_by({piece._id} on {Board.square_name((piece.rank, piece.file))}, attacked by {attacker}?)")
        if not board:
            board = self.board

        file = piece.file
        rank = piece.rank
        attacker = Piece(attacker)

        if attacker.name == PAWN:
            if attacker.colour == WHITE:
                movements = [SW, SE]
            else:
                movements = [NW, NE]
        else:
            movements = attacker.movements

        for movement in movements:
            #print(movement)
            distance = 0
            possible_file = file
            possible_rank = rank

            while distance != attacker.max_distance:
                #print(distance)
                #board.print_board()
                possible_file += movement[1]
                possible_rank += movement[0]

                # If passed edge of board
                if possible_file < 0 or possible_file > 7 or \
                        possible_rank < 0 or possible_rank > 7:
                    #print("off edge of board")
                    break
                #print(board.BOARD[possible_rank][possible_file])
                # If square is occupied
                if board.BOARD[possible_rank][possible_file] is not EMPTY:
                    # If own piece in the way
                    if board.BOARD[possible_rank][possible_file].colour == piece.colour:
                        #print(f"own piece in way: {board.BOARD[possible_rank][possible_file]}")
                        break
                    # If opposition piece in the way
                    else:
                        # If is attacker we are searching for
                        if board.BOARD[possible_rank][possible_file].name == attacker.name:
                            #print(f"Attacker found: {attacker.name}")
                            return True
                        # If attacker is Rook or Bishop, we also search for a Queen
                        elif attacker.name is ROOK or attacker.name is BISHOP:
                            if board.BOARD[possible_rank][possible_file].name is QUEEN:
                                #print("Queen found while searching for R or B")
                                return True
                        # If is a different piece
                        else:
                            #print("different piece found")
                            break

                # Square not occupied
                distance += 1

    def test_if_mate(self):
        """ Returns True if win or draw """
        legal_moves = []
        for rank in self.board.BOARD:
            for sq in rank:
                if type(sq) is Piece and sq.colour == self.whose_move():
                    legal_moves.append(self.get_possible_squares(sq))
        if not any(legal_moves):
            if self.in_check(self.whose_move()):
                self.finish_game(result=CHECKMATE)
                return CHECKMATE
            else:
                self.finish_game(result=STALEMATE)
                return STALEMATE



    def move(self, move, promote=None):
        """ Move a piece in game conditions
            input is source square, destination square
            Input is one of:
                - String eg. 'D2D4'
                - Tuple of ((from tuple), (to tuple)) eg. ((4,5),(5,5))"""

        en_passant = None
        half_move_reset = None

        if type(move) is not str:
            from_square = TO_FILE[move[0][1]] + TO_RANK[move[0][0]]
            to_square = TO_FILE[move[1][1]] + TO_RANK[move[1][0]]
            move = from_square + to_square

        # If input format is incorrect
        if len(move) != 4:
            return False
        if not move[1].isdigit() or not move[3].isdigit():
            return False
        if not move[0].isalpha() or not move[2].isalpha():
            return False


        # Convert to board format
        from_square = move[0:2].upper()
        to_square = move[2:].upper()


        piece = self.board.get_square_occupant(from_square)

        # If moving empty square
        if type(piece) is not Piece:
            return False
        # If moving opponent piece
        if piece.colour is not self.whose_move():
            return False

        # If promoting, checks already made, so we can move inputted piece to promote square
        if promote:
            if self.white_to_move():
                promote = promote.upper()
            else:
                promote = promote.lower()

            self.board.place_piece(promote, to_square)
            self.board.remove_piece(from_square)
            self.change_turn(en_passant=None, reset=True)
            return True


        # Test if move is legal
        poss_rank = RANK[to_square[1]]
        poss_file = FILE[to_square[0]]
        poss_moves = self.get_possible_squares(piece=piece, square=from_square)
        #print(poss_moves)

        # If legal move
        if [poss_rank, poss_file] in poss_moves:

            # If capture or pawn move, reset half move clock
            if self.board.BOARD[poss_rank][poss_file] is not EMPTY:
                half_move_reset = True
            elif piece.name is PAWN:
                half_move_reset = True

            # Check if en passant is now available
            if piece.name is PAWN and abs(int(move[3]) - int(move[1])) == 2:
                if piece.colour is WHITE:
                    en_passant = move[2] + str(int(move[1]) + 1)
                else:
                    en_passant = move[2] + str(int(move[1]) - 1)

            # Check for promotion square
            if piece.name is PAWN:
                if piece.colour is WHITE and to_square[1] is "8":
                    if self.cmd_mode:
                        piece = self.promote()
                    else:
                        return PROMOTE
                elif piece.colour is BLACK and to_square[1] is "1":
                    if self.cmd_mode:
                        piece = self.promote()
                    else:
                        return PROMOTE

            # Update castling rights
            if any(self.castling_rights):
                if piece.name is KING or piece.name is ROOK:
                    self.update_castling_rights(piece)

            # Move piece
            self.board.place_piece(piece._id, to_square)
            self.board.remove_piece(from_square)

            # If castling
            if piece.name is KING and abs(ord(move[2]) - ord(move[0])) == 2:
                self.castle(to_square=to_square)

            self.change_turn(en_passant=en_passant, reset=half_move_reset)

            return True

        # If illegal move
        else:
            return False

    def update_en_passant_square(self, square):
        """ Sets en passant square to supplied square, else sets it to None """
        if not square:
            self.en_passant_sq = None
        else:
            self.en_passant_sq = square

    def update_move_clocks(self, reset=None):
        """ Sets move_count, full_move_count and half_move_count.
            If reset is passed, then the half move clock will reset to 0 """
        self.move_count += 1
        self.full_move_count = self.move_count // 2 + 1
        if reset:
            self.half_move_count = 0
        else:
            self.half_move_count += 1

    def start_turn(self):
        """ Checks mate or draw conditions at start of turn """
        print(f"check: {self.check}, castling rights: {''.join(self.castling_rights)}, en-passant: {self.en_passant_sq}, halfmove: {self.half_move_count}, fullmove:{self.full_move_count}, active colour:{self.active_colour}")
        if not self.test_if_mate():
            self.test_if_draw()

    def change_turn(self, en_passant=None, reset=None):
        """ Update move counters and active colour """

        self.update_move_clocks(reset)
        self.active_colour = self.whose_move()
        self.update_en_passant_square(en_passant)
        self.check = self.in_check(self.active_colour)


    def test_if_draw(self):
        """ Check if draw claim is available, if so, get user input from command line if cmd_mode, or via controller.py
            Check if it's an automatic draw, if so, end game as draw """
        self.claim_draw = False

        # Move count draw claim conditions
        if self.half_move_count >= 150:
            self.finish_game(result=DRAW)

        elif self.half_move_count >= 100:
            if self.request_draw():
                self.finish_game(result=DRAW)

        # Position repetition draw claim conditions
        self.store_position()
        repetition_count = self.count_repetitions()

        if repetition_count == 5:
            self.finish_game(result=DRAW)

        elif repetition_count >= 3:
            print("threefold repetition")
            if self.request_draw():
                self.finish_game(result=DRAW)



    def request_draw(self):
        """ Asks user if they want to claim draw """
        if self.cmd_mode:
            answers = "Y", "YES", "N", "NO"
            answer = ""
            while answer.upper() not in answers:
                answer = Game.get_input("Claim draw? (y or n)").upper()
            if answer == "Y" or answer == "YES":
                return True
        else:
            self.claim_draw = True


    def finish_game(self, result=None):
        """ Finishes game with result of one of: draw, stalemate or resign, checkmate result """
        print(result)
        self.gameover = result

    def promote(self):
        """ Ask user for promotion piece and return piece """
        pieces = "QRBN"
        if self.cmd_mode:
            piece = Game.get_input(f"Choose a piece({pieces}): ")
        while piece.upper() not in pieces:
            piece = Game.get_input(f"Choose a piece({pieces}): ")
        if self.active_colour is WHITE:
            return Piece(piece.upper())
        else:
            return Piece(piece.lower())

    # Function to allow unittest to input data
    @staticmethod
    def get_input(msg):
        """ Get's input from user """
        return input(msg)

    def castle(self, to_square):
        """ Moves correct Rook to other side of King """
        if to_square.upper() == "G1":
            self.board.remove_piece("H1")
            self.board.place_piece("R", "F1")
        elif to_square.upper() == "C1":
            self.board.remove_piece("A1")
            self.board.place_piece("R", "D1")
        elif to_square.upper() == "G8":
            self.board.remove_piece("H8")
            self.board.place_piece("r", "F8")
        elif to_square.upper() == "C8":
            self.board.remove_piece("A8")
            self.board.place_piece("r", "D8")

    def update_castling_rights(self, piece):
        """ Removes specific castling rights for colour of piece inputted:
             - Removes long and short castling rights if King is inputted
             - Removes long castling rights if A Rook is inputted
             - Removes short castling rights if H Rook is inputted """
        if piece.name is KING:
            if piece.colour is WHITE:
                self.castling_rights[0] = ""
                self.castling_rights[1] = ""
            else:
                self.castling_rights[2] = ""
                self.castling_rights[3] = ""

        if piece.name is ROOK:
            if piece.colour is WHITE:
                if self.castling_rights[0] and piece.file is 7:
                    self.castling_rights[0] = ""
                elif self.castling_rights[1] and piece.file is 0:
                    self.castling_rights[1] = ""
            else:
                if self.castling_rights[2] and piece.file is 7:
                    self.castling_rights[2] = ""
                elif self.castling_rights[3] and piece.file is 0:
                    self.castling_rights[3] = ""

    def export_fen(self):
        """ Export current board position in FEN format """
        position = []
        for row in reversed(self.board.BOARD):
            output_row = ""
            empty_squares_count = 0
            for square in row:
                if square is EMPTY:
                    empty_squares_count += 1
                else:
                    if empty_squares_count:
                        output_row += str(empty_squares_count)
                        empty_squares_count = 0
                    else:
                        output_row += square._id
                if empty_squares_count == 8:
                    output_row += str(empty_squares_count)
            position.append(output_row)
        position = "/".join(position)
        output = []
        output.append(position)
        output.append(self.active_colour)
        if self.castling_rights:
            output.append("".join(self.castling_rights))
        else:
            output.append("-")
        if self.en_passant_sq:
            output.append(self.en_passant_sq)
        else:
            output.append("-")
        output.append(str(self.half_move_count))
        output.append(str(self.full_move_count))
        return " ".join(output)

    def store_position(self):
        """ Store position to self.positions to test for repetitions """
        fen = self.export_fen().split(" ")
        position = " ".join([fen[0], fen[2], fen[3]])
        self.positions.append(position)

    def count_repetitions(self):
        """ Returns highest number of repetitions there has been """
        repetitions = Counter(self.positions).most_common(1)
        return repetitions[0][1]


# For testing purposes #
if __name__ == "__main__":

    # Example FEN for importing to have custom start positions
    FEN_START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    FEN_99moves = "5k2/ppp5/4P3/3R3p/6P1/1K2Nr2/PP3P2/8 w - - 99 49"
    FEN_149moves = "5k2/ppp5/4P3/3R3p/6P1/1K2Nr2/PP3P2/8 b - - 149 49"
    FEN_W_MATE = "rnQ1kbnr/pppppppp/2bq4/8/8/8/PPPPPPPP/RNB1KBNR b KQkq -"
    FEN_B_BLOCKMATE = "rnQ1kbnr/ppppqppp/2b1p3/8/8/8/PPPPPPPP/RNB1KBNR b KQkq -"
    FEN_W_1MOVE_MATE = "rn2kbnr/ppp1pppp/2bpQ3/2q5/8/8/PPPPPPPP/RNB1KBNR w KQkq -"
    FEN_W_1MOVE_MATE_AT_149MOVES = "rn2kbnr/ppp1pppp/2bpQ3/2q5/8/8/PPPPPPPP/RNB1KBNR w KQkq - 149 74"
    FEN_B_CASTLE_THROUGH_CHECK = "r3kbnr/ppp1pppp/n1b5/2qQ4/8/8/PPPPPPPP/RNB1KBNR b KQkq -"
    FEN_PROMOTING = "4kbnr/ppPppppp/rn1qb3/8/8/R1NP4/PpP1PPPP/2BQKBNR w KQkq -"
    FEN_OPPOSITION_TEST = "r3kbn1/p4ppp/rn1Kbp2/8/8/R1NP4/PpP1PPPP/2BQ1BNR w KQkq -"

    game = Game(fen=None, cmd_mode=True)

    # Game loop
    while not game.gameover:
        game.board.print_board()
        move = ""
        game.start_turn()

        if move.lower() == "q":
            game.gameover = "exit"
            break

        while not game.move(move) and move.lower() != "q" and not game.gameover:
            move = input("move: ")





