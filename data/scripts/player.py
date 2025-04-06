import pygame

from data.scripts.image_functions import load_image

class Player:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.arrow = load_image('arrow.png')
        self.angle = 0
        self.angle_speed = 1

    def blit_center(self, display):
        rotated_arrow = pygame.transform.rotate(self.arrow, self.angle)
        rotated_rect = rotated_arrow.get_rect(center=(self.x, self.y))

        display.blit(rotated_arrow, rotated_rect.topleft)

        self.angle += self.angle_speed
        if self.angle >= 360:
            self.angle = 0

    def display(self, display):
        pygame.draw.circle(display, (255, 255, 255), (self.x, self.y), self.radius)
        self.blit_center(display)