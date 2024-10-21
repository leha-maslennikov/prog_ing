from typing import Callable, Iterator
from PySide6 import QtCore, QtWidgets, QtGui


class ChartWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.center_ratio = (0.3, 0.8)
        self.shift = QtCore.QPoint(0, 0)
        self.scale = 10
        self.draw_callback: list[Callable[[ChartWidget, QtGui.QPainter], None]] = []

    def resizeEvent(self, e):
        self.shift = QtCore.QPoint(
            self.size().width() * self.center_ratio[0],
            self.size().height() * self.center_ratio[1],
        )

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter()
        painter.begin(self)
        for callback in self.draw_callback:
            callback(self, painter)
        painter.end()

    def setScale(self, scale: float) -> None:
        self.scale = scale

    def draw_chart_wrapper(
        self, gen: Callable[[float, float, float, float], Iterator[tuple[float, float]]]
    ) -> None:
        def draw_chart(window: ChartWidget, painter: QtGui.QPainter) -> None:
            path = QtGui.QPainterPath()
            size = self.size()
            points = gen(
                -self.shift.x(),
                self.shift.y(),
                size.width() - self.shift.x(),
                self.shift.y() - size.height(),
            )
            x0, y0 = next(points)
            for x, y in points:
                x, y = window.scale * x, window.scale * y
                path.moveTo(window.shift.x() + x0, window.shift.y() - y0)
                path.lineTo(window.shift.x() + x, window.shift.y() - y)
                x0, y0 = x, y
            painter.drawPath(path)

        self.draw_callback.append(draw_chart)