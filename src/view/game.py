# import necessary libs
import pygame as pg
from random import randint
# import other modules
from model.errors import IllegalMove
from model.grid import AGENT, HUMAN, Grid
from model.agent import Agent
from view.main_frame import MainFrame

# define constants 
TITLE = 'Connect 4'

# scenery
BACKGROUND_COLOUR = (200,200,200)

# images paths
ICON = 'src/img/favicon.png'
RED_PLAYER = 'src/img/red_70x70.png'
YELLOW_PLAYER = 'src/img/yellow_70x70.png'
BOARD = 'src/img/Board_640x480.png'

# Cooridinates of the screen
HEIGHT = 600
WIDTH = 800

# player image sizes
PLAYER_HEIGHT = 70
PLAYER_WIDTH = 70

BOARD_HEIGHT = 480
BOARD_WIDTH = 640

# initial player cords
PLAYER_X_INIT = 130 - PLAYER_WIDTH / 2
PLAYER_Y_INIT = 500 - PLAYER_HEIGHT / 2

# distances
HORIZONTAL_MOVE = 90
VERTICAL_MOVE = 80

# boundaries
HORIZONTAL_BOUND = 635
VERTICAL_BOUND = 65
NO_ROWS = 6
NO_COLUMNS = 7

FLOATING_Y = VERTICAL_BOUND - VERTICAL_MOVE / 2

class Game:

    # Initialize pygame and load images
    def __init__(self, ai_agent: Agent, frame: MainFrame):
        
        self.__frame = frame
        pg.init()
        self.__icon = pg.image.load(ICON)
        self.__human_player = pg.image.load(RED_PLAYER)
        self.__ai_player = pg.image.load(YELLOW_PLAYER)
        self.__board = pg.image.load(BOARD)
        self.__state_grid = Grid()
        self.__agent = ai_agent
        self.__turn = HUMAN
        
        # game loop variables
        self.__running = True
        
        # player column prior to pressing enter
        self.__col = 0

        # real time player coordinated
        self.__player_x = PLAYER_X_INIT
        self.__player_y = FLOATING_Y

        #  set scene attributes
        self.__screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)

        pg.display.set_icon(self.__icon)

    # function to draw player
    def __place_player(self, player = HUMAN, x= WIDTH/2, y=HEIGHT/2):
        #choose loaded player image
        if player == HUMAN:
            player_img = self.__human_player
        else :
            player_img = self.__ai_player

        # set boundaries
        x = x if x <= HORIZONTAL_BOUND and x >= PLAYER_X_INIT else PLAYER_X_INIT
        y = y if y >= FLOATING_Y and y <= PLAYER_Y_INIT else PLAYER_Y_INIT

        self.__screen.blit(player_img, (x, y))

    def __move_left(self, player_x = HORIZONTAL_BOUND):
        return player_x - HORIZONTAL_MOVE if player_x > PLAYER_X_INIT else HORIZONTAL_BOUND


    def __move_right(self, player_x = PLAYER_X_INIT):
        return player_x + HORIZONTAL_MOVE  if player_x < HORIZONTAL_BOUND else PLAYER_X_INIT

    def __move_to_row_column(self,row,column):
        return PLAYER_X_INIT + HORIZONTAL_MOVE * ( column % NO_COLUMNS), VERTICAL_BOUND + VERTICAL_MOVE * (row % NO_ROWS)
    def get_state_grid(self):
        return self.__state_grid

    def set_state_grid(self,grid):
        self.__state_grid = grid

    def __handle_events(self):
        for event in pg.event.get():
            # Quit on exit button click
            if event.type == pg.QUIT:
                self.__running = False
            # if it's human's turn take thier move
            elif self.__turn == HUMAN and event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.__player_x = self.__move_left(self.__player_x)
                    self.__col = (self.__col - 1) % NO_COLUMNS
                elif event.key == pg.K_RIGHT:
                    self.__player_x = self.__move_right(self.__player_x)
                    self.__col = (self.__col + 1) % NO_COLUMNS
                elif event.key == pg.K_RETURN:
                    try:
                        self.__state_grid.make_a_move(self.__col, HUMAN)
                        self.__frame.show_score(self.__state_grid.get_score())
                        self.__turn = AGENT
                        print(self.__state_grid.get_grid_array())
                    except(IllegalMove):
                        pass

    # game loop
    def go(self):
        
        # randomly pick a starter
        if randint(0,1) == 0:
            self.__state_grid.make_a_move(NO_COLUMNS / 2,AGENT)

        while self.__running:
            
            self.__handle_events()
                        
            # set background colour
            self.__screen.fill(BACKGROUND_COLOUR)

            # place players on board
            for i in range(NO_ROWS):
                for j in range(NO_COLUMNS):
                    p = self.__state_grid.get_grid_array()[i][j] 
                    if(p != 0):
                        p_x, p_y = self.__move_to_row_column(i, j)
                        self.__place_player(p, p_x, p_y)

            # board
            self.__screen.blit(self.__board, (WIDTH / 2 - BOARD_WIDTH / 2 , HEIGHT / 2 - BOARD_HEIGHT / 2))
            

            if self.__state_grid.is_terminal():
                print("score =",self.__state_grid.get_score())
                # TODO: end the game properly
                self.__running = False
            elif self.__turn == HUMAN:
                self.__place_player(self.__turn,self.__player_x,self.__player_y)
            elif self.__turn == AGENT:
                pg.display.update() 
                self.__state_grid = self.__agent.move(self.__state_grid, self.__frame.alpha_beta_pruning())
                self.__frame.show_score(self.__state_grid.get_score())

                # output the tree
                self.__agent.tree_to_svg("out\\tree")
                self.__frame.show_time()
                self.__turn = HUMAN


            # update scene
            pg.display.update() 
            self.__frame.update()
