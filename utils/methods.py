from typing import Callable
from models import PointGenerator, POINT, SIZE


class EulerMethod(PointGenerator):
    def __init__(
        self,
        x_prime: Callable[[float, float], tuple[float, float]],
        y_prime: Callable[[float, float], tuple[float, float]],
        x: float,
        y: float,
        h: float,
        cnt: int,
    ):
        self.x_prime = x_prime
        self.y_prime = y_prime
        self.x = x
        self.y = y
        self.h = h
        self.cnt = cnt

    def __call__(self, size: SIZE, scale: float):
        super().__call__(scale, scale)
        self.x0 = self.x
        self.y0 = self.y
        self.n = self.cnt
        return self

    def __next__(self) -> POINT:
        if self.n == 0:
            raise StopIteration
        self.n -= 1
        x, y = self.x0, self.y0
        self.x0 = x + self.h * self.x_prime(x, y)
        self.y0 = y + self.h * self.y_prime(x, y)

        return (self.scale * x, self.scale * y)


class RungeKuttMethod(PointGenerator):
    def __init__(
        self,
        x_prime: Callable[[float, float], tuple[float, float]],
        y_prime: Callable[[float, float], tuple[float, float]],
        x: float,
        y: float,
        h: float,
        cnt: int,
    ):
        self.x_prime = x_prime
        self.y_prime = y_prime
        self.x = x
        self.y = y
        self.h = h
        self.cnt = cnt

    def __call__(self, size: SIZE, scale: float):
        super().__call__(scale, scale)
        self.x0 = self.x
        self.y0 = self.y
        self.n = self.cnt
        return self

    def __next__(self) -> POINT:
        if self.n == 0:
            raise StopIteration
        self.n -= 1
        x, y = self.x0, self.y0

        k1 = self.h * self.x_prime(x, y)
        l1 = self.h * self.y_prime(x, y)
        k2 = self.h * self.x_prime(x + k1 / 2, y + l1 / 2)
        l2 = self.h * self.y_prime(x + k1 / 2, y + l1 / 2)
        k3 = self.h * self.x_prime(x + k2 / 2, y + l2 / 2)
        l3 = self.h * self.y_prime(x + k2 / 2, y + l2 / 2)
        k4 = self.h * self.x_prime(x + k3, y + l3)
        l4 = self.h * self.y_prime(x + k3, y + l3)
        self.x0 = x + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        self.y0 = y + (l1 + 2 * l2 + 2 * l3 + l4) / 6

        return (self.scale * x, self.scale * y)
