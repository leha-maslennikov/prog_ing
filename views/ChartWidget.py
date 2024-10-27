from PySide6 import QtCore, QtWidgets, QtGui
from models import PointGenerator
from time import time


class ChartWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.scale = 40
        self.draw_callback: list[PointGenerator] = []
        self.dy = 0
        self.last_repaint = time()

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        self.mouse_last_pos = e.globalPosition()

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):
        if e.buttons() == QtCore.Qt.MouseButton.LeftButton:
            if time() - self.last_repaint > 0.1:
                self.last_repaint = time()
                self.shift += e.globalPosition() - self.mouse_last_pos
                self.mouse_last_pos = e.globalPosition()
                self.repaint()

    def wheelEvent(self, e: QtGui.QWheelEvent):
        self.dy += e.angleDelta().y()
        if time() - self.last_repaint > 0.1:
            self.last_repaint = time()
            self.scale += self.dy // 10
            self.dy = 0
            self.scale = max(self.scale, 10)
            self.repaint()

    def resizeEvent(self, e):
        self.shift = QtCore.QPointF(
            self.size().width() * 0.5,
            self.size().height() * 0.5,
        )

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.draw_axis(painter)
        for callback in self.draw_callback:
            callback(self, painter)
        painter.end()

    def get_min_max_points(self) -> tuple[QtCore.QPointF, QtCore.QPointF]:
        size = self.size()
        shift = self.shift
        return (
            QtCore.QPointF(-shift.x(), shift.y() - size.height()),
            QtCore.QPointF(size.width() - shift.x(), shift.y()),
        )

    def draw_axis(self, painter: QtGui.QPainter):
        min_max = self.get_min_max_points()
        draw_x = lambda x: painter.drawLine(
            QtCore.QPointF(x, -min_max[0].y()) + self.shift,
            QtCore.QPointF(x, -min_max[1].y()) + self.shift,
        )
        draw_y = lambda y: painter.drawLine(
            QtCore.QPointF(min_max[0].x(), -y) + self.shift,
            QtCore.QPointF(min_max[1].x(), -y) + self.shift,
        )
        pen = painter.pen()
        painter.setPen(QtGui.QColor(0, 0, 0, 50))
        scale = int(self.scale)
        for x in range(0, int(min_max[1].x()) + 1, scale):
            draw_x(x)
        for x in range(0, int(min_max[0].x()) - 1, -scale):
            draw_x(x)
        for y in range(0, int(min_max[1].y()) + 1, scale):
            draw_y(y)
        for y in range(0, int(min_max[0].y()) - 1, -scale):
            draw_y(y)
        painter.setPen(QtGui.QColor(100, 0, 0, 100))
        draw_x(0)
        draw_y(0)
        painter.setPen(pen)

    def point_generator_wrapper(
        self, gen: PointGenerator, pen: QtGui.QColor = None
    ) -> None:
        def draw_chart(window: ChartWidget, painter: QtGui.QPainter) -> None:
            if pen:
                tmp_pen = painter.pen()
                painter.setPen(pen)
            path = QtGui.QPainterPath()
            min_max = window.get_min_max_points()
            points = gen(
                ((min_max[0].x(), min_max[1].x()), (min_max[0].y(), min_max[1].y())),
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
            if pen:
                painter.setPen(tmp_pen)

        self.draw_callback.append(draw_chart)
