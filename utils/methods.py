"""Модуль с математическими методами для генерации точек"""

from typing import Callable
from models import PointGenerator, POINT, SIZE


class EulerMethod(PointGenerator):
    """Метод Эйлера для построения фазового портрета
    
    @code
    def x_prime(float x, float y) -> POINT:
        return x
    def y_prime(float x, float y) -> POINT:
        return -y

    gen = EulerMethod(x_prime, y_prime, 1, 0, 0.01, 1000)
    for point in gen(((0, 100), (0, 100)), 1):
        print(point)
    @endcode"""

    def __init__(
        self,
        x_prime: Callable[[float, float], tuple[float, float]],
        y_prime: Callable[[float, float], tuple[float, float]],
        x: float,
        y: float,
        h: float,
        cnt: int,
    ):
        """@param [in] x_prime производная по x
        @param [in] y_prime производная по y
        @param [in] x начальный x
        @param [in] y начальный y
        @param [in] h шаг метода
        @param [in] cnt кол-во шагов"""
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
    """Метод Рунге-Кутта для построения фазового портрета
    
    @code
    def x_prime(float x, float y) -> POINT:
        return x
    def y_prime(float x, float y) -> POINT:
        return -y

    gen = RungeKuttMethod(x_prime, y_prime, 1, 0, 0.1, 1000)
    for point in gen(((0, 100), (0, 100)), 1):
        print(point)
    @endcode"""

    def __init__(
        self,
        x_prime: Callable[[float, float], tuple[float, float]],
        y_prime: Callable[[float, float], tuple[float, float]],
        x: float,
        y: float,
        h: float,
        cnt: int,
    ):
        """@param [in] x_prime производная по x
        @param [in] y_prime производная по y
        @param [in] x начальный x
        @param [in] y начальный y
        @param [in] h шаг метода
        @param [in] cnt кол-во шагов"""
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
