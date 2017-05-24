from abc import ABC, abstractmethod


class Trajetoria(ABC):
    """
    Representa uma trajetória baseada em uma função
    """

    @abstractmethod
    def proximo(self, incremento) -> (float, float):
        pass

    @abstractmethod
    def anterior(self, decremento) -> (float, float):
        pass

    @abstractmethod
    def gera(self) -> (float, float):
        pass


class TrajetoriaLinear(Trajetoria):
    """
    Representa uma trajetória definida por uma reta
    """

    def __init__(self, a, x_inicial, b, vertical=False):
        self.a = a
        self.b = b
        self.vertical = vertical
        self.x = x_inicial

    def proximo(self, incremento):
        self.x += incremento
        return self.gera()

    def anterior(self, decremento):
        self.x -= decremento
        return self.gera()

    def gera(self):
        y = self.a * self.x + self.b
        if self.vertical:
            return y, self.x
        return self.x, y
