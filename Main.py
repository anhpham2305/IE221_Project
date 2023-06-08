import pygame, os, time

from Game import Game
from PlayerAI import Ai
from Constants import *

"""
2048 Game

This program implements the popular game 2048 using the Pygame library.
It allows the player to manually control the game or let an AI play automatically.

Requirements:
    - Python 3.x
    - Pygame library

Classes:
    - Main: The main game controller responsible for managing game states, event handling, and rendering the game interface.
    - Button: Represents a clickable button in the game interface.

Constants and Configurations:
    - FPS: Frames per second for the game.
    - SIZE: Default grid size for the game.
    - SIZE_5x5, SIZE_6x6, SIZE_8x8: Alternative grid sizes for the game.
    - DEBUG: Flag for enabling debug mode.
    - colors: Dictionary of colors for different tile values.
    - GAME_WH: Width and height of the game grid.
    - WINDOW_W, WINDOW_H: Width and height of the game window.

Functions:
    - run(): Entry point for starting the game.

Usage:
    Run the script to start the game. The game window will appear, and you can interact with it using the keyboard or mouse.
    The objective of the game is to reach the 2048 tile by merging tiles with the same value. The game ends when there are no
    valid moves left or when the 2048 tile is reached.

    Controls:
    - Arrow keys or 'W', 'A', 'S', 'D': Move the tiles in the corresponding directions.
    - 'Start' button: Start a new game renders 4x4 grid.
    - 'Auto' button: Enable or disable auto-play mode.
    - '5x5', '6x6', '8x8' buttons: Change the grid size.

    Enjoy playing 2048!

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


class Main:
    def __init__(self):
        global FPS
        pygame.init()
        os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (100, 50)
        self.set_window_size(WINDOW_W, WINDOW_H, title="2048")
        self.state = "start"
        self.fps = FPS
        self.catch_n = 0
        self.clock = pygame.time.Clock()
        self.game = Game(SIZE)
        self.ai = Ai()
        self.step_time = config.STEP_TIME
        self.next_f = ""
        self.last_time = time.time()
        self.jm = -1
        self.sound_played = False
        self.move_sound = pygame.mixer.Sound("./sound/move_sound.wav")
        self.win_sound = pygame.mixer.Sound("./sound/win_sound.wav")
        self.lose_sound = pygame.mixer.Sound("./sound/lose_sound.wav")
        self.time_limit = (
            6  # Mức thời gian cho chế độ chơi tính thời gian (60 giây trong ví dụ)
        )
        self.start_time = 0  # Thời gian bắt đầu chơi
        self.time_mode = False

    def start(self):
        # Load buttons
        self.button_list = [
            Button("start", "Restart", (GAME_WH + 60, 130)),
            Button("ai", "Auto", (GAME_WH + 60, 220)),
            Button("time", "Time", (GAME_WH + 60, 310)),  # Thêm button "Time"
            # Button('size_5x5', '5x5', (GAME_WH + 60, 310)),
            # Button('size_6x6', '6x6', (GAME_WH + 60, 400)),
            # Button('size_8x8', '8x8', (GAME_WH + 60, 490))
        ]
        self.run()

    def run(self):
        time_start = 0
        while self.state != "exit":
            if self.game.state in ["over", "win"]:
                self.state = self.game.state
            self.handle_events()
            if self.next_f != "" and (
                self.state == "run"
                or self.state == "ai"
                or self.state == "time"
                and time.time() - self.last_time > self.step_time
            ):
                self.game.run(self.next_f)
                self.next_f = ""
                self.last_time = time.time()
            elif self.state == "start":
                self.game.start()
                self.state = "run"
            self.set_background((146, 135, 125))
            self.draw_info()
            self.draw_buttons(self.button_list)
            self.draw_grid()
            self.update()
        print("Exiting the game")

    def end_game(self):
        # ...
        if (
            self.state == "time"
        ):  # Thêm điều kiện xử lý khi kết thúc trò chơi tính thời gian
            self.state = "over"
            self.draw_text("Time's up!", (GAME_WH + 60, 200))
            self.draw_text(
                "Final Score: {}".format(self.game.score), (GAME_WH + 60, 240)
            )

    # ...

    def draw_grid(self):
        for y in range(SIZE):
            for x in range(SIZE):
                self.draw_block((x, y), self.game.grid.tiles[y][x])
        if self.state == "over":
            pygame.draw.rect(self.screen, (0, 0, 0, 0.5), (0, 0, GAME_WH, GAME_WH))
            self.draw_text(
                "Game Over!", (GAME_WH / 2, GAME_WH / 2), size=25, center="center"
            )
        elif self.state == "win":
            pygame.draw.rect(self.screen, (0, 0, 0, 0.5), (0, 0, GAME_WH, GAME_WH))
            self.draw_text(
                "You Win!", (GAME_WH / 2, GAME_WH / 2), size=25, center="center"
            )
        if self.next_f != "":
            if not self.sound_played:
                self.move_sound.play()
                self.sound_played = True
        elif self.state == "win":
            if not self.sound_played:
                self.win_sound.play()
                self.sound_played = True
        elif self.state == "over":
            if not self.sound_played:
                self.lose_sound.play()
                self.sound_played = True

    # Draw a block
    # Vẽ một ô vuông
    def draw_block(self, xy, number):
        one_size = GAME_WH / SIZE
        dx = int(one_size * 0.05)  # Khoảng cách giữa các ô vuông
        radius = int(one_size * 0.1)  # Độ cong của góc bo tròn
        x, y = xy[0] * one_size, (xy[1] + 0.5) * one_size
        color = colors[str(int(number))] if number <= 2048 else (0, 0, 255)
        pygame.draw.rect(
            self.screen,
            color,
            (x + dx, y + dx, one_size - 2 * dx, one_size - 2 * dx),
            border_radius=radius,
        )

        if number != 0:
            font_size = int(one_size * 0.4)
            font_color = (20, 20, 20) if number <= 4 else (250, 250, 250)
            font = pygame.font.SysFont("None", font_size)
            text = font.render(str(int(number)), True, font_color)
            text_rect = text.get_rect(center=(x + one_size / 2, y + one_size / 2))
            self.screen.blit(text, text_rect)

    def draw_info(self):
        self.draw_text("Score: {}".format(self.game.score), (GAME_WH + 60, 40))
        if self.state == "ai":
            self.draw_text("Interval: {}".format(self.step_time), (GAME_WH + 60, 60))
            self.draw_text("Evaluation: {}".format(self.jm), (GAME_WH + 60, 80))
        if self.state == "time":
            current_time = time.time() - self.start_time
            remaining_time = self.time_limit - current_time

            # Chuyển đổi thời gian từ giây sang phút:giây
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)

            # Định dạng thời gian dưới dạng chuỗi phút:giây
            time_text = "{:02d}:{:02d}".format(minutes, seconds)

            # Vẽ thông tin thời gian lên màn hình
            self.draw_text("Time: {}".format(time_text), (GAME_WH + 60, 100))

    def set_background(self, color=(255, 0, 0)):
        self.screen.fill(color)

    def draw_buttons(self, buttons):
        for b in buttons:
            if b.is_show:
                pygame.draw.rect(
                    self.screen, (200, 200, 200), (b.x, b.y, b.w, b.h), border_radius=10
                )  # Bo tròn góc của button
                self.draw_text(
                    b.text, (b.x + b.w / 2, b.y + b.h / 2), size=18, center="center"
                )

    def draw_text(self, text, xy, color=(0, 0, 0), size=18, center=None):
        font = pygame.font.Font(None, round(size))
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        if center == "center":
            text_rect.center = xy
        else:
            text_rect.topleft = xy
        self.screen.blit(text_obj, text_rect)

    # Set window size
    def set_window_size(self, w, h, title="Python Game"):
        self.screen2 = pygame.display.set_mode((w, h), pygame.DOUBLEBUF, 32)
        self.screen = self.screen2.convert_alpha()
        pygame.display.set_caption(title)

    def update(self):
        self.screen2.blit(self.screen, (0, 0))
        # Refresh the screen
        # pygame.display.update()
        pygame.display.flip()
        time_passed = self.clock.tick(self.fps)
        if self.state == "time":
            current_time = time.time() - self.start_time
            remaining_time = self.time_limit - current_time

            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)

            time_text = "{:02d}:{:02d}".format(minutes, seconds)

            self.draw_text("Time: {}".format(time_text), (GAME_WH + 60, 100))

            if remaining_time <= 0:
                self.end_game()

    # Event handling
    # Event handling
    def handle_events(self):
        if self.state == "ai" and self.next_f == "":
            self.next_f, self.jm = self.ai.get_next(self.game.grid.tiles)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "exit"
                elif event.key in [pygame.K_LEFT, pygame.K_a] and self.state in [
                    "run",
                    "time",
                ]:
                    self.next_f = "L"
                    self.move_sound.play()
                elif event.key in [pygame.K_RIGHT, pygame.K_d] and self.state in [
                    "run",
                    "time",
                ]:
                    self.next_f = "R"
                    self.move_sound.play()
                elif event.key in [pygame.K_DOWN, pygame.K_s] and self.state in [
                    "run",
                    "time",
                ]:
                    self.next_f = "D"
                    self.move_sound.play()
                elif event.key in [pygame.K_UP, pygame.K_w] and self.state in [
                    "run",
                    "time",
                ]:
                    self.next_f = "U"
                    self.move_sound.play()
                elif event.key in [pygame.K_k, pygame.K_l] and self.state == "ai":
                    if event.key == pygame.K_k and self.step_time > 0:
                        self.step_time *= 0.9
                    if event.key == pygame.K_l and self.step_time < 10:
                        if self.step_time != 0:
                            self.step_time *= 1.1
                        else:
                            self.step_time = 0.01
                    if self.step_time < 0:
                        self.step_time = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in self.button_list:
                    if i.is_click(event.pos):
                        if i.name == "time":
                            if not self.time_mode:
                                self.time_mode = True
                                self.start_time = time.time()
                                time_start = time.time()
                            else:
                                self.time_mode = False

                        if i.name == "size_5x5":
                            self.game = Game(SIZE_5x5)
                            self.state = "start"
                        elif i.name == "size_6x6":
                            self.game = Game(SIZE_6x6)
                            self.state = "start"
                        elif i.name == "size_8x8":
                            self.game = Game(SIZE_8x8)
                            self.state = "start"
                        else:
                            self.state = i.name
                            if i.name == "start":
                                self.game.start()  # Bắt đầu trò chơi
                                self.game.score = 0  # Đặt điểm số về 0
                                self.state = "run"
                            if i.name == "ai":
                                i.name = "run"
                                i.text = "Cancel Auto"
                            elif i.name == "run":
                                i.name = "ai"
                                i.text = "Auto Play"
                        break


def main_menu():
    pygame.init()
    os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (100, 50)
    main_game = Main()
    main_game.start()


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
        return (
            self.is_show
            and self.x <= xy[0] <= self.x + self.w
            and self.y <= xy[1] <= self.y + self.h
        )


if __name__ == "__main__":
    run()
