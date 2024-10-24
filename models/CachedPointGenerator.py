from typing import Iterable
from models import PointGenerator, SIZE, POINT


class SimpleCachedPointGenerator(PointGenerator):

    point_generator: PointGenerator
    points: list[POINT]

    def __init__(self, point_generator: PointGenerator) -> None:
        self.point_generator = point_generator
        self.points = []

    def __call__(self, size: SIZE, scale: float = 1) -> Iterable[POINT]:
        self.scale = scale
        if not self.points:
            self.points = [point for point in self.point_generator(size, 1)]
        self.n = 0

        return self.__iter__()

    def __iter__(self) -> Iterable[POINT]:
        return self

    def __next__(self) -> POINT:
        if self.n == len(self.points):
            raise StopIteration
        self.n += 1
        return (
            self.scale * self.points[self.n - 1][0],
            self.scale * self.points[self.n - 1][1],
        )
