import pygame
import random


class Background:
    def __init__(self):
        self.background_colors = [
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0),
            (255, 0, 255),
            (0, 255, 255),
        ]
        self.color = self.change_background()
        self.previous_color = self.color
        self.color_change_time = pygame.time.get_ticks()
        self.transition_duration = 1000

    def change_background(self):
        return random.choice(self.background_colors)

    def transition(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.color_change_time

        if elapsed >= self.transition_duration:
            return self.color

        progress = elapsed / self.transition_duration
        r = self.previous_color[0] + (self.color[0] - self.previous_color[0]) * progress
        g = self.previous_color[1] + (self.color[1] - self.previous_color[1]) * progress
        b = self.previous_color[2] + (self.color[2] - self.previous_color[2]) * progress

        return (int(r), int(g), int(b))

    def display(self, display):
        if pygame.time.get_ticks() - self.color_change_time > 5000:
            self.previous_color = self.color
            self.color = self.change_background()
            self.color_change_time = pygame.time.get_ticks()

        current_color = self.transition()
        display.fill(current_color)
