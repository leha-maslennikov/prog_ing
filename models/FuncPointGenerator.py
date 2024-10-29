from typing import Callable, Iterable
from models import PointGenerator, POINT, SIZE


class FuncPointGenerator(PointGenerator):
    """Генератор на основе функции
    @code
    def func(x: float) -> POINT:
        return x*x

    gen = FuncPointGenerator(func)

    for point in gen(((0, 100), (0, 100)), 1):
        print(point)

    @endcode"""

    func: Callable[[float], POINT]
    x: int

    def __init__(self, func: Callable[[float], POINT] = lambda x: x) -> None:
        """@param [in] func вещественная функция вещественного аргумента"""
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
