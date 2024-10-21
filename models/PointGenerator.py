from typing import Callable, Iterable

SIZE = tuple[tuple[float, float], tuple[float, float]]
POINT = tuple[float, float]


class PointGenerator(Iterable[POINT]):
    size: SIZE
    scale: float

    def __call__(self, size: SIZE, scale: float = 1) -> Iterable[POINT]:
        self.size = size
        self.scale = scale
        return self.__iter__()

    def __iter__(self) -> Iterable[POINT]:
        return self

    def __next__(self) -> POINT:
        raise StopIteration
