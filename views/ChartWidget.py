from PySide6 import QtCore, QtWidgets, QtGui
from models import PointGenerator


class ChartWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.center_ratio = (0.3, 0.8)
        self.shift = QtCore.QPointF(0, 0)
        self.scale = 10
        self.draw_callback: list[PointGenerator] = []

    def resizeEvent(self, e):
        self.shift = QtCore.QPointF(
            self.size().width() * self.center_ratio[0],
            self.size().height() * self.center_ratio[1],
        )

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter()
        painter.begin(self)
        for callback in self.draw_callback:
            callback(self, painter)
        painter.end()

    def point_generator_wrapper(self, gen: PointGenerator) -> None:
        def draw_chart(window: ChartWidget, painter: QtGui.QPainter) -> None:
            path = QtGui.QPainterPath()
            size = window.size()
            points = gen(
                (
                    (-window.shift.x(), size.width() - window.shift.x()),
                    (window.shift.y() - size.height(), window.shift.y()),
                ),
                window.scale,
            )
            try:
                x, y = next(points)
            except Exception as e:
                print("no x0, y0 from\n", gen)
                return
            point = QtCore.QPointF(x, -y) + window.shift
            for x, y in points:
                path.moveTo(point)
                point = QtCore.QPointF(x, -y) + window.shift
                path.lineTo(point)
            painter.drawPath(path)

        self.draw_callback.append(draw_chart)
