def axis(min_x: float, min_y: float, max_x: float, max_y: float):
    yield (min_x, 0)
    yield (max_x, 0)


def ordinat(min_x: float, min_y: float, max_x: float, max_y: float):
    yield (0, max_y)
    yield (0, min_y)


def x_times_x(min_x: float, min_y: float, max_x: float, max_y: float):
    print(min_x, max_x, max_y, min_y)
    for x in range(int(min_x), int(max_x)):
        yield (x, x * x)
