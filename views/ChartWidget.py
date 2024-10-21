from typing import Callable, Iterator
from PySide6 import QtCore, QtWidgets, QtGui


class ChartWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.center_ratio = (0.3, 0.8)
        self.scale = 10
        self.draw_callback: list[Callable[[ChartWidget, QtGui.QPainter], None]] = [
            axis
        ]

    def resizeEvent(self, e):
        self.shift = QtCore.QPoint(
            self.size().width() * self.center_ratio[0],
            -self.size().height() * self.center_ratio[1],
        )

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter()
        painter.begin(self)
        for callback in self.draw_callback:
            callback(self, painter)
            print(callback)
        painter.end()

    def setScale(self, scale: float) -> None:
        self.scale = scale


def draw_coords(window: ChartWidget, painter: QtGui.QPainter) -> None:
    path = QtGui.QPainterPath()
    path.moveTo(window.shift.x(), 0)
    path.lineTo(window.shift.x(), window.size().height())
    path.moveTo(0, window.shift.y())
    path.lineTo(window.size().width(), window.shift.y())
    painter.drawPath(path)


def draw_chart_wrapper(
    gen: Callable[[],Iterator[tuple[float, float]]]
) -> None:
    def draw_chart(window: ChartWidget, painter: QtGui.QPainter) -> None:
        path = QtGui.QPainterPath()
        points = gen()
        x0, y0 = next(points)
        for x, y in points:
            x, y = window.scale * x, window.scale * y
            path.moveTo(window.shift.x() + x0, window.shift.y() + y0)
            path.lineTo(window.shift.x() + x, window.shift.y() + y)
            x0, y0 = x, y
        painter.drawPath(path)
    return draw_chart

@draw_chart_wrapper
def axis():
    for x in range(-100, 100):
        yield (x, 0)


def _ordinat():
    for y in range(-1000, 1000):
        yield (0, y)
        
ordinat = draw_chart_wrapper(_ordinat())


def xx():
    for x in range(-100, 100):
        yield (x, x * x)

draw_xx = draw_chart_wrapper(xx())
