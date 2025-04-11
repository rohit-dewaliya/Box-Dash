import random

from data.scripts.image_functions import load_image, scale_image_size


class Box:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.alpha = 80
        self.images = []
        self.name = random.choice(['black_background.png', 'white_background.png'])
        self.direction = random.choice([0, 1])

        self.pos = random.randint(0, self.screen_size[0])

        for i in range(1, 6):
            image = scale_image_size(load_image(self.name, self.alpha + 30 * i), 100, 100)
            if self.direction:
                self.images.append([image, [-100 - 30 * (5 - i), self.pos]])
            else:
                self.images.append([image, [self.pos, -100 - 30 * (5 - i)]])

        self.speed = 10

    def display(self, display):
        for box in self.images:
            display.blit(box[0], box[1])

            if self.direction:
                box[1][0] += self.speed
            else:
                box[1][1] += self.speed

        if self.direction and self.images[0][1][0] > self.screen_size[0]:
            return True

        if not self.direction and self.images[0][1][1] > self.screen_size[1]:
            return True

        return False