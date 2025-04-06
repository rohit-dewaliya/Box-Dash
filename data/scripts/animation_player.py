import pygame
from data.scripts.image_functions import load_image, scale_image_ratio


def load_animations(name):
    path = 'data/images/animations/' + name + '/' + name + '.txt'
    file = open(path, 'r')
    data = file.read()
    data = data.split('\n')

    animation_data = {}

    size = [0, 0]
    for info in data:
        ani_name = info.split(':')[0]
        ani_data = info.split(':')[1]

        ani_path = 'animations/' + name + '/' + ani_name
        animation = []
        for num in range(0, len(ani_data)):
            frames = ani_data[num]
            img = scale_image_ratio(load_image(ani_path + '/' + ani_name + '_' + str(num + 1) + '.png'), 1)
            size = [img.get_width(), img.get_height()]

            for frame in range(0, int(frames)):
                animation.append(img)
        animation_data[ani_name] = animation

    return animation_data, size


class AnimationPlayer(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = [0, 0]
        self.flip = False
        self.animation_data = {}
        self.animation_frame = 0
        self.animation_state = 'flying'
        self.previous_animation_state = 'flying'
        self.animation = None
        self.start_animation = False

    # Loading the Animations-------------------------------------------------#
    def animations(self, path):
        self.animation_data, self.size = load_animations(path)
        self.current_animation()

    # Setting the Current Animation----------------------------------------#
    def current_animation(self):
        self.animation = self.animation_data[self.animation_state]
        self.start_animation = True

    # Playing the Animation-----------------------------------------#
    def play_animation(self, display, scroll):
        if self.start_animation:
            if self.animation_state == self.previous_animation_state:
                if self.animation_frame == len(self.animation):
                    self.animation_frame = 0
                    self.start_animation = True

            else:
                self.animation_frame = 0
                self.previous_animation_state = self.animation_state
                self.current_animation()

            display.blit(pygame.transform.flip(self.animation[self.animation_frame], self.flip, False),
                         (self.x - int(scroll[0]) - self.size[0] // 2, self.y - int(scroll[1]) - self.size[1] // 2))
            self.animation_frame += 1
