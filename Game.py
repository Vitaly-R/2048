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
        pygame.init()
        pygame.font.init()
        self.__init_block_parameters(blocks)
        self.__init_screen()
        self.__init_starting_board()
        self.__init_move_handling()

    def __init_block_parameters(self, blocks):
        self.__blocks = min(max(blocks, self.__MIN_BLOCKS), self.__MAX_BLOCKS)
        self.__block_length = min(self.__DEF_BLOCK_LENGTH, self.__MAX_SCREEN_WIDTH // self.__blocks)

    def __init_screen(self):
        self.__screen_width = self.__block_length * self.__blocks
        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_width))

    def __init_starting_board(self):
        self.__board = np.ones((self.__blocks, self.__blocks)).astype(np.int)
        self.__running = True
        self.__game_over = False

    def __init_move_handling(self):
        self.__moves = {pygame.K_UP: self.__move_up,
                        pygame.K_DOWN: self.__move_down,
                        pygame.K_LEFT: self.__move_left,
                        pygame.K_RIGHT: self.__move_right}
        self.__moved = False

    def run(self):
        self.__show_start_screen()
        self.__init_game()
        self.__run_game()
        self.__quit()

    def __show_start_screen(self):
        self.__screen.fill(self.__BOARD_BG_COLOR)
        font = pygame.font.SysFont(self.__DEF_START_END_FONT, self.__DEF_TEXT_SIZE)
        text = font.render('Press \'Enter\' to start', False, self.__DEF_TEXT_COLOR)
        position = (self.__screen_width // 2 - text.get_width() // 2, self.__screen_width // 2 - text.get_height() // 2)
        self.__screen.blit(text, position)
        pygame.display.flip()
        self.__wait_start()

    def __wait_start(self):
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

    def __init_game(self):
        self.__create_block()
        self.__create_block()

    def __create_block(self):
        x = r.randint(0, self.__blocks - 1)
        y = r.randint(0, self.__blocks - 1)
        while self.__board[y, x] != 1:
            x = r.randint(0, self.__blocks - 1)
            y = r.randint(0, self.__blocks - 1)
        self.__board[y, x] *= 2
        if 0.9 <= r.random():
            self.__board[y, x] *= 2

    def __run_game(self):
        while self.__running:
            if self.__game_over:
                self.__show_game_over_screen()
            else:
                self.__do_loop()

    def __do_loop(self):
        self.__screen.fill(self.__BOARD_BG_COLOR)
        self.__check_game_over()
        if not self.__game_over:
            self.__handle_events()
            self.__draw_blocks()
            self.__draw_text()
            pygame.display.flip()

    def __check_game_over(self):
        if 1 not in self.__board:
            self.__game_over = self.__no_horizontal_possible_moves() and self.__no_vertical_possible_moves()

    def __no_horizontal_possible_moves(self):
        exists = False
        for i in range(self.__blocks):
            for j in range(1, self.__blocks):
                if self.__board[i, j-1] == self.__board[i, j]:
                    exists = True
        return not exists

    def __no_vertical_possible_moves(self):
        exists = False
        for j in range(self.__blocks):
            for i in range(1, self.__blocks):
                if self.__board[i-1, j] == self.__board[i, j]:
                    exists = True
        return not exists

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                break
            elif event.type == pygame.KEYDOWN and event.key in self.__moves.keys():
                self.__handle_movement(event)

    def __handle_movement(self, event):
        self.__moved = False
        self.__moves[event.key]()
        if self.__moved:
            self.__create_block()

    def __move_up(self):
        for j in range(self.__board.shape[1]):
            lim = 0
            for i in range(1, self.__board.shape[0]):
                k = i
                m = 0
                while lim < k:
                    if self.__board[k - 1, j] == 1 and self.__board[k, j] != 1:
                        self.__board[k - 1, j] = self.__board[k, j]
                        m += 1
                        self.__moved = True
                        self.__board[k, j] = 1
                    elif self.__board[k - 1, j] == self.__board[k, j] and self.__board[k, j] != 1:
                        self.__board[k - 1, j] += self.__board[k, j]
                        self.__moved = True
                        self.__board[k, j] = 1
                        m += 1
                        lim = k
                        break
                    else:
                        break
                    k -= 1

    def __move_down(self):
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
                        break
                    else:
                        break
                    k += 1

    def __move_left(self):
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
                        break
                    else:
                        break
                    k -= 1

    def __move_right(self):
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
                        break
                    else:
                        break
                    k += 1

    def __draw_blocks(self):
        for i in range(self.__board.shape[0]):
            for j in range(self.__board.shape[1]):
                b_color = self.__BLOCK_LEGEND[min(int(np.log2(self.__board[i, j])), 20)]
                pygame.draw.rect(self.__screen, b_color, pygame.Rect(j * self.__block_length + self.__BORDER_WIDTH // 2,
                                                                     i * self.__block_length + self.__BORDER_WIDTH // 2,
                                                                     self.__block_length - self.__BORDER_WIDTH,
                                                                     self.__block_length - self.__BORDER_WIDTH))

    def __draw_text(self):
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
        msg, qut, rst, rsp = self.__get_game_over_messages()
        self.__do_game_over_loop(msg, qut, rst, rsp)

    def __get_game_over_messages(self):
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
        self.__init_starting_board()
        self.__init_game()

    def __respect(self, clock):
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
        self.__screen.fill(self.__BOARD_BG_COLOR)
        self.__screen.blit(message, message_pos)
        self.__screen.blit(quit_game, quit_game_pos)
        self.__screen.blit(restart, restart_pos)
        self.__screen.blit(respect, respect_pos)

    @staticmethod
    def __quit():
        pygame.font.quit()
        pygame.quit()
