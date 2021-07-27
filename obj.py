# Christian Daniel Perez De Leon  19710

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