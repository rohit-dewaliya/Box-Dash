import pygame
import random


class Food:
    def __init__(self, screen_size):
        self.x = None
        self.y = None
        self.x_range = [150, screen_size[0] - 150]
        self.y_range = [150, screen_size[1] - 150]
        self.size = 20
        self.color = (255, 0, 0)
        self.rect = None

        self.get_pos()

    def get_pos(self):
        self.x = random.randint(*self.x_range)
        self.y = random.randint(*self.y_range)

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def display(self, display):
        pygame.draw.rect(display, self.color, self.rect)