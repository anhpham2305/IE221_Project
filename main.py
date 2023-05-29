try:
    import pygame, os, time
except:
    print('cmd run: pip3 install pygame -i https://mirrors.aliyun.com/pypi/simple')
    exit()
from pygame.locals import *
from game import Game
from ai import Ai
from config import *
"""
2048 Game

This program implements the popular game 2048 using the Pygame library.
It allows the player to manually control the game or let an AI play automatically.

Usage:
    - Use arrow keys or 'W', 'A', 'S', 'D' keys to move the tiles in the game.
    - Click the 'Start' button to start a new game.
    - Click the 'Auto' button to let the AI play automatically.
    - Click the '5x5', '6x6', '8x8' buttons to change the grid size.
    - Press 'K' key to decrease the AI's move interval.
    - Press 'L' key to increase the AI's move interval.

Requirements:
    - Python 3.x
    - Pygame library

Author:
    Hong Anh

Date:
    2023-06
"""

# config = Development()
config = SupperFast()

FPS = config.FPS
SIZE = config.SIZE
SIZE_5x5 = config.SIZE_5x5
SIZE_6x6 = config.SIZE_6x6
SIZE_8x8 = config.SIZE_8x8
DEBUG = config.DEBUG
colors = config.COLORS
GAME_WH = config.GAME_WH
WINDOW_W = config.WINDOW_W
WINDOW_H = config.WINDOW_H

# Font in the grid


class Main():
    def __init__(self):
        global FPS
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 50)
        self.set_window_size(WINDOW_W, WINDOW_H, title='2048')
        self.state = 'start'
        self.fps = FPS
        self.catch_n = 0
        self.clock = pygame.time.Clock()
        self.game = Game(SIZE)
        self.ai = Ai()
        self.step_time = config.STEP_TIME
        self.next_f = ''
        self.last_time = time.time()
        self.jm = -1

    def start(self):
        # Load buttons
        self.button_list = [
            Button('start', 'Start', (GAME_WH + 60, 130)),
            Button('ai', 'Auto', (GAME_WH + 60, 220)),
            Button('size_5x5', '5x5', (GAME_WH + 60, 310)),
            Button('size_6x6', '6x6', (GAME_WH + 60, 400)),
            Button('size_8x8', '8x8', (GAME_WH + 60, 490))
        ]
        self.run()

    def run(self):
        while self.state != 'exit':
            if self.game.state in ['over', 'win']:
                self.state = self.game.state
            self.handle_events()
            if self.next_f != '' and (
                    self.state == 'run' or self.state == 'ai' and time.time() - self.last_time > self.step_time):
                self.game.run(self.next_f)
                self.next_f = ''
                self.last_time = time.time()
            elif self.state == 'start':
                self.game.start()
                self.state = 'run'
            self.set_background((146, 135, 125))
            self.draw_info()
            self.draw_buttons(self.button_list)
            self.draw_grid()
            self.update()
        print('Exiting the game')

    def draw_grid(self):
        for y in range(SIZE):
            for x in range(SIZE):
                self.draw_block((x, y), self.game.grid.tiles[y][x])
        if self.state == 'over':
            pygame.draw.rect(self.screen, (0, 0, 0, 0.5),
                             (0, 0, GAME_WH, GAME_WH))
            self.draw_text('Game Over!', (GAME_WH / 2, GAME_WH / 2), size=25, center='center')
        elif self.state == 'win':
            pygame.draw.rect(self.screen, (0, 0, 0, 0.5),
                             (0, 0, GAME_WH, GAME_WH))
            self.draw_text('You Win!', (GAME_WH / 2, GAME_WH / 2), size=25, center='center')

    # Draw a block
    # Vẽ một ô vuông
    def draw_block(self, xy, number):
        one_size = GAME_WH / SIZE
        dx = int(one_size * 0.05)  # Khoảng cách giữa các ô vuông
        radius = int(one_size * 0.1)  # Độ cong của góc bo tròn
        x, y = xy[0] * one_size, xy[1] * one_size
        color = colors[str(int(number))] if number <= 2048 else (0, 0, 255)
        pygame.draw.rect(self.screen, color, (x + dx, y + dx, one_size - 2 * dx, one_size - 2 * dx), border_radius=radius)
    
        if number != 0:
            font_size = int(one_size * 0.4)
            font_color = (20, 20, 20) if number <= 4 else (250, 250, 250)
            font = pygame.font.SysFont('None', font_size)
            text = font.render(str(int(number)), True, font_color)
            text_rect = text.get_rect(center=(x + one_size / 2, y + one_size / 2))
            self.screen.blit(text, text_rect)


    def draw_info(self):
        self.draw_text('Score: {}'.format(self.game.score), (GAME_WH + 60, 40))
        if self.state == 'ai':
            self.draw_text('Interval: {}'.format(self.step_time), (GAME_WH + 60, 60))
            self.draw_text('Evaluation: {}'.format(self.jm), (GAME_WH + 60, 80))

    def set_background(self, color=(255, 0, 0)):
        self.screen.fill(color)

    def capture_screen(self, filename=None):
        if filename is None:
            filename = "./catch/catch-{:04d}.png".format(self.catch_n)
        pygame.image.save(self.screen, filename)
        self.catch_n += 1

    def draw_buttons(self, buttons):
        for b in buttons:
            if b.is_show:
                pygame.draw.rect(self.screen, (200, 200, 200),
                                (b.x, b.y, b.w, b.h), border_radius=10)  # Bo tròn góc của button
                self.draw_text(b.text, (b.x + b.w / 2, b.y + b.h / 2), size=18, center='center')


    def draw_text(self, text, xy, color=(0, 0, 0), size=18, center=None):
        font = pygame.font.SysFont('None', round(size))
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        if center == 'center':
            text_rect.center = xy
        else:
            text_rect.topleft = xy
        self.screen.blit(text_obj, text_rect)


    # Set window size
    def set_window_size(self, w, h, title='Python Game'):
        self.screen2 = pygame.display.set_mode((w, h), pygame.DOUBLEBUF, 32)
        self.screen = self.screen2.convert_alpha()
        pygame.display.set_caption(title)

    def update(self):
        self.screen2.blit(self.screen, (0, 0))
        # Refresh the screen
        # pygame.display.update()
        pygame.display.flip()
        time_passed = self.clock.tick(self.fps)

    # Event handling
    def handle_events(self):
        if self.state == 'ai' and self.next_f == '':
            self.next_f, self.jm = self.ai.get_next(self.game.grid.tiles)
        for event in pygame.event.get():
            if event.type == QUIT:
                self.state = 'exit'
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.state = 'exit'
                elif event.key in [K_LEFT, K_a] and self.state == 'run':
                    self.next_f = 'L'
                elif event.key in [K_RIGHT, K_d] and self.state == 'run':
                    self.next_f = 'R'
                elif event.key in [K_DOWN, K_s] and self.state == 'run':
                    self.next_f = 'D'
                elif event.key in [K_UP, K_w] and self.state == 'run':
                    self.next_f = 'U'
                elif event.key in [K_k, K_l] and self.state == 'ai':
                    if event.key == K_k and self.step_time > 0:
                        self.step_time *= 0.9
                    if event.key == K_l and self.step_time < 10:
                        if self.step_time != 0:
                            self.step_time *= 1.1
                        else:
                            self.step_time = 0.01
                    if self.step_time < 0:
                        self.step_time = 0

            if event.type == MOUSEBUTTONDOWN:
                for i in self.button_list:
                    if i.is_click(event.pos):
                        if i.name == 'size_5x5':
                            self.game = Game(SIZE_5x5)
                            self.state = 'start'
                        elif i.name == 'size_6x6':
                            self.game = Game(SIZE_6x6)
                            self.state = 'start'
                        elif i.name == 'size_8x8':
                            self.game = Game(SIZE_8x8)
                            self.state = 'start'
                        else:
                            self.state = i.name
                            if i.name == 'ai':
                                i.name = 'run'
                                i.text = 'Cancel Auto'
                            elif i.name == 'run':
                                i.name = 'ai'
                                i.text = 'Auto Play'
                        break



def run():
    Main().start()


# Button class
class Button(pygame.sprite.Sprite):
    def __init__(self, name, text, xy, size=(100, 50)):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.text = text
        self.x, self.y = xy[0], xy[1]
        self.w, self.h = size
        self.is_show = True

    def is_click(self, xy):
        return (self.is_show and
                self.x <= xy[0] <= self.x + self.w and
                self.y <= xy[1] <= self.y + self.h)


if __name__ == '__main__':
    run()
