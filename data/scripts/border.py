import pygame


class Border:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.offset = [100, 100]
        self.lenght = self.screen_size[0] - self.offset[0] * 2
        self.height = 10
        self.top_rect = pygame.Rect(self.offset[0], self.offset[1], self.lenght, self.height)
        self.bottom_rect = pygame.Rect(self.offset[0], self.screen_size[1] - self.offset[1], self.lenght,
        self.height)
        self.left_rect = pygame.Rect(self.offset[0], self.offset[1], self.height, self.lenght)
        self.right_rect = pygame.Rect(self.screen_size[0] - self.offset[0], self.offset[1], self.height, self.lenght + 10)


    def display(self, display):
        pygame.draw.rect(display, (0, 0, 0), self.top_rect)
        pygame.draw.rect(display, (0, 0, 0), self.bottom_rect)
        pygame.draw.rect(display, (0, 0, 0), self.left_rect)
        pygame.draw.rect(display, (0, 0, 0), self.right_rect)