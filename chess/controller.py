import pygame, sys

from pygame.locals import *

from chess.locals import *
from chess.game import Game
from chess.screen import Screen

# Example FEN for importing to have custom start positions
FEN_START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
FEN_99moves = "5k2/ppp5/4P3/3R3p/6P1/1K2Nr2/PP3P2/8 b - - 99 49"
FEN_149moves = "5k2/ppp5/4P3/3R3p/6P1/1K2Nr2/PP3P2/8 b - - 149 49"
FEN_W_MATE = "rnQ1kbnr/pppppppp/2bq4/8/8/8/PPPPPPPP/RNB1KBNR b KQkq -"
FEN_B_BLOCKMATE = "rnQ1kbnr/ppppqppp/2b1p3/8/8/8/PPPPPPPP/RNB1KBNR b KQkq -"
FEN_W_1MOVE_MATE = "rn2kbnr/ppp1pppp/2bpQ3/2q5/8/8/PPPPPPPP/RNB1KBNR w KQkq -"
FEN_W_1MOVE_MATE_AT_149MOVES = "rn2kbnr/ppp1pppp/2bpQ3/2q5/8/8/PPPPPPPP/RNB1KBNR w KQkq - 149 74"
FEN_B_CASTLE_THROUGH_CHECK = "r3kbnr/ppp1pppp/n1b5/2qQ4/8/8/PPPPPPPP/RNB1KBNR b KQkq -"
FEN_PROMOTING = "4kbnr/ppPppppp/rn1qb3/8/8/R1NP4/PpP1PPPP/2BQKBNR w KQkq -"
FEN_OPPOSITION_TEST = "r3kbn1/p4ppp/rn1Kbp2/8/8/R1NP4/PpP1PPPP/2BQ1BNR w KQkq -"



class GameLoop():
    """ Control player input """

    def __init__(self, ai=None, fen=None, fps=30):
        """ Initialises game loop """

        self.chess_game = Game(fen=fen)
        self.ai = ai
        self.FPS = fps
        self.fpsClock = pygame.time.Clock()
        self.start()

    def start(self):
        Screen.start_screen()
        Screen.load_all_chessmen()
        Screen.draw_checkered_board()
        Screen.draw_all_chessmen(self.chess_game.board.BOARD)
        self.chess_game.start_turn()
        move_from = None
        move_to = None
        b_possible_moves = None

        # Game loop
        while True:

            if self.chess_game.gameover:
                Screen.draw_btm_bar()
                Screen.display_btm_info(self.chess_game.gameover)
                Screen.draw_top_bar()
                Screen.display_top_info("Press SPACE to play again")

            elif self.chess_game.claim_draw:
                Screen.draw_btm_bar()
                Screen.display_btm_info("Accept draw? (press y to accept)")

            # Computer AI plays black
            elif not self.chess_game.white_to_move():
                if self.ai:
                    self.chess_game.move(self.chess_game.get_random_move())
                    Screen.draw_checkered_board()
                    Screen.draw_all_chessmen(self.chess_game.board.BOARD)
                    Screen.draw_top_bar()
                    self.chess_game.start_turn()

            else:
                Screen.draw_btm_bar()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN and not self.chess_game.gameover:
                    if event.key == K_y and self.chess_game.claim_draw:
                        self.chess_game.gameover = DRAW
                        self.chess_game.start_turn()
                        break

                elif event.type == pygame.KEYDOWN and self.chess_game.gameover:
                    if event.key == K_SPACE:
                        self.chess_game = Game(fen=self.chess_game.fen)
                        GameLoop.draw_whole_screen(self.chess_game.board.BOARD)
                        self.chess_game.start_turn()

                elif event.type == pygame.MOUSEBUTTONDOWN and not self.chess_game.gameover:

                    # If already clicked on a piece
                    if move_from:
                        # Next click = move_to square
                        move_to = GameLoop.get_clicked_square(event.pos)
                        if move_to:
                            try_move = self.chess_game.move(move_from + move_to)
                        else:
                            try_move = None

                        # If move_to is a legal move
                        if try_move == PROMOTE:
                            Screen.display_top_info("Choose promotion piece (press Q, R, B, or N)")
                            Screen.update()
                            promote_piece = None
                            while not promote_piece:
                                promote_piece = GameLoop.choose_promotion_piece()
                            self.chess_game.move(move_from + move_to, promote=promote_piece)
                            Screen.draw_checkered_board()
                            Screen.draw_all_chessmen(self.chess_game.board.BOARD)
                            Screen.draw_top_bar()
                            self.chess_game.start_turn()
                            move_from = None
                            move_to = None
                            break

                        elif try_move:
                            move_from = None
                            move_to = None
                            Screen.draw_checkered_board()
                            Screen.draw_all_chessmen(self.chess_game.board.BOARD)
                            self.chess_game.start_turn()
                            break

                        # If clicked same square
                        elif move_to == move_from:
                            Screen.draw_checkered_board()
                            Screen.draw_all_chessmen(self.chess_game.board.BOARD)
                            move_from = None
                            move_to = None
                            break

                        # If move_to_square has legal moves, make that the move_from square
                        elif self.chess_game.get_possible_squares(square=move_to):
                            move_from = move_to
                            move_to = None

                        # If move_to is not a legal move, reset cicked squares
                        else:
                            move_from = None
                            move_to = None
                            Screen.draw_checkered_board()
                            Screen.draw_all_chessmen(self.chess_game.board.BOARD)
                            break

                    # If no piece selected
                    move_from = GameLoop.get_clicked_square(event.pos)
                    Screen.draw_checkered_board()
                    Screen.draw_all_chessmen(self.chess_game.board.BOARD)
                    legal_moves = self.chess_game.get_possible_squares(square=move_from)
                    if legal_moves:
                        for sq in legal_moves:
                            Screen.draw_dot_on_square(sq)
                        break

            pygame.display.update()
            self.fpsClock.tick(self.FPS)

    @staticmethod
    def draw_whole_screen(board):
        """ Draws top and bottom bars, and board and chessmen """
        Screen.draw_top_bar()
        Screen.draw_btm_bar()
        Screen.draw_checkered_board()
        Screen.draw_all_chessmen(board)

    @staticmethod
    def get_clicked_square(pos):
        """ Gets square where mouse clicked """
        file = int((pos[0] - Screen.LEFTBAR) / Screen.GRID_SIZE)
        rank = 7 - int((pos[1] - Screen.TOPBAR) / Screen.GRID_SIZE)
        if rank < 0 or rank > 7:
            return None
        elif file < 0 or file > 7:
            return None
        else:
            square = TO_FILE[file] + TO_RANK[rank]
            return square

    @staticmethod
    def choose_promotion_piece():
        """ Waits for user button click """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == K_q:
                    return "Q"
                elif event.key == K_r:
                    return "R"
                elif event.key == K_b:
                    return "B"
                elif event.key == K_n:
                    return "N"


# For testing purposes #
if __name__ == "__main__":

    GameLoop()