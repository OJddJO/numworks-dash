from kandinsky import fill_rect as fRect,draw_string as dStr,get_pixel as gCol
from ion import *
from time import sleep
from random import randint

class Cube:
    def __init__(self):
        self.col = (0, 0, 150)
    
    def draw(self):
        fRect(30, 180, 10, 10, self.col)

    def gravity(self):
        pass

class Spike:
    def __init__(self, x, y):
        self.col = (240, 0, 0)
        self.pos = [x, y]
        self.destroy = False

    def draw(self):
        fRect(self.pos[0]+4, self.pos[1], 2, 2, self.col)
        fRect(self.pos[0]+3, self.pos[1]+2, 4, 2, self.col)
        fRect(self.pos[0]+2, self.pos[1]+4, 6, 2, self.col)
        fRect(self.pos[0]+1, self.pos[1]+6, 8, 2, self.col)
        fRect(self.pos[0], self.pos[1]+8, 10, 2, self.col)

    def move(self):
        self.pos[0] -= 1
        for i in range(5):
            fRect(self.pos[0]+6-i+2*i, self.pos[1]+2*i, 1, 2, (255, 255, 255))
        if self.pos[0]+10 < 0:
            self.destroy = True

    def update(self):
        self.draw()
        self.move()


class Structure:
    def __init__(self, y):
        self.interval = [40, 160]
        if y > self.interval[1]:
            y = self.interval[1]
        elif y < self.interval[0]:
            y = self.interval[0]
        self.structureElement = []
        return y

    def draw(self):
        for element in self.structureElement:
            element.update()


class triSpike(Structure):
    def __init__(self, y):
        self.pos = [320, super().__init__(y)]
        for i in range(3):
            self.structureElement.append(Spike(self.pos[0]+10*i, self.pos[1]))
