import math

from PyQt5.QtCore import QObject


class Objeto(QObject):

    def desenha(self):
        pass

    def move(self):
        pass

    def colidiu(self, objeto):
        d = math.sqrt((objeto.x - self.x)**2 + (objeto.y - self.y)**2)

        raio1 = min(self.largura, self.altura)/2
        raio2 = min(objeto.largura, objeto.altura)/2

        if d <= raio1 + raio2:
            return True
        else:
            return False