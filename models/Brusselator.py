from models import PointGenerator, CachedPointGenerator, SimpleCachedPointGenerator
from utils import EulerMethod, RungeKuttMethod


def Brusselator(
    a: float, b: float, h: float, cnt: int, x: float, y: float, is_euler: bool = False
) -> PointGenerator:
    def x_prime(x: float, y: float):
        return 1 - (b + 1) * x + a * x * x * y

    def y_prime(x: float, y: float):
        return b * x - a * x * x * y

    if is_euler:
        return SimpleCachedPointGenerator(EulerMethod(x_prime, y_prime, x, y, h, cnt))
    else:
        return SimpleCachedPointGenerator(RungeKuttMethod(x_prime, y_prime, x, y, h, cnt))
