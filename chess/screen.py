import pygame, os, sys
from locals import *
from board import Board


class Screen:

    ######## USER CHANGEABLE DATA ########

    S_TITLE = "Chess"  # Window title
    SCREEN_SIZE = (8, 8)  # Playing area in grid cells
    GRID_SIZE = 50          # Grid size in pixels
    BG_COLOR = (100,100,100)         # Playing area background colour
    T_BG_COLOR = R_BG_COLOR = B_BG_COLOR = L_BG_COLOR = (255,255,255)   # Side panels background colour
    T_SIZE, R_SIZE, B_SIZE, L_SIZE = (2, 2, 2, 2)              # Side panels sizes in grid cells (0 = Non existent)
    FONT_COLOR = RED

    ############### END ###################

    pygame.init()

    # Outside panel sizes in pixels
    TOPBAR = GRID_SIZE * T_SIZE
    RIGHTBAR = GRID_SIZE * R_SIZE
    BOTTOMBAR = GRID_SIZE * B_SIZE
    LEFTBAR = GRID_SIZE * L_SIZE

    SCREEN_WIDTH = GRID_SIZE * SCREEN_SIZE[0]  # Playing screen width in pixels
    SCREEN_HEIGHT = GRID_SIZE * SCREEN_SIZE[1]  # Playing screen height in pixels

    WINDOW_WIDTH = SCREEN_WIDTH + LEFTBAR + RIGHTBAR
    WINDOW_HEIGHT = SCREEN_HEIGHT + TOPBAR + BOTTOMBAR
    WINDOW_SIZE = (WINDOW_WIDTH,  WINDOW_HEIGHT)

    GRID_WIDTH = int(SCREEN_WIDTH / GRID_SIZE)  # Total number of grid squares on x axis
    GRID_HEIGHT = int(SCREEN_HEIGHT / GRID_SIZE)  # Total number of grid squares on y axis

    GRID_MID_Y = int(((SCREEN_HEIGHT / 2 + TOPBAR) / GRID_SIZE))  # Mid point on y axis in Grid coordinates
    GRID_MID_X = int(((SCREEN_WIDTH / 2 + LEFTBAR) / GRID_SIZE)) # Mid point on x axis in Grid coordinates

    # Grid boundaries in grid coordingates
    GRIDX_0 = int(LEFTBAR / GRID_SIZE)
    GRIDX_MAX = int((SCREEN_WIDTH + LEFTBAR) / GRID_SIZE)

    GRIDY_0 = int(TOPBAR / GRID_SIZE)
    GRIDY_MAX = int((SCREEN_HEIGHT + TOPBAR) / GRID_SIZE)

    TOP_BAR = (0,0,WINDOW_WIDTH,T_SIZE * GRID_SIZE)
    BTM_BAR = (0, WINDOW_HEIGHT - (B_SIZE * GRID_SIZE), WINDOW_WIDTH, WINDOW_HEIGHT)
    LEFT_BAR = (0, 0, L_SIZE * GRID_SIZE, WINDOW_HEIGHT)
    RIGHT_BAR = (WINDOW_WIDTH - (R_SIZE * GRID_SIZE), 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    surface = None

    BTM_FONT = pygame.font.Font("freesansbold.ttf", min(int(SCREEN_WIDTH/15), 30))
    ONSCREEN_FONT = pygame.font.Font("freesansbold.ttf", int(SCREEN_WIDTH/15))

    CHESSMEN = {}

    @classmethod
    def start_screen(cls):
        """ Starts screen with options as spceified above in the class fields """

        cls.surface = pygame.display.set_mode(cls.WINDOW_SIZE)
        pygame.display.set_caption(cls.S_TITLE)

        cls.fill_background()
        cls.draw_top_bar()
        cls.draw_btm_bar()
        cls.draw_left_bar()
        cls.draw_right_bar()

    @classmethod
    def fill_background(cls):
        """ Fills background with game_bg_color """
        cls.surface.fill(cls.BG_COLOR)

    @classmethod
    def draw_top_bar(cls):
        """ Draws score bar on display surface """
        pygame.draw.rect(cls.surface, cls.T_BG_COLOR, cls.TOP_BAR)

    @classmethod
    def draw_right_bar(cls):
        """ Draws score bar on display surface """
        pygame.draw.rect(cls.surface, cls.R_BG_COLOR, cls.RIGHT_BAR)

    @classmethod
    def draw_btm_bar(cls):
        """ Draws score bar on display surface """
        pygame.draw.rect(cls.surface, cls.B_BG_COLOR, cls.BTM_BAR)

    @classmethod
    def draw_left_bar(cls):
        """ Draws score bar on display surface """
        pygame.draw.rect(cls.surface, cls.L_BG_COLOR, cls.LEFT_BAR)

    @classmethod
    def display_btm_info(cls, msg):
        """ Displays the msg onto the bottom of the window where the bottom bar is """
        btm_surface = cls.BTM_FONT.render(msg, True, Screen.FONT_COLOR)
        btm_rect = btm_surface.get_rect()
        btm_rect.center = (cls.WINDOW_WIDTH / 2, cls.WINDOW_HEIGHT - (cls.BOTTOMBAR / 2))
        cls.surface.blit(btm_surface, btm_rect)

    @classmethod
    def display_msg(cls, msg):
        """ Displays msg onto the middle of the screen """
        display_msg_surface = cls.ONSCREEN_FONT.render(msg, True, Screen.FONT_COLOR)
        display_msg_rect = display_msg_surface.get_rect()
        display_msg_rect.center = (cls.WINDOW_WIDTH / 2,
                                (cls.WINDOW_HEIGHT - cls.BOTTOMBAR - cls.TOPBAR) /2 + cls.TOPBAR)
        cls.surface.blit(display_msg_surface, display_msg_rect)

    @classmethod
    def display_top_info(cls, msg):
        """ Displays the msg onto the top of the window where the top bar is """
        top_surface = cls.BTM_FONT.render(msg, True, Screen.FONT_COLOR)
        top_rect = top_surface.get_rect()
        top_rect.center = (cls.WINDOW_WIDTH / 2, cls.TOPBAR / 2)
        cls.surface.blit(top_surface, top_rect)

    @classmethod
    def draw_checkered_board(cls):
        """ Draws chess board colours """
        board = pygame.Surface((Screen.SCREEN_SIZE[0] * Screen.GRID_SIZE, Screen.SCREEN_SIZE[1] * Screen.GRID_SIZE))
        colours = {1: LIGHT, -1: DARK}
        colour = 1
        for row in range(Screen.SCREEN_SIZE[0]):
            for square in range(Screen.SCREEN_SIZE[1]):
                sq_rect = (square * Screen.GRID_SIZE, row * Screen.GRID_SIZE, Screen.GRID_SIZE, Screen.GRID_SIZE)
                pygame.draw.rect(board, colours[colour], sq_rect)
                colour = -colour
            colour = -colour
        cls.surface.blit(board, (Screen.LEFTBAR, Screen.TOPBAR))


    @classmethod
    def load_all_chessmen(cls):
        """ Loads image files of all chessmen """
        Screen.CHESSMEN["king_w"] = \
            pygame.transform.scale(pygame.image.load(os.path.join('chess', 'images', 'king_w.png'))
                                   .convert_alpha(),(Screen.GRID_SIZE, Screen.GRID_SIZE))
        Screen.CHESSMEN["king_b"] = \
            pygame.transform.scale(pygame.image.load(os.path.join('chess', 'images', 'king_b.png'))
                                   .convert_alpha(), (Screen.GRID_SIZE, Screen.GRID_SIZE))
        Screen.CHESSMEN["queen_w"] = \
            pygame.transform.scale(pygame.image.load(os.path.join('chess', 'images', 'queen_w.png'))
                                   .convert_alpha(), (Screen.GRID_SIZE, Screen.GRID_SIZE))
        Screen.CHESSMEN["queen_b"] = \
            pygame.transform.scale(pygame.image.load(os.path.join('chess', 'images', 'queen_b.png'))
                                   .convert_alpha(), (Screen.GRID_SIZE, Screen.GRID_SIZE))
        Screen.CHESSMEN["rook_w"] = \
            pygame.transform.scale(pygame.image.load(os.path.join('chess', 'images', 'rook_w.png'))
                                   .convert_alpha(),(Screen.GRID_SIZE, Screen.GRID_SIZE))
        Screen.CHESSMEN["rook_b"] = \
            pygame.transform.scale(pygame.image.load(os.path.join('chess', 'images', 'rook_b.png'))
                                   .convert_alpha(),(Screen.GRID_SIZE, Screen.GRID_SIZE))
        Screen.CHESSMEN["bishop_w"] = \
            pygame.transform.scale(pygame.image.load(os.path.join('chess', 'images', 'bishop_w.png'))
                                   .convert_alpha(), (Screen.GRID_SIZE, Screen.GRID_SIZE))
        Screen.CHESSMEN["bishop_b"] = \
            pygame.transform.scale(pygame.image.load(os.path.join('chess', 'images', 'bishop_b.png'))
                                   .convert_alpha(), (Screen.GRID_SIZE, Screen.GRID_SIZE))
        Screen.CHESSMEN["knight_w"] = \
            pygame.transform.scale(pygame.image.load(os.path.join('chess', 'images', 'knight_w.png'))
                                   .convert_alpha(), (Screen.GRID_SIZE, Screen.GRID_SIZE))
        Screen.CHESSMEN["knight_b"] = \
            pygame.transform.scale(pygame.image.load(os.path.join('chess', 'images', 'knight_b.png'))
                                   .convert_alpha(), (Screen.GRID_SIZE, Screen.GRID_SIZE))
        Screen.CHESSMEN["pawn_w"] = \
            pygame.transform.scale(pygame.image.load(os.path.join('chess', 'images', 'pawn_w.png'))
                                   .convert_alpha(), (Screen.GRID_SIZE, Screen.GRID_SIZE))
        Screen.CHESSMEN["pawn_b"] = \
            pygame.transform.scale(pygame.image.load(os.path.join('chess', 'images', 'pawn_b.png'))
                                   .convert_alpha(),(Screen.GRID_SIZE, Screen.GRID_SIZE))

    @classmethod
    def draw_all_chessmen(cls, board):
        """ Draws all chess men to board """
        boardsurf = pygame.Surface((Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGHT), SRCALPHA)
        for row, rank in enumerate(reversed(board)):
            for square, piece in enumerate(rank):
                if piece is not EMPTY:
                    sq_rect = (square * Screen.GRID_SIZE, row * Screen.GRID_SIZE, Screen.GRID_SIZE, Screen.GRID_SIZE)
                    boardsurf.blit(Screen.CHESSMEN[piece.image], sq_rect)
        cls.surface.blit(boardsurf, (Screen.LEFTBAR, Screen.TOPBAR))


    @classmethod
    def draw_circle_on_square(cls, square):
        """ Draws a circle on inputted square """
        sq_rect = (square[1] * Screen.GRID_SIZE + Screen.LEFTBAR, (7 - square[0]) * Screen.GRID_SIZE + Screen.TOPBAR,
                   Screen.GRID_SIZE, Screen.GRID_SIZE)
        pygame.draw.ellipse(cls.surface, RED, sq_rect, 1)

    @classmethod
    def draw_dot_on_square(cls, square, color=YELLOW_T):
        """ Draws a dot on inputted square """
        sq_pos = (square[1] * Screen.GRID_SIZE + Screen.LEFTBAR, (7 - square[0]) * Screen.GRID_SIZE + Screen.TOPBAR)
        square_surface = pygame.Surface((Screen.GRID_SIZE, Screen.GRID_SIZE), SRCALPHA)
        dot_diameter = 6
        dot_pos = (int(0.5 * Screen.GRID_SIZE), int(0.5 * Screen.GRID_SIZE))
        pygame.draw.circle(square_surface, color, dot_pos, dot_diameter)
        cls.surface.blit(square_surface, sq_pos)

    @classmethod
    def highlight_square(cls, square, color=RED):
        """ Highlights inputted square """
        sq_pos = (square[1] * Screen.GRID_SIZE + Screen.LEFTBAR, (7 - square[0]) * Screen.GRID_SIZE + Screen.TOPBAR)
        square_surface = pygame.Surface((Screen.GRID_SIZE, Screen.GRID_SIZE))
        square_surface.set_alpha(128)
        square_surface.fill(color)
        cls.surface.blit(square_surface, sq_pos)


    @staticmethod
    def update():
        """ Updates Screen """
        pygame.display.update()




# ================ FOR TESTING PURPOSES ================ #

if __name__ == "__main__":

    Screen.start_screen()
    Screen.draw_checkered_board()

    board = Board()
    Screen.load_all_chessmen()
    Screen.draw_all_chessmen(board.BOARD)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        Screen.update()
