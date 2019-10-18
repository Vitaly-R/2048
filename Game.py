import pygame
import random as r
import numpy as np


class Game:

    __FACTOR = 3
    __DEF_BLOCK_LENGTH = 100
    __MAX_SCREEN_WIDTH = 500
    __BORDER_WIDTH = 4
    __MIN_BLOCKS = 4
    __MAX_BLOCKS = 25
    # Maps the log of values of the blocks to their background colors.
    __BLOCK_LEGEND = {0: (230, 230, 230),
                      1: (255, 255, 200),
                      2: (255, 255, 170),
                      3: (255, 255, 135),
                      4: (255, 255, 100),
                      5: (255, 255, 50),
                      6: (255, 255, 0),
                      7: (255, 200, 0),
                      8: (255, 160, 0),
                      9: (255, 120, 0),
                      10: (255, 80, 0),
                      11: (255, 40, 0),
                      12: (255, 0, 0),
                      13: (220, 0, 0),
                      14: (190, 0, 0),
                      15: (160, 0, 0),
                      16: (120, 0, 0),
                      17: (90, 0, 0),
                      18: (60, 0, 0),
                      19: (30, 0, 0),
                      20: (0, 0, 0)}
    # Maps the log of values of the blocks to their text colors.
    __TEXT_LEGEND = {0: (0, 0, 0),
                     1: (0, 0, 0),
                     2: (0, 0, 0),
                     3: (0, 0, 0),
                     4: (0, 0, 0),
                     5: (0, 0, 0),
                     6: (0, 0, 0),
                     7: (60, 60, 60),
                     8: (60, 60, 60),
                     9: (60, 60, 60),
                     10: (60, 60, 60),
                     11: (60, 60, 60),
                     12: (150, 150, 150),
                     13: (150, 150, 150),
                     14: (200, 200, 200),
                     15: (200, 200, 200),
                     16: (200, 200, 200),
                     17: (225, 225, 225),
                     18: (225, 225, 225),
                     19: (225, 225, 225),
                     20: (255, 255, 255)}
    __BOARD_BG_COLOR = (90, 90, 90)
    __DEF_TEXT_COLOR = (200, 200, 200)
    __DEF_TEXT_SIZE = 40
    __DEF_START_END_FONT = 'Arial'
    __DEF_GAME_FONT = 'David MS'

    def __init__(self, blocks=__MIN_BLOCKS):
        """
        Initializes the game.
        :param blocks: Number of blocks per row/column requested by the player.
        """
        pygame.init()
        pygame.font.init()
        self.__init_block_parameters(blocks)
        self.__init_screen()
        self.__init_starting_board()
        self.__init_move_handling()

    def __init_block_parameters(self, blocks):
        """
        Sets number of blocks and the length of each block (in pixels) on the screen.
        If the number of blocks requested is not between the minimal and maximal number of blocks, it will be
        changed as necessary.
        (Assumption - the number of blocks is always given as an integer)
        :param blocks: Number of blocks per row/column requested by the player.
        """
        self.__blocks = min(max(blocks, self.__MIN_BLOCKS), self.__MAX_BLOCKS)
        self.__block_length = min(self.__DEF_BLOCK_LENGTH, self.__MAX_SCREEN_WIDTH // self.__blocks)

    def __init_screen(self):
        """
        Initializes the game screen (window on which the game will be displayed).
        """
        self.__screen_width = self.__block_length * self.__blocks
        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_width))

    def __init_starting_board(self):
        """
        Initializes the array representing the board, and the flags to run and end the game.
        """
        self.__board = np.ones((self.__blocks, self.__blocks)).astype(np.int)
        self.__running = True
        self.__game_over = False

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
        self.__show_start_screen()
        self.__run_game()
        self.__quit()

    def __show_start_screen(self):
        """
        Shows start screen.
        """
        font = pygame.font.SysFont(self.__DEF_START_END_FONT, self.__DEF_TEXT_SIZE)
        text = font.render('Press \'Enter\' to start', False, self.__DEF_TEXT_COLOR)
        position = (self.__screen_width // 2 - text.get_width() // 2, self.__screen_width // 2 - text.get_height() // 2)
        self.__screen.fill(self.__BOARD_BG_COLOR)
        self.__screen.blit(text, position)
        pygame.display.flip()
        self.__wait_start()

    def __wait_start(self):
        """
        Waits for the player to respond during the start screen.
        """
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait = False
                    self.__running = False
                    break
                elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                    wait = False
                    break

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
        x, y = np.random.randint(0, self.__blocks, 2, int)
        while self.__board[y, x] != 1:
            x, y = np.random.randint(0, self.__blocks, 2, int)
        self.__board[y, x] = self.__board[y, x] * 2 if r.random() < 0.9 else self.__board[y, x] * 4

    def __run_game(self):
        """
        Runs the main part of the game.
        """
        self.__init_start_blocks()
        while self.__running:
            if self.__game_over:
                self.__show_game_over_screen()
            else:
                self.__do_loop()

    def __do_loop(self):
        """
        Runs the main loop of the game.
        """
        self.__screen.fill(self.__BOARD_BG_COLOR)
        self.__check_game_over()
        if not self.__game_over:
            self.__handle_events()
            self.__draw_blocks()
            self.__draw_text()
            pygame.display.flip()

    def __check_game_over(self):
        """
        Checks if the game should end by checking that there are no available positions, and that there are no
        legal moves remaining.
        """
        self.__game_over = 1 not in self.__board and \
            True not in [self.__board[i, j - 1] == self.__board[i, j]
                         for i in range(self.__blocks) for j in range(1, self.__blocks)] and \
            True not in [self.__board[i - 1, j] == self.__board[i, j]
                         for j in range(self.__blocks) for i in range(1, self.__blocks)]

    def __handle_events(self):
        """
        Handles events during the game.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                break
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
        # iterating over the columns
        for j in range(self.__board.shape[1]):
            lim = 0  # (uppermost row to check - starts at 0 and increases as more blocks move up)
            # iterating over the rows
            for i in range(1, self.__board.shape[0]):
                k = i  # (starting index of the block to move up, which is at position [k, j] during the next loop)
                while lim < k:
                    # We only need to move the block if its value is not 1, since it represents an empty place.
                    if self.__board[k - 1, j] == 1 and self.__board[k, j] != 1:
                        # This case is if the next position is free, and we simply need to move the block and
                        # then continue to the next iteration (if we haven't reached the limit).
                        self.__board[k - 1, j] = self.__board[k, j]
                        self.__moved = True
                        self.__board[k, j] = 1
                    elif self.__board[k - 1, j] == self.__board[k, j] and self.__board[k, j] != 1:
                        # This case is if the next position holds a block with an equal value to the one currently
                        # moving, in which case the two blocks will fuse to a new block with twice the value.
                        # In this case, we need to stop, so a new limit is set and the loop will break.
                        self.__board[k - 1, j] += self.__board[k, j]
                        self.__moved = True
                        self.__board[k, j] = 1
                        lim = k
                    else:
                        # In this case, the next position above is unavailable and has a block with a different value,
                        # so we simply break the loop
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

    def __draw_blocks(self):
        """
        Draws the blocks on the board.
        """
        for i in range(self.__board.shape[0]):
            for j in range(self.__board.shape[1]):
                b_color = self.__BLOCK_LEGEND[min(int(np.log2(self.__board[i, j])), 20)]
                pygame.draw.rect(self.__screen, b_color, pygame.Rect(j * self.__block_length + self.__BORDER_WIDTH // 2,
                                                                     i * self.__block_length + self.__BORDER_WIDTH // 2,
                                                                     self.__block_length - self.__BORDER_WIDTH,
                                                                     self.__block_length - self.__BORDER_WIDTH))

    def __draw_text(self):
        """
        Writes the text on all blocks with a value greater than 1.
        """
        for i in range(self.__board.shape[0]):
            for j in range(self.__board.shape[1]):
                if 1 < self.__board[i, j]:
                    index = min(int(np.log2(self.__board[i, j])), max(self.__TEXT_LEGEND.keys()))
                    t_color = self.__TEXT_LEGEND[index]
                    t_size = int(((10/11)**(len(str(self.__board[i, j])) - 1))*0.75 * self.__block_length)
                    font_f = pygame.font.SysFont(self.__DEF_GAME_FONT, t_size)
                    text = font_f.render(str(self.__board[i, j]), False, t_color)
                    position = ((j + 0.5) * self.__block_length - text.get_width() // 2,
                                (i + 0.5) * self.__block_length - text.get_height() // 2)
                    self.__screen.blit(text, position)

    def __show_game_over_screen(self):
        """
        Gets the messages for the 'Game Over' screen and passes them to a method which displays it.
        """
        msg, qut, rst, rsp = self.__get_game_over_messages()
        self.__do_game_over_loop(msg, qut, rst, rsp)

    def __get_game_over_messages(self):
        """
        Returns the text and position of the messages of the 'Game Over' screen.
        """
        font = pygame.font.SysFont(self.__DEF_START_END_FONT, self.__DEF_TEXT_SIZE)
        message = font.render('Game Over!', False, self.__DEF_TEXT_COLOR)
        message_pos = (self.__screen_width // 2 - message.get_width() // 2,
                       self.__screen_width // 2 - int(1.5 * message.get_height()))
        quit_game = font.render('Press \'Esc\' to quit', False, self.__DEF_TEXT_COLOR)
        quit_game_pos = (self.__screen_width // 2 - quit_game.get_width() // 2,
                         self.__screen_width // 2 - quit_game.get_height() // 2)
        restart = font.render('Press \'r\' to restart', False, self.__DEF_TEXT_COLOR)
        restart_pos = (self.__screen_width // 2 - restart.get_width() // 2,
                       self.__screen_width // 2 + restart.get_height() // 2)
        respect = font.render('Press \'f\' to respect', False, self.__DEF_TEXT_COLOR)
        respect_pos = (self.__screen_width // 2 - respect.get_width() // 2,
                       self.__screen_width - respect.get_height())
        return (message, message_pos), (quit_game, quit_game_pos), (restart, restart_pos), (respect, respect_pos)

    def __do_game_over_loop(self, msg, qut, rst, rsp):
        """
        Displays the 'Game Over' screen and waits for the player to respond.
        Each parameter is a tuple of a message and its position on the screen.
        """
        (message, message_pos) = msg
        (quit_game, quit_game_pos) = qut
        (restart, restart_pos) = rst
        (respect, respect_pos) = rsp
        wait = True
        clock = pygame.time.Clock()
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    wait = False
                    self.__running = False
                    break
                elif event.type == pygame.KEYUP and event.key == pygame.K_r:
                    wait = False
                    self.__restart_game()
                    break
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    self.__respect(clock)
            self.__show_messages(message, message_pos, quit_game, quit_game_pos,
                                 restart, restart_pos, respect, respect_pos)
            pygame.display.flip()

    def __restart_game(self):
        """
        Restarts the game (resets the array representing the board).
        """
        self.__init_starting_board()
        self.__init_start_blocks()

    def __respect(self, clock):
        """
        Displays the 'Respect' screen.
        :param clock: A pygame clock object.
        """
        self.__screen.fill((255, 255, 255))
        font_2 = pygame.font.SysFont('comicsansms', 60, True)
        text = font_2.render('Respect', False, (0, 0, 0))
        position = (self.__screen_width // 2 - text.get_width() // 2,
                    self.__screen_width // 2 - text.get_height() // 2)
        self.__screen.blit(text, position)
        pygame.display.flip()
        clock.tick(0.5)

    def __show_messages(self, message, message_pos, quit_game, quit_game_pos,
                        restart, restart_pos, respect, respect_pos):
        """
        Displays the messages of the 'Game Over' screen.
        """
        self.__screen.fill(self.__BOARD_BG_COLOR)
        self.__screen.blit(message, message_pos)
        self.__screen.blit(quit_game, quit_game_pos)
        self.__screen.blit(restart, restart_pos)
        self.__screen.blit(respect, respect_pos)

    @staticmethod
    def __quit():
        """
        Terminates pygame.
        """
        pygame.font.quit()
        pygame.quit()
