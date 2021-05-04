import math
from random import randint, random

import tkinter as tk

from gamelib import Sprite, GameApp, Text, KeyPress

from consts import *


class Fruit(Sprite):
    Point = 0

    def __init__(self, app, image, x, y):
        super().__init__(app, image, x, y)
        self.app = app
        self.direction = randint(0, 1)*2 - 1
        self.t = randint(0, 360) * 2 * math.pi / 360

    def move(self):
        if self.x < -30:
            self.to_be_deleted = True


class SlowFruit(Fruit):
    point = 1

    def update(self):
        self.x -= FRUIT_SLOW_SPEED
        self.move()


class FastFruit(Fruit):
    point = 2

    def update(self):
        self.x -= FRUIT_FAST_SPEED
        self.move()


class SlideFruit(Fruit):
    point = 3

    def update(self):
        self.x -= FRUIT_FAST_SPEED
        self.y += self.direction * 5
        self.move()


class CurvyFruit(Fruit):
    point = 4

    def update(self):
        self.x -= FRUIT_SLOW_SPEED * 1.2
        self.t += 1
        self.y += math.sin(self.t*0.08)*10
        self.move()


class Pressed(KeyPress):
    def execute(self, event):
        if event.keysym == 'Up':
            return CAT_UP
        elif event.keysym == 'Down':
            return CAT_DOWN


class Cat(Sprite):
    def __init__(self, app, x, y):
        super().__init__(app, 'images/cat.png', x, y)

        self.app = app
        self.direction = None

    def ovservera(self):
        if self.y < 0-(2*CAT_MARGIN):
            self.y = CANVAS_HEIGHT + (2*CAT_MARGIN)

    def ovserverb(self):
        if self.y >= CANVAS_HEIGHT+(2*CAT_MARGIN):
            self.y = -(2*CAT_MARGIN)

    def update(self):
        if self.direction == CAT_UP:
            self.y -= CAT_SPEED
            self.ovservera()
        elif self.direction == CAT_DOWN:
            self.y += CAT_SPEED
            self.ovserverb()

    def check_collision(self, fruit):
        if self.distance_to(fruit) <= CAT_CATCH_DISTANCE:
            fruit.to_be_deleted = True
            self.app.score += fruit.point
            self.app.update_score()


class CatGame(GameApp):
    def init_game(self):
        self.cat = Cat(self, 50, CANVAS_HEIGHT // 2)
        self.elements.append(self.cat)

        self.score = 0
        self.score_text = Text(self, 'Score: 0', 100, 40)
        self.fruits = []
        self.key_event = Pressed()

    def update_score(self):
        self.score_text.set_text('Score: ' + str(self.score))

    def random_fruits(self):
        if random() > 0.95:
            p = random()
            y = randint(50, CANVAS_HEIGHT - 50)
            if p <= 0.3:
                new_fruit = SlowFruit(
                    self, 'images/apple.png', CANVAS_WIDTH, y)
            elif p <= 0.6:
                new_fruit = FastFruit(
                    self, 'images/banana.png', CANVAS_WIDTH, y)
            elif p <= 0.8:
                new_fruit = SlideFruit(
                    self, 'images/cherry.png', CANVAS_WIDTH, y)
            else:
                new_fruit = CurvyFruit(
                    self, 'images/pear.png', CANVAS_WIDTH, y)

            self.fruits.append(new_fruit)

    def process_collisions(self):
        for f in self.fruits:
            self.cat.check_collision(f)

    def update_and_filter_deleted(self, elements):
        new_list = []
        for e in elements:
            e.update()
            e.render()
            if e.to_be_deleted:
                e.delete()
            else:
                new_list.append(e)
        return new_list

    def post_update(self):
        self.process_collisions()

        self.random_fruits()

        self.fruits = self.update_and_filter_deleted(self.fruits)

    def on_key_pressed(self, event):
        self.cat.direction = self.key_event.execute(event)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Fruit Cat")

    # do not allow window resizing
    root.resizable(False, False)
    app = CatGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
