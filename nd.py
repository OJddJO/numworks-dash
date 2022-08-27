from kandinsky import fill_rect as fRect,draw_string as dStr,get_pixel as gCol
from ion import *
from time import sleep
from random import randint

class UI:

    def __init__(self):
        self.optionList = ["     Play     ", "     Exit     ", " [OK] to jump "]
        self.modifiedList = []
        self.select = 0
        self.draw()

    def draw(self):
        fRect(0, 0, 320, 222, (255, 255, 255))
        txt = ["Numworks Dash", "by OJd_dJO"]
        dStr(txt[0], int(160-(len(txt[0])*10/2)), 80, (50, 50, 200))
        dStr(txt[1], int(160-(len(txt[1])*10/2)), 98, (50, 50, 200))

    def update(self):
        self.modifiedList = []
        for element in self.optionList:
            if element == self.optionList[self.select]:
                self.modifiedList.append("> "+element+" <")
            else:
                self.modifiedList.append("  "+element+"  ")
        i = 0
        for element in self.modifiedList:
            yMod = 18*i
            length = len(element)*10
            if element == self.modifiedList[self.select]:
              dStr(element, 160-int(length/2), 140+yMod, (0, 0, 0), (200, 200, 200))
            else:
              dStr(element, 160-int(length/2), 140+yMod)
            i += 1
        if keydown(KEY_DOWN):
            self.select += 1
            if self.select == 3:
                self.select = 0
            while keydown(KEY_DOWN):
                pass
        elif keydown(KEY_UP):
            self.select -= 1
            if self.select == -1:
                self.select = 2
            while keydown(KEY_UP):
                pass

        if keydown(KEY_OK):
            if self.select == 0:
                fRect(0, 0, 320, 222, (255, 255, 255))
                game = Game()
                run = True
                while run:
                    run = game.run()
                    sleep(1/120)
                dStr("GG!", 148, 100)
                while keydown(KEY_OK):
                    pass
                return True
            if self.select == 1:
                fRect(0, 0, 320, 222, (255, 255, 255))
                return False
            if self.select == 2:
                pass
        return True


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
            self.yVel += 0.1 + ((self.yVel**2)/25)
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
        self.pos = [320, y]
        self.structureElement.append(Ground(self.pos[0], 110, self.pos[1]+10, 190-self.pos[1]))

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


class BruhSpike(Structure):
    def __init__(self, y):
        super().__init__(y)
        self.structureElement.append(Spike(self.pos[0]+40, self.pos[1]))
        self.structureElement.append(Ground(self.pos[0]+60, 10, self.pos[1]-40, 10))


class SpikeRoof(Structure):
    def __init__(self, y):
        super().__init__(y)
        self.structureElement.append(Spike(self.pos[0]+50, self.pos[1]))
        self.structureElement.append(Ground(self.pos[0]+35, 10, self.pos[1]-40, 10))


class TriSpike(Structure):
    def __init__(self, y):
        super().__init__(y)
        for i in range(3):
            self.structureElement.append(Spike(self.pos[0]+40+10*i, self.pos[1]))


class Game:
    def __init__(self):
        self.player = Cube()
        self.obsList = []
        self.score = 0
        self.lastY = 200
        self.tick = 60
        fRect(0, 200, 320, 222, (0, 0, 0))

    def addObs(self):
        if self.tick == 0:
            if randint(0, 1) == 0: self.lastY += 10
            else: self.lastY -= 10
            if self.lastY > 190:
                self.lastY = 190
            elif self.lastY < 40:
                self.lastY = 190
            t = randint(0, 2)
            if t == 0: self.obsList.append(TriSpike(self.lastY))
            elif t == 1: self.obsList.append(SpikeRoof(self.lastY))
            elif t == 2: self.obsList.append(BruhSpike(self.lastY))
            self.tick = 120
        else: self.tick -= 1

    def run(self):
        self.player.update()
        for element in self.obsList:
            element.update()
            if element.structureElement == []:
                self.obsList.remove(element)
                self.score += 1
        self.addObs()
        dStr("Score: "+str(self.score), 200, 10)
        if self.player.collider(): return False
        else: return True

ui = UI()
run = True
while run:
    run = ui.update()
