import math
import tkinter as tk
import time
import random

#G = 6.674184 * 10**(-11) #m³/(kg * s^2)
G = 5 * 10**3
step = 0.1

class Object:
    def __init__(self, x, y, m):
        self.m = m
        self.angle = 0 #rad
        self.F = [0, 0] #N
        self.a = [0, 0] #m/s^2
        self.v = [0, 0] #m/s
        self.s = [x, y] #m

    def getF(self, m, x, y):
        d = math.sqrt((self.s[0] - x)**2 + (self.s[1] - y)**2)
        if d > 100:
            dx = x - self.s[0]
            dy = y - self.s[1]
            angle = math.atan2(dx, dy)

            F = G * self.m * m / d**2 #N
            Fx = F * math.sin(angle) #N
            Fy = F * math.cos(angle) #N

            self.F[0] += Fx
            self.F[1] += Fy

            #print('F: ', F, ' N | angle: ', angle)

    def calcMove(self):
        self.a[0] = self.F[0] / self.m
        self.a[1] = self.F[1] / self.m

        self.v[0] = self.v[0] + self.a[0] * step
        self.v[1] = self.v[1] + self.a[1] * step
        
        self.s[0] = self.s[0] + self.v[0] * step
        self.s[1] = self.s[1] + self.v[1] * step
   
class GUI:
    def __init__(self):
        self.run = True
        width = 1000
        height = 1000
        self. objects = []
        self.root = tk.Tk()
        self.root.title('Gravity')
        self.root.resizable(tk.FALSE,tk.FALSE)

        self.canvas = tk.Canvas(self.root, bg='white', width = width, height = height, relief=tk.RIDGE)
        self.canvas.pack()

        self.center = Object(width/2, height/2, 1000)

        self.root.bind('<Button 1>', self.click1)

        self.root.protocol("WM_DELETE_WINDOW", self.quit)

    def quit(self):
        self.run = False

    def click1(self, e):
        mass = random.randint(1,100)
        self.objects.append(Object(e.x, e.y, mass))

    def draw(self, step):
        self.canvas.delete(tk.ALL)
        self.canvas.create_oval(self.center.s[0] - 5, self.center.s[1] - 5, self.center.s[0] + 5, self.center.s[1] + 5, fill='black')
        for i in range(len(self.objects)):
            self.objects[i].F = [0, 0]
            self.objects[i].getF(self.center.m, self.center.s[0], self.center.s[1])
            for j in range(i, len(self.objects)):
                if j != i:
                    self.objects[i].getF(self.objects[j].m, self.objects[j].s[0], self.objects[j].s[1])
            self.objects[i].calcMove()
            self.canvas.create_oval(self.objects[i].s[0] - 5, self.objects[i].s[1] - 5, self.objects[i].s[0] + 5, self.objects[i].s[1] + 5, fill='red')
            

gui = GUI()
while gui.run:
    gui.draw(step)
    gui.root.update()
    time.sleep(step)
