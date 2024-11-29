from typing import Callable, Iterable
from models import PointGenerator, POINT, SIZE, SimpleCachedPointGenerator


class ModelingPointGenerator(PointGenerator):
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


class EulerMethod(ModelingPointGenerator):

    def __next__(self) -> POINT:
        if self.n == 0:
            raise StopIteration
        self.n -= 1
        x, y = self.x0, self.y0
        self.x0 = x + self.h * self.x_prime(x, y)
        self.y0 = y + self.h * self.y_prime(x, y)

        return (self.scale * x, self.scale * y)


class RungeKuttMethod(ModelingPointGenerator):

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


class Cycle(SimpleCachedPointGenerator):

    def __init__(self, gen: ModelingPointGenerator, eps: float, y0: float) -> None:
        self.gen = gen
        gen.cnt = 10**10
        gen = gen(None, 1)
        last = next(gen)
        last_x = None
        for point in gen:
            if (point[1] - y0) > 0 and (last[1] - y0) < 0:
                y1, y2 = last[1], point[1]
                x1, x2 = last[0], point[0]
                x = (y0 - y1) * (x2 - x1) / (y2 - y1) + x1
                if last_x and (abs(last_x - x) < eps):
                    last_x = x
                    break
                last_x = x
            last = point
        self.gen.x = last_x
        self.gen.y = y0
        self.points = []
        gen = self.gen(None, 1)
        last = next(gen)
        for point in gen:
            self.points.append(point)
            if (point[1] - y0) > 0 and (last[1] - y0) < 0:
                break
            last = point
        print((gen.cnt - gen.n)*gen.h)