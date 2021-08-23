# Christian Daniel Perez De Leon  19710
import struct

def _color(r, g, b):
    return bytes([ int(b * 255), int(g* 255), int(r* 255)])

class Obj(object):
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.lines = file.read().splitlines()
        
        self.vertices = []
        self.texturacoordenadas = []
        self.normales = []
        self.caras = []
        self.read()
    
    def read(self):
        for line in self.lines:
            if line:
                prefix, value = line.split(' ', 1)

                if prefix == 'v':
                    self.vertices.append(list(map(float, value.split(' '))))
                elif prefix == 'vt':
                    self.texturacoordenadas.append(list(map(float, value.split(' '))))
                elif prefix == 'vn':
                    self.normales.append(list(map(float, value.split(' '))))
                elif prefix == 'f':
                    self.caras.append( [ list(map(int, vert.split('/'))) for vert in value.split(' ')] )

class Texture(object):
    def __init__(self, filename):
        self.filename = filename
        self.read()


    def read(self):
        with open(self.filename, "rb") as image:
            image.seek(10)
            headerSize = struct.unpack('=l', image.read(4))[0]

            image.seek(14 + 4)
            self.width = struct.unpack('=l', image.read(4))[0]
            self.height = struct.unpack('=l', image.read(4))[0]

            image.seek(headerSize)

            self.pixels = []

            for y in range(self.height):
                self.pixels.append([])
                for x in range(self.width):
                    b = ord(image.read(1)) / 255
                    g = ord(image.read(1)) / 255
                    r = ord(image.read(1)) / 255

                    self.pixels[y].append( _color(r,g,b) )
    
    
    def getColor(self, tx, ty):
        if 0<=tx<1 and 0<=ty<1:
            x = int(tx * self.width)
            y = int(ty * self.height)
            return self.pixels[y][x]
        else:
            return _color(0,0,0)