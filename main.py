import pygame
from pygame.locals import *

from data.scripts.clock import Clock
from data.scripts.font import Font
from data.scripts.image_functions import load_image, scale_image_ratio, scale_image_size
from data.scripts.border import Border
from data.scripts.player import Player
from data.scripts.background import Background
from data.scripts.food import Food
from data.scripts.file_manager import read_json, write_json
from data.scripts.enemy import Enemy
from data.scripts.moving_box import Box

pygame.init()
pygame.mixer.init()

def load_sound(file_name):
    return pygame.mixer.Sound("data/sounds/" + file_name)

def play_sound(sound):
    pygame.mixer.Sound.play(sound)


class Game:
    def __init__(self):
        self.size = [600, 600]
        self.screen = pygame.display.set_mode(self.size, 0, 32)

        pygame.display.set_caption("Box Dash")
        pygame.display.set_icon(load_image('icon.png'))

        # Images--------------------------#
        self.images = {
            load_image('space_key.png'): "Change arrow rotating direction",
            load_image('left_button.png'): "Shoot the player"
        }

        self.white_background = load_image('white_background.png', 100)
        self.black_background = load_image('black_background.png', 100)


        # Fonts-----------------------------#
        self.score_fonts = Font('small_font.png', (255, 255, 255), 2)

        # Music-----------------------------#
        self.burst = load_sound('burst.wav')
        self.buttonclick = load_sound('buttonclick.wav')
        self.ballbounce = load_sound('ballbounce.wav')

        pygame.mixer.music.load('data/sounds/background music.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.4)

        self.clock = Clock(30)
        self._game = True
        self.game_start = False

        # Text----------------#
        self.score_font = Font('small_font.png', (255, 255, 255), 4)
        self.instructions_font = Font('small_font.png', (255, 255, 255), 3)
        self.game_heading_1 = Font('large_font.png', (255, 255, 255), 10)
        self.game_heading_2 = Font('large_font.png', (255, 0, 0), 10)
        self.high_score_font = Font('large_font.png', (1, 0, 0), 7)
        self.score_font = Font('small_font.png', (255, 255, 255), 6)
        self.play_font = Font('small_font.png', (1, 0, 0), 4)

        self.reset_game()

        self.data = read_json('data.txt')
        self.data = self.data.split('\n')
        self.instruction, self.high_score = eval(self.data[0]), eval(self.data[1])



    def reset_game(self):
        self.game_over = False

        self.border = Border(self.size)
        self.food = Food(self.size)
        self.enemies = [
            Enemy(self.size, self.border.height, self.border.offset),
            Enemy(self.size, self.border.height, self.border.offset),
        ]

        self.background = Background()

        self.platforms = [
            self.border.top_rect,
            self.border.bottom_rect,
            self.border.right_rect,
            self.border.left_rect
        ]

        self.score = 0

        radius = 10
        player_pos = [self.border.offset[0] + self.border.height + radius, self.size[1] // 2]
        self.player = Player(*player_pos, radius)

    def start_screen(self):
        game = True
        _x = 10
        speed = -1
        hover = False
        moving_boxes = Box(self.size)

        while game:
            mouse_pos = pygame.mouse.get_pos()

            self.background.display(self.screen)

            if moving_boxes.display(self.screen):
                moving_boxes = Box(self.size)

            x = self.game_heading_1.get_width('Box Dash', 3)

            self.screen.blit(scale_image_size(self.white_background, x + 50, self.game_heading_1.image_height),
                             ((self.size[0] - x) // 2 - 25, 0))
            self.game_heading_1.display_fonts(self.screen, "Box Dash", [(self.size[0] - x) // 2, 10], 3)

            if _x < -10 or _x > 10:
                speed *= -1

            self.game_heading_2.display_fonts(self.screen, "Box Dash", [int((self.size[0] - x)) // 2 + _x, 10], 3)

            _x -= speed * 0.4

            high_score_x = self.high_score_font.get_width(f'{self.high_score}', 3)
            self.high_score_font.display_fonts(self.screen, f'{self.high_score}', [(self.size[0] - high_score_x) //
                                                                                   2, 180], 3)

            score_x = self.score_font.get_width(f'Score {self.score}', 3)
            self.score_font.display_fonts(self.screen, f'Score {self.score}', [(self.size[0] - score_x) //
                                                                                   2, 270], 3)

            play_x = self.play_font.get_width('Play', 3)

            background = None
            if ((self.size[0] - play_x) // 2 - 50 < mouse_pos[0] < (self.size[0] - play_x) // 2 + 110 and 390 <
                    mouse_pos[1] < 390 + self.play_font.image_height + 20):
                background = self.black_background
                hover = True
            else:
                background = self.white_background
                hover = False

            self.screen.blit(scale_image_size(background, play_x + 100, self.play_font.image_height + 20),
                             [(self.size[0] - play_x) // 2 - 50, 390])
            self.play_font.display_fonts(self.screen, 'Play', [(self.size[0] - play_x) // 2, 400])

            for event in pygame.event.get():
                if event.type == QUIT:
                    game = False
                    self._game = False

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.buttonclick.play()
                        if hover:
                            self.reset_game()
                            game = False

            pygame.display.update()
            self.clock.tick()

    def main(self):
        while self._game:
            self.background.display(self.screen)
            self.border.display(self.screen)

            if self.instruction:
                x = 50
                y = 50

                for image in self.images.keys():
                    y += image.get_height() + 50

                y //= 2

                for image, text in self.images.items():
                    self.screen.blit(image, (x, y))
                    self.instructions_font.display_fonts(self.screen, text, [x + image.get_width() + 50,
                                                                      y + image.get_height() // 2])
                    y += image.get_height() + 50
            else:
                self.high_score = max(self.high_score, self.score)

                food_captured = self.player.display(self.screen, self.food.rect, self.ballbounce, self.platforms)

                if food_captured:
                    self.food.get_pos()
                    self.score += 1

                    if self.score % 5 == 0:
                        for enemy in self.enemies:
                            enemy.speed += 1

                    if self.score % 10 == 0:
                        self.enemies.append(Enemy(self.size, self.border.height, self.border.offset))

                self.food.display(self.screen)

                self.score_font.display_fonts(self.screen, f'Score: {self.score}', [10, 10], 2)

                if self.game_over:
                    self.start_screen()

                for enemy in self.enemies:
                    if enemy.display(self.screen, self.player.rect):
                        self.game_over = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._game = False

                if event.type == KEYDOWN:
                    if not self.instruction:
                        if event.key == K_SPACE:
                            self.player.angle_speed *= -1
                    else:
                        self.instruction = False

                if event.type == MOUSEBUTTONDOWN:
                    if not self.instruction:
                        if event.button == 1:
                            self.burst.play()
                            self.player.shoot = True
                            self.player.shooting_angle = -self.player.angle
                    else:
                        self.instruction = False

            pygame.display.update()
            self.clock.tick()

if __name__ == "__main__":
    game = Game()
    game.start_screen()
    game.main()
    write_json('data.txt', f'False\n{game.high_score}')