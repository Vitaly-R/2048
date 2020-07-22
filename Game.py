import pygame
import random as r
import numpy as np
from GUI import GUI


class Game:

    __BLOCKS = 4

    def __init__(self):
        """
        Initializes the game.
        """
        self.__gui = GUI(self.__BLOCKS)
        self.__init_board()
        self.__init_move_handling()
        self.__events = None

    def __init_board(self):
        """
        Initializes the array representing the board, and the flags to run and end the game.
        """
        self.__board = np.ones((self.__BLOCKS, self.__BLOCKS)).astype(np.int)
        self.__init_start_blocks()
        self.__running = True
        self.__start_screen = True
        self.__playing = False
        self.__game_over = False

    def __init_start_blocks(self):
        """
        Initializes two starting blocks before the game starts.
        """
        self.__create_block()
        self.__create_block()

    def __create_block(self):
        """
        Creates a block in a random available position on the board.
        A position on the board is available if its value is 1.
        (In the context of the game, a block is simply a number on the board.)
        """
        x, y = np.random.randint(0, self.__BLOCKS, 2, int)
        while self.__board[y, x] != 1:
            x, y = np.random.randint(0, self.__BLOCKS, 2, int)
        self.__board[y, x] = self.__board[y, x] * 2 if r.random() < 0.9 else self.__board[y, x] * 4

    def __init_move_handling(self):
        """
        Initializes a dictionary mapping each legal move to a method handling it, and a flag indicating that
        blocks on the board moved.
        """
        self.__moves = {pygame.K_UP: self.__move_up,
                        pygame.K_DOWN: self.__move_down,
                        pygame.K_LEFT: self.__move_left,
                        pygame.K_RIGHT: self.__move_right}
        self.__moved = False

    def run(self):
        """
        Runs the entire game.
        """
        while self.__running:
            self.__events = pygame.event.get()
            if self.__start_screen:
                self.__do_start_screen_loop()
            elif self.__playing:
                self.__do_main_game_loop()
            elif self.__game_over:
                pass
            else:
                pass
        self.__gui.end()

    def __do_start_screen_loop(self):
        self.__gui.show_start_screen()
        for event in self.__events:
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self.__start_screen = False
                    self.__playing = True

    def __do_main_game_loop(self):
        """
        Runs the main loop of the game.
        """
        self.__gui.show_main_game_screen(self.__board)
        self.__check_game_over()
        if self.__playing:
            self.__handle_events()

    def __check_game_over(self):
        """
        Checks if the game should end by checking that there are no available positions, and that there are no
        legal moves remaining.
        """
        self.__playing = (1 in self.__board or
                          True in [self.__board[i, j - 1] == self.__board[i, j] for i in range(self.__BLOCKS) for j in range(1, self.__BLOCKS)] or
                          True in [self.__board[i - 1, j] == self.__board[i, j] for j in range(self.__BLOCKS) for i in range(1, self.__BLOCKS)])
        self.__game_over = not self.__playing

    def __handle_events(self):
        """
        Handles events during the game.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type == pygame.KEYDOWN and event.key in self.__moves.keys():
                self.__handle_movement(event)

    def __handle_movement(self, event):
        """
        Handles moves by the player.
        :param event: The event representing the move made by the player.
        """
        self.__moved = False
        self.__moves[event.key]()
        if self.__moved:
            self.__create_block()

    def __move_up(self):
        """ Handles an 'up' move. """
        for j in range(self.__board.shape[1]):
            lim = 0
            for i in range(1, self.__board.shape[0]):
                k = i
                while lim < k:
                    if self.__board[k - 1, j] == 1 and self.__board[k, j] != 1:
                        self.__board[k - 1, j] = self.__board[k, j]
                        self.__moved = True
                        self.__board[k, j] = 1
                    elif self.__board[k - 1, j] == self.__board[k, j] and self.__board[k, j] != 1:
                        self.__board[k - 1, j] += self.__board[k, j]
                        self.__moved = True
                        self.__board[k, j] = 1
                        lim = k
                    else:
                        break
                    k -= 1

    def __move_down(self):
        """ Handles a 'down' move. """
        for j in range(self.__board.shape[1]):
            lim = self.__board.shape[0] - 1
            for i in range(self.__board.shape[0] - 2, -1, -1):
                k = i
                while k < lim:
                    if self.__board[k + 1, j] == 1 and self.__board[k, j] != 1:
                        self.__board[k + 1, j] = self.__board[k, j]
                        self.__moved = True
                        self.__board[k, j] = 1
                    elif self.__board[k + 1, j] == self.__board[k, j] and self.__board[k, j] != 1:
                        self.__board[k + 1, j] += self.__board[k, j]
                        self.__moved = True
                        self.__board[k, j] = 1
                        lim = k
                    else:
                        break
                    k += 1

    def __move_left(self):
        """ Handles a 'left' move. """
        for i in range(self.__board.shape[0]):
            lim = 0
            for j in range(1, self.__board.shape[1]):
                k = j
                while lim < k:
                    if self.__board[i, k - 1] == 1 and self.__board[i, k] != 1:
                        self.__board[i, k - 1] = self.__board[i, k]
                        self.__moved = True
                        self.__board[i, k] = 1
                    elif self.__board[i, k - 1] == self.__board[i, k] and self.__board[i, k] != 1:
                        self.__board[i, k - 1] += self.__board[i, k]
                        self.__moved = True
                        self.__board[i, k] = 1
                        lim = k
                    else:
                        break
                    k -= 1

    def __move_right(self):
        """ Handles a 'right' move. """
        for i in range(self.__board.shape[0]):
            lim = self.__board.shape[1] - 1
            for j in range(self.__board.shape[1] - 2, -1, -1):
                k = j
                while k < lim:
                    if self.__board[i, k + 1] == 1 and self.__board[i, k] != 1:
                        self.__board[i, k + 1] = self.__board[i, k]
                        self.__moved = True
                        self.__board[i, k] = 1
                    elif self.__board[i, k + 1] == self.__board[i, k] and self.__board[i, k] != 1:
                        self.__board[i, k + 1] += self.__board[i, k]
                        self.__moved = True
                        self.__board[i, k] = 1
                        lim = k
                    else:
                        break
                    k += 1

    def __do_game_over_loop(self):
        """
        Displays the 'Game Over' screen and waits for the player to respond.
        Each parameter is a tuple of a message and its position on the screen.
        """
        self.__gui.show_game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                self.__running = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_r:
                self.__restart_game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                self.__game_over = False

    def __restart_game(self):
        """
        Restarts the game (resets the array representing the board).
        """
        self.__init_board()
        self.__start_screen = False
        self.__playing = True

    def __do_respects_loop(self):
        self.__gui.show_respects_screen()
        self.__game_over = True
