from typing import Callable, Iterable


def euler_method(
    func: Callable[[float, float], tuple[float, float]], x: float, y: float
) -> Iterable[tuple[float, float]]:
    while True:
        yield (x, y)
        x, y = func(x, y)