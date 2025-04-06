import random

import pygame
from pygame.locals import *

from data.scripts.clock import Clock
from data.scripts.font import Font
from data.scripts.image_functions import load_image, scale_image_ratio
from data.scripts.border import Border
from data.scripts.player import Player
from data.scripts.background import Background

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

        self.background = Background()

        radius = 10
        player_pos = [self.border.offset[0] + self.border.height + radius, self.size[1] // 2]
        self.player = Player(*player_pos, radius)

    def main(self):
        while self._game:

            self.background.display(self.screen)

            self.border.display(self.screen)
            self.player.display(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._game = False

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.player.angle_speed *= -1

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        print(self.player.angle)

            pygame.display.update()
            self.clock.tick()

if __name__ == "__main__":
    game = Game()
    game.main()