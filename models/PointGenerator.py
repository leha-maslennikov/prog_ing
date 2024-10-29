from typing import Callable, Iterable

## Размер окна ((min_x, max_x), (min_y, max_y))
SIZE = tuple[tuple[float, float], tuple[float, float]]

## Точка на плоскости (x, y)
POINT = tuple[float, float]


class PointGenerator(Iterable[POINT]):
    """Базовый класс генерирующий POINT"""

    ## @private
    size: SIZE
    ## @private
    scale: float

    def __call__(self, size: SIZE, scale: float = 1) -> Iterable[POINT]:
        """@param [in] size размер окна ((min_x, max_x), (min_y, max_y)), в котором будет происходить отрисовка
        @param [in] scale кол-во пикселей, являющихся еденицей деления

        @return итерируемый объект, возвращающий POINT"""
        self.size = size
        self.scale = scale
        return self.__iter__()

    def __iter__(self) -> Iterable[POINT]:
        return self

    def __next__(self) -> POINT:
        raise StopIteration
