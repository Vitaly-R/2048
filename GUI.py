import pygame
import os


class GUI:
    __IMG_DIR = "Images"
    __BG_COLOR = (90, 90, 90)
    __TEXT_COLOR = (200, 200, 200)
    # Maps the values of the blocks to their (background, text) colors.
    __BLOCK_COLORS = {1:     ((230, 230, 230), (230, 230, 230), 40),
                      2:     ((255, 255, 200), (0, 0, 0), 40),
                      4:     ((255, 255, 170), (0, 0, 0), 40),
                      8:     ((255, 255, 135), (0, 0, 0), 40),
                      16:    ((255, 255, 100), (0, 0, 0), 40),
                      32:    ((255, 255, 50), (0, 0, 0), 40),
                      64:    ((255, 255, 0), (0, 0, 0), 40),
                      128:   ((255, 200, 0), (60, 60, 60), 40),
                      256:   ((255, 160, 0), (60, 60, 60), 40),
                      512:   ((255, 120, 0), (60, 60, 60), 40),
                      1024:  ((255, 80, 0), (60, 60, 60), 35),
                      2048:  ((255, 40, 0), (60, 60, 60), 35),
                      4096:  ((255, 0, 0), (150, 150, 150), 35),
                      8192:  ((220, 0, 0), (150, 150, 150), 35),
                      16384: ((190, 0, 0), (200, 200, 200), 30),
                      32768: ((160, 0, 0), (200, 200, 200), 30),
                      65536: ((120, 0, 0), (200, 200, 200), 30),
                      131072: ((60, 0, 0), (200, 200, 200), 25)}
    __BLOCK_WIDTH = 96
    __BORDER_WIDTH = 2
    __FULL_CELL_WIDTH = __BLOCK_WIDTH + 2 * __BORDER_WIDTH

    def __init__(self, blocks):
        pygame.init()
        self.__screen = pygame.display.set_mode((blocks * self.__FULL_CELL_WIDTH, blocks * self.__FULL_CELL_WIDTH))
        self.__load_images()

    def __load_images(self):
        self.__start_screen = pygame.image.load(os.path.join(self.__IMG_DIR, "StartScreen.png"))
        self.__game_over_screen = pygame.image.load(os.path.join(self.__IMG_DIR, "GameOverScreen.png"))
        self.__respects_screen = pygame.image.load(os.path.join(self.__IMG_DIR, "RespectsScreen.png"))

    def show_start_screen(self):
        self.__screen.blit(self.__start_screen, (0, 0))
        pygame.display.flip()

    def show_main_game_screen(self, board):
        self.__screen.fill(self.__BG_COLOR)
        font_name = pygame.font.get_default_font()
        for row in range(len(board)):
            for col in range(len(board[row])):
                bg_color, text_color, text_size = self.__BLOCK_COLORS[board[row, col]]
                font = pygame.font.Font(font_name, text_size)
                text = font.render(str(board[row, col]), True, text_color)
                text_rect = text.get_rect()
                text_rect.center = (self.__FULL_CELL_WIDTH // 2 + col * self.__FULL_CELL_WIDTH, self.__FULL_CELL_WIDTH // 2 + row * self.__FULL_CELL_WIDTH)
                pygame.draw.rect(self.__screen, bg_color, pygame.Rect(self.__BORDER_WIDTH + col * self.__FULL_CELL_WIDTH,
                                                                      self.__BORDER_WIDTH + row * self.__FULL_CELL_WIDTH,
                                                                      self.__BLOCK_WIDTH, self.__BLOCK_WIDTH))
                self.__screen.blit(text, text_rect)
        pygame.display.flip()

    def show_game_over_screen(self):
        self.__screen.blit(self.__game_over_screen, (0, 0))
        pygame.display.flip()

    def show_respects_screen(self):
        self.__screen.blit(self.__respects_screen, (0, 0))
        pygame.time.wait(2000)
        pygame.display.flip()

    @staticmethod
    def end():
        pygame.quit()
