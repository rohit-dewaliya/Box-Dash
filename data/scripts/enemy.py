import random
import pygame


class Enemy:
    def __init__(self, screen_size, width, offset):
        self.screen_size = screen_size
        self.width = width
        self.offset = offset

        self.size = 20
        self.points = self.get_points()

        self.pos = random.choice(self.points)
        self.index = self.points.index(self.pos)

        self.speed = 2
        self.target = self.get_new_target()
        self.rect = pygame.Rect(*self.pos, self.size, self.size)

    def get_points(self):
        point_1 = [self.offset[0] + self.width, self.offset[1] + self.width]
        point_2 = [self.screen_size[0] - self.offset[0] - self.size, self.offset[1] + self.width]
        point_3 = [self.screen_size[0] - self.offset[0] - self.size, self.screen_size[1] - self.offset[1] - self.size]
        point_4 = [self.offset[0] + self.width, self.screen_size[1] - self.offset[1] - self.size]
        return [point_1, point_2, point_3, point_4]

    def get_new_target(self):
        self.points = self.get_points()
        options = [self.points[(self.index - 1) % 4], self.points[(self.index + 1) % 4]]
        new_target = random.choice(options)
        self.target_index = self.points.index(new_target)
        return new_target

    def move_toward_target(self):
        dx = self.target[0] - self.pos[0]
        dy = self.target[1] - self.pos[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < self.speed:
            self.pos = self.target
            self.index = self.target_index
            self.target = self.get_new_target()
        else:
            self.pos[0] += self.speed * dx / distance
            self.pos[1] += self.speed * dy / distance

        self.rect.topleft = (int(self.pos[0]), int(self.pos[1]))

    def display(self, display, rect):
        self.move_toward_target()
        pygame.draw.rect(display, (0, 0, 0), self.rect)

        if self.rect.colliderect(rect):
            return True

        return False