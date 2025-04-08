import pygame
from pygame.locals import *

from data.scripts.clock import Clock
from data.scripts.font import Font
from data.scripts.image_functions import load_image, scale_image_ratio
from data.scripts.border import Border
from data.scripts.player import Player
from data.scripts.background import Background
from data.scripts.food import Food
from data.scripts.file_manager import read_json, write_json

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


        # Fonts-----------------------------#
        self.score_fonts = Font('small_font.png', (255, 255, 255), 2)

        # Music-----------------------------#
        # self.jump = load_sound('jump.wav')
        #
        # pygame.mixer.music.load('data/sounds/background music.mp3')
        # pygame.mixer.music.play(-1)
        # pygame.mixer.music.set_volume(0.4)

        # self.score = 0
        # self.highest_score = 0
        self.clock = Clock(30)
        self._game = True
        self.game_start = False

        self.border = Border(self.size)
        self.food = Food(self.size)

        self.background = Background()

        self.platforms = [
            self.border.top_rect,
            self.border.bottom_rect,
            self.border.right_rect,
            self.border.left_rect
        ]

        # Text----------------#
        self.score_font = Font('small_font.png', (255, 255, 255), 4)
        self.instructions_font = Font('small_font.png', (255, 255, 255), 3)

        self.score = 0

        radius = 10
        player_pos = [self.border.offset[0] + self.border.height + radius, self.size[1] // 2]
        self.player = Player(*player_pos, radius)

        self.instruction = eval(read_json('data.txt'))
        if self.instruction:
            write_json('data.txt', 'False')

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
                food_captured = self.player.display(self.screen, self.food.rect, self.platforms)

                if food_captured:
                    self.food.get_pos()
                    self.score += 1

                self.food.display(self.screen)

                self.score_font.display_masked_fonts(self.screen, f'Score: {self.score}', [10, 10], 2)

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
                            self.player.shoot = True
                            self.player.shooting_angle = -self.player.angle
                    else:
                        self.instruction = False

            pygame.display.update()
            self.clock.tick()

if __name__ == "__main__":
    game = Game()
    game.main()