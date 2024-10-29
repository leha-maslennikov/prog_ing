"""Модуль с общими генераторами"""

from typing import Iterable
from models import SIZE, POINT, PointGenerator


class Axis(PointGenerator):
    """Генератор оси аксис
    
    @code
    gen = Axis()
    for point in gen(((0, 100), (0, 100)), 1):
        print(point)
    @endcode"""

    def __call__(self, size: SIZE, scale: float = 1) -> Iterable[tuple[float, float]]:
        super().__call__(size, scale)
        self.stack = [(self.size[0][0], 0), (self.size[0][1], 0)]
        return self

    def __next__(self) -> POINT:
        if self.stack:
            return self.stack.pop()
        raise StopIteration


class Ordinat(PointGenerator):
    """Генератор оси ординат
    
    @code
    gen = Ordinat()
    for point in gen(((0, 100), (0, 100)), 1):
        print(point)
    @endcode"""

    def __call__(self, size: SIZE, scale: float = 1) -> Iterable[tuple[float, float]]:
        super().__call__(size, scale)
        self.stack = [(0, self.size[1][0]), (0, self.size[1][1])]
        return self

    def __next__(self) -> POINT:
        if self.stack:
            return self.stack.pop()
        raise StopIteration
