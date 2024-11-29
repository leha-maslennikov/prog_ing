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
                self.shift += e.globalPosition() - self.mouse_last_pos
                self.mouse_last_pos = e.globalPosition()
                self.repaint()
                self.last_repaint = time()

    def wheelEvent(self, e: QtGui.QWheelEvent):
        self.dy += e.angleDelta().y()
        if time() - self.last_repaint > 0.1:
            self.scale += self.dy // 10
            self.dy = 0
            self.scale = max(self.scale, 10)
            self.repaint()
            self.last_repaint = time()

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

        scale = int(self.scale)
        delimiter = 60
        delimiter_weight = delimiter / scale

        pen = painter.pen()
        painter.setPen(QtGui.QColor(0, 0, 0, 50))
        font = painter.font()

        font.setPointSize(14)
        painter.setFont(font)

        x0 = self.shift.x()
        y0 = self.shift.y()
        min_x = int(min_max[0].x() / delimiter) * delimiter
        max_x = int(min_max[1].x() / delimiter) * delimiter
        for x in range(min_x, max_x + 1, delimiter):
            p1 = QtCore.QPointF(x0 + x, 0)
            p2 = QtCore.QPointF(x0 + x, self.size().height())
            painter.drawLine(p1, p2)
            painter.drawText(
                x0 + x,
                min(self.size().height() - 15, abs(max(15, y0))),
                str(x // delimiter * delimiter_weight)[0:4],
            )
        min_y = int(min_max[0].y() / delimiter) * delimiter
        max_y = int(min_max[1].y() / delimiter) * delimiter
        for y in range(min_y, max_y + 1, delimiter):
            p1 = QtCore.QPointF(0, y0 - y)
            p2 = QtCore.QPointF(self.size().width(), y0 - y)
            painter.drawLine(p1, p2)
            painter.drawText(
                min(self.size().width() - 40, max(0, x0)),
                y0 - y,
                str(y // delimiter * delimiter_weight)[0:4],
            )

        painter.setPen(
            QtGui.QPen(QtGui.Qt.GlobalColor.black, 1, QtGui.Qt.PenStyle.SolidLine)
        )
        p1 = QtCore.QPointF(x0, 0)
        p2 = QtCore.QPointF(x0, self.size().height())
        painter.drawLine(p1, p2)
        p1 = QtCore.QPointF(0, y0)
        p2 = QtCore.QPointF(self.size().width(), y0)
        painter.drawLine(p1, p2)
        painter.setPen(
            QtGui.QPen(QtGui.Qt.GlobalColor.black, 2.0, QtGui.Qt.PenStyle.SolidLine)
        )
        painter.drawText(self.size().width() - 10, min(self.size().height() - 12, y0 - 2), "x")
        painter.drawText(max(0, x0+2), 12, "y")

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
