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
        points = []
        x0 = v0.x
        x1 = v1.x
        y0 = v0.y
        y1 = v1.y

        if x0 == x1 and y0 == y1:
            self.glPoint(x0,y1, color)
            return points

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

    def glFillTriangle(self, A, B, C, color = None):

        if A.y < B.y:
            A, B = B, A
        if A.y < C.y:
            A, C = C, A
        if B.y < C.y:
            B, C = C, B

        def flatBottomTriangle(v1, v2, v3):
            try:
                d_21 = (v2.x - v1.x) / (v2.y - v1.y)
                d_31 = (v3.x - v1.x) / (v3.y - v1.y)
            except:
                pass
            else:
                x1 = v2.x
                x2 = v3.x
                for y in range(v2.y, v1.y + 1):
                    self.glLine(V2(int(x1),y), V2(int(x2),y), color)
                    x1 += d_21
                    x2 += d_31

        def flatTopTriangle(v1, v2, v3):
            try:
                d_31 = (v3.x - v1.x) / (v3.y - v1.y)
                d_32 = (v3.x - v2.x) / (v3.y - v2.y)
            except:
                pass
            else:
                x1 = v3.x
                x2 = v3.x

                for y in range(v3.y, v1.y + 1):
                    self.glLine(V2(int(x1),y), V2(int(x2),y), color)
                    x1 += d_31
                    x2 += d_32

        if B.y == C.y:
            flatBottomTriangle(A, B, C)
        elif A.y == B.y:
            flatTopTriangle(A, B, C)
        else:
            D = V2(A.x + ((B.y - A.y) / (C.y - A.y)) * (C.x - A.x)   , B.y)
            flatBottomTriangle(A, B, D)
            flatTopTriangle(B, D, C)
            
    def glDrawPolygon(self, polygon):
        for i in range(len(polygon)):
            self.glLine(V2(polygon[i][0], polygon[i][1]), V2(polygon[(i+1) % len(polygon)][0], polygon[(i+1) % len(polygon)][1]))

    def glScanLine(self):
        # Basandose en el algoritmo Scan Line, se implemento el siguiente codigo
        for y in range (self.height):
            puntos = []
            puntosfiltrados = []
            for x in range (self.width):
                if self.pixels[x][y] == self.curr_color:
                    puntos.append((x,y))
            for l in range (0, len(puntos)):
                if (puntos[(l+1) % len(puntos)][0] - puntos[l][0]) != 1:
                    puntosfiltrados.append((puntos[l]))


            if len(puntosfiltrados) == 0:
                pass
            elif len(puntosfiltrados) % 2 == 0:
                for x in range(0, len(puntosfiltrados), 2):
                    self.glLine(V2(puntosfiltrados[x][0], puntosfiltrados[x][1]),V2(puntosfiltrados[(x+1) % len(puntosfiltrados)][0], puntosfiltrados[(x+1) % len(puntosfiltrados)][1]))
            elif len(puntosfiltrados) % 3 == 0:
                for x in range(0, len(puntosfiltrados), 1):
                    self.glLine(V2(puntosfiltrados[x][0], puntosfiltrados[x][1]),V2(puntosfiltrados[(x+1) % len(puntosfiltrados)][0], puntosfiltrados[(x+1) % len(puntosfiltrados)][1]))
            #print(puntos)

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

