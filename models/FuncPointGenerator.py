from typing import Callable, Iterable
from models import *


class FuncPointGenerator(PointGenerator):

    def __init__(self, func: Callable[[float], POINT] = lambda x: x) -> None:
        self.func = func

    def __call__(self, size: SIZE, scale: float = 1) -> Iterable[POINT]:
        super().__call__(size, scale)
        self.x = int(self.size[0][0])
        return self

    def __next__(self) -> POINT:
        if self.x < int(self.size[0][1]) + 1:
            x = self.x
            self.x += 1
            return (x, self.scale * self.func(x / self.scale))
        raise StopIteration
