import math
from random import randint, random

import tkinter as tk

from gamelib import Sprite, GameApp, Text

from consts import *

class Fruit(Sprite):

    value = 1

    def __init__(self, app, image_filename, x, y):
        super().__init__(app, image_filename, x, y)

        self.app = app

    def update(self):
        pass


class Strategy():
    def Slow(self, fruit):
        def update():
            fruit.x -= FRUIT_SLOW_SPEED
            if fruit.x < -30:
                fruit.to_be_deleted = True

        fruit.update = update
        return fruit

    def Fast(self, fruit):
        def update():
            fruit.x -= FRUIT_SLOW_SPEED

            if fruit.x < -30:
                fruit.to_be_deleted = True
        
        fruit.update = update
        return fruit

    def Slide(self, fruit):
        fruit.direction = randint(0,1)*2 - 1

        def update():
            fruit.x -= FRUIT_FAST_SPEED
            fruit.y += fruit.direction * 5

            if fruit.x < -30:
                fruit.to_be_deleted = True
        
        fruit.update = update
        return fruit
        
    def Curvy(self, fruit):
        fruit.t = randint(0,360) * 2 * math.pi / 360

        def update():
            fruit.x -= FRUIT_SLOW_SPEED * 1.2
            fruit.t += 1
            fruit.y += math.sin(fruit.t*0.08)*10

            if fruit.x < -30:
                fruit.to_be_deleted = True

        fruit.update = update
        return fruit


class FruitFactory():

    product = {"apple": [1, Strategy().Slow, "images/apple.png"],
               "banana": [2, Strategy().Fast, "images/banana.png"],
               "cherry": [3, Strategy().Slide, "images/cherry.png"],
               "pear": [4, Strategy().Curvy, "images/pear.png"]}

    def create(self, app, param, x, y):
        val, strat, image = self.product[param]
        fruit = Fruit(app, image, x, y)
        fruit.value = val
        
        return strat(fruit)


class Cat(Sprite):
    def __init__(self, app, x, y):
        super().__init__(app, 'images/cat.png', x, y)

        self.app = app
        self.direction = None

    def update(self):
        if self.direction == CAT_UP:
            if self.y >= CAT_MARGIN:
                self.y -= CAT_SPEED
        elif self.direction == CAT_DOWN:
            if self.y <= CANVAS_HEIGHT - CAT_MARGIN:
                self.y += CAT_SPEED

    def check_collision(self, fruit):
        if self.distance_to(fruit) <= CAT_CATCH_DISTANCE:
            fruit.to_be_deleted = True
            self.app.score += fruit.value
            self.app.update_score()


class CatGame(GameApp):
    def init_game(self):
        self.cat = Cat(self, 50, CANVAS_HEIGHT // 2)
        self.elements.append(self.cat)

        self.score = 0
        self.score_text = Text(self, 'Score: 0', 100, 40)
        self.fruits = []

        self.fac = FruitFactory()

    def update_score(self):
        self.score_text.set_text('Score: ' + str(self.score))

    def random_fruits(self):
        if random() > 0.95:
            p = random()
            y = randint(50, CANVAS_HEIGHT - 50)
            if p <= 0.3:
                new_fruit = self.fac.create(self, 'apple', CANVAS_WIDTH, y)
                # new_fruit = self.fac.SlowFruit(self, CANVAS_WIDTH, y)
            elif p <= 0.6:
                new_fruit = self.fac.create(self, 'banana', CANVAS_WIDTH, y)
                # new_fruit = self.fac.FastFruit(self, CANVAS_WIDTH, y)
            elif p <= 0.8:
                new_fruit = self.fac.create(self, 'cherry', CANVAS_WIDTH, y)
                # new_fruit = self.fac.SlideFruit(self, CANVAS_WIDTH, y)
            else:
                new_fruit = self.fac.create(self, "pear", CANVAS_WIDTH, y)
                # new_fruit = self.fac.CurvyFruit(self, CANVAS_WIDTH, y)

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
        if event.keysym == 'Up':
            self.cat.direction = CAT_UP
        elif event.keysym == 'Down':
            self.cat.direction = CAT_DOWN
    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Fruit Cat")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = CatGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
