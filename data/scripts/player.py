import pygame
import math

from data.scripts.image_functions import load_image


class Player:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.arrow = load_image('arrow.png', 200)
        self.angle = 0
        self.angle_speed = 1
        self.shooting_angle = 0
        self.shoot = False
        self.shooting_speed = 10

        self.trail = []
        self.max_trail_length = 20
        self.trail_fade_speed = 15

    def blit_center(self, display):
        rotated_arrow = pygame.transform.rotate(self.arrow, self.angle)
        rotated_rect = rotated_arrow.get_rect(center=(self.x, self.y))
        display.blit(rotated_arrow, rotated_rect.topleft)

        self.angle += self.angle_speed
        if self.angle >= 360:
            self.angle = 0

    def set_pos(self):
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

    def change_offset(self, offset):
        self.x -= offset[0]
        self.y -= offset[1]
        self.set_pos()

    def shoot_player(self, ballbounce, platforms):
        coors = self.find_coordinates(self.shooting_speed, math.radians(self.shooting_angle))
        new_x = self.x + coors[0]
        new_y = self.y + coors[1]

        test_rect = pygame.Rect(new_x - self.radius, new_y - self.radius, self.radius * 2, self.radius * 2)

        collision_found = False

        for platform in platforms:
            if test_rect.colliderect(platform):
                ballbounce.play()
                collision_found = True

                dx = test_rect.centerx - platform.centerx
                dy = test_rect.centery - platform.centery
                width = (test_rect.width + platform.width) / 2
                height = (test_rect.height + platform.height) / 2
                overlap_x = width - abs(dx)
                overlap_y = height - abs(dy)

                if overlap_x > overlap_y:
                    self.angle = -90 if dy > 0 else 90
                else:
                    self.angle = 0 if dx > 0 else 180
                break

        if not collision_found:
            self.trail.append([self.x, self.y, 200])
            if len(self.trail) > self.max_trail_length:
                self.trail.pop(0)
            self.x = new_x
            self.y = new_y
        else:
            self.shoot = False
            return True

        self.set_pos()

        return False

    def find_coordinates(self, distance, angle):
        y = distance * math.sin(angle)
        x = distance * math.cos(angle)
        return [x, y]

    def draw_transparent_circle(self, surface, color, pos, radius, alpha):
        temp_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(temp_surface, color + (alpha,), (radius, radius), radius)
        surface.blit(temp_surface, (pos[0] - radius, pos[1] - radius))

    def draw_trail(self, display):
        new_trail = []
        for x, y, alpha in self.trail:
            if alpha > 0:
                self.draw_transparent_circle(display, (245, 245, 245), (x, y), self.radius, alpha)
                new_trail.append([x, y, alpha - self.trail_fade_speed])
        self.trail = new_trail

    def display(self, display, food, ballbounce, platforms = []):
        self.draw_trail(display)

        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), self.radius + 1)
        self.draw_transparent_circle(display, (255, 255, 255), (self.x, self.y), self.radius, 255)

        if not self.shoot:
            self.blit_center(display)

        if self.shoot:
            self.shoot_player(ballbounce, platforms)
            if self.rect.colliderect(food):
                return True

        return False