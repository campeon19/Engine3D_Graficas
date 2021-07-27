# Christian Daniel Perez De Leon 19710

import struct
from collections import namedtuple
from obj import Obj

V2 = namedtuple('Point2', ['x', 'y'])


def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h', w)

def dword(d):
    return struct.pack('=l', d)

def color(r, g, b):
    return bytes([ int(b * 255), int(g* 255), int(r* 255)])


BLACK = color(0,0,0)
WHITE = color(1,1,1)


class Renderer(object):
    def __init__(self, width, height):
        self.curr_color = WHITE
        self.clear_color = BLACK
        self.glCreateWindow(width, height)

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()
        self.glViewport(0,0, width, height)

    def glViewport(self, x, y, width, height):
        self.vpX = x
        self.vpY = y
        self.vpWidth = width
        self.vpHeight = height



    def glClearColor(self, r, g, b):
        self.clear_color = color(r, g, b)

    def glClear(self):
        self.pixels = [[ self.clear_color for y in range(self.height)] for x in range(self.width)]

    def glColor(self, r, g, b):
        self.curr_color = color(r,g,b)


    def glPoint(self, x, y, color = None):
        if x < self.vpX or x >= self.vpX + self.vpWidth or y < self.vpY or y >= self.vpY + self.vpHeight:
            return

        if (0 < x < self.width) and (0 < y < self.height):
            self.pixels[int(x)][int(y)] = color or self.curr_color
    
    def glVertex(self, x, y, color = None):
        if x < -1 or x > 1:
            return
        if y < -1 or y > 1:
            return
        
        pixelX = (x+1) * (self.vpWidth / 2) + self.vpX
        pixelY = (y+1) * (self.vpHeight / 2) + self.vpY

        if (0 < x < self.width) and (0 < y < self.height):
            self.pixels[int(x)][int(y)] = color or self.curr_color


    def glLine(self, v0, v1, color = None):
        x0 = v0.x
        x1 = v1.x
        y0 = v0.y
        y1 = v1.y

        if x0 == x1 and y0 == y1:
            self.glPoint(x0,y1, color)
            return

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5
        m = dy/dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x, color)
            else:
                self.glPoint(x, y, color)

            offset += m
            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 1

    def glLoadModel(self, filename, transalate = V2(0.0,0.0), scale = V2(1,1)):

        model = Obj(filename)

        for cara in model.caras:
            vertCount = len(cara)

            for v in range(vertCount):
                index0 = cara[v][0] - 1
                index1 = cara[(v+1) % vertCount][0] - 1

                vert0 = model.vertices[index0]
                vert1 = model.vertices[index1]

                x0 = round(vert0[0] * scale.x + transalate.x)
                x1 = round(vert1[0] * scale.x + transalate.x)
                y0 = round(vert0[1] * scale.y + transalate.y)
                y1 = round(vert1[1] * scale.y + transalate.y)

                self.glLine(V2(x0,y0), V2(x1, y1))

                #self.glPoint(vert[0] * scale.x + transalate.x, vert[1] * scale.y + transalate.y)

    def glFillTriangleInv(self, v1,v2,v3):
        invslope1 = (v3.x - v1.x) / (v3.y - v1.y)
        invslope2 = (v3.x - v2.x) / (v3.y - v2.y)
        curx1 = v3.x
        curx2 = v3.x 
        print(v1.y)
        print(v3.y)
        print(invslope2)
        

        for i in range(v3.y, v1.y, 1):
            
            
            
            self.glLine(V2(int(curx1), i), V2(int(curx2), i))
            curx1 = curx1 - invslope1
            curx2 = curx2 - invslope2
            


    def glFinish(self, filename):
        with open(filename, "wb") as file:
            # Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color Table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])

