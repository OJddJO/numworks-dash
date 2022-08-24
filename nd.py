from kandinsky import fill_rect as fRect,draw_string as dStr,get_pixel as gCol
from ion import *
from time import sleep
from random import randint

class Cube:
    def __init__(self):
        self.col = (0, 0, 150)
        self.y = 180
        self.yVel = 0
        self.yMinVel, self.yMaxVel = -4, 4
        self.yJumpVel = -4
        self.jumped = False
    
    def draw(self):
        fRect(30, self.y, 10, 10, self.col)
        if self.yVel == 0:
            return
        if self.yVel < 0:
            fRect(30, self.y+10, 10, abs(int(self.yVel)), (255, 255, 255))
        elif self.yVel > 0:
            fRect(30, self.y-1, 10, -abs(int(self.yVel)), (255, 255, 255))

    def gravity(self):
        if self.grounded() and not self.jumped:
            self.yVel = 0
        elif not self.jumped and self.yVel < self.yMaxVel and not self.grounded():
            self.yVel += 0.1 + ((self.yVel**2)/20)
        elif self.jumped:
            if self.yVel < 0:
                self.yVel += 0.1 + (1/abs(self.yVel))/10
            elif self.yVel >= 0:
                self.jumped = False
        if self.yVel > self.yMaxVel:
            self.yVel == self.yMaxVel
        if not self.grounded():
            for i in range(10):
                for e in range(abs(int(self.yVel))):
                    if gCol(30+i, self.y+11+e) == (0, 0, 0):
                        self.yVel = e
                        return

    def jump(self):
        if self.grounded():
            self.jumped = True
            self.yVel = self.yJumpVel

    def grounded(self):
        for i in range(10):
            if gCol(30+i, self.y+11,) == (0, 0, 0):
                return True
        return False

    def collider(self):
        for i in range(11):
            if gCol(30+i, self.y-1) == (240, 0, 0):
                return True
        for i in range(11):
            if gCol(30+i, self.y+11) == (240, 0, 0):
                return True
        for i in range(10):
            if gCol(40, self.y+i) == (240, 0, 0) or gCol(40, self.y+i) == (0, 0, 0):
                return True
        for i in range(10):
            if gCol(29, self.y+i) == (240, 0, 0) or gCol(29, self.y+i) == (0, 0, 0):
                return True
        return False

    def update(self):
        if keydown(KEY_OK):
            self.jump()
        self.gravity()
        self.y += int(self.yVel)
        self.draw()
        self.collider()


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


class Ground:
    def __init__(self, x, xMax, y, yMax):
        self.x, self.xMax, self.y, self.yMax = x, xMax, y, yMax
        self.destroy = False
    def draw(self):
        fRect(self.x, self.y, self.xMax, self.yMax, (0, 0, 0))
    def move(self):
        self.x -= 1
        fRect(self.x + self.xMax, self.y, 1, self.yMax, (255, 255, 255))
        if self.x + self.xMax < 0:
            self.destroy = True
    def update(self):
        self.draw()
        self.move()


class Structure:
    def __init__(self, y):
        self.interval = [40, 190]
        if y > self.interval[1]:
            y = self.interval[1]
        elif y < self.interval[0]:
            y = self.interval[0]
        self.structureElement = []
        return y

    def draw(self):
        for element in self.structureElement:
            element.update()

    def destroy(self):
        for element in self.structureElement:
            if element.destroy:
                self.structureElement.remove(element)

    def update(self):
        self.draw()
        self.destroy()


class TriSpike(Structure):
    def __init__(self, y):
        self.pos = [320, super().__init__(y)]
        for i in range(3):
            self.structureElement.append(Spike(self.pos[0]+40+10*i, self.pos[1]))
        self.structureElement.append(Ground(self.pos[0], 110, self.pos[1]+10, 190-self.pos[1]))


