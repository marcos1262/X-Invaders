from abc import ABC, abstractmethod
import math

class Objeto(ABC):
    largura = 0
    altura = 0
    x = 0
    y = 0

    @abstractmethod
    def desenha(self):
        pass


    @abstractmethod
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