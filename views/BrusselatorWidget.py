from typing import Callable
from PySide6 import QtCore, QtGui, QtWidgets
from utils import EulerMethod, RungeKuttMethod, Cycle
from views import ChartWidget
from models import PointGenerator, SimpleCachedPointGenerator, Brusselator


class BrusselatorInfoWidget(QtWidgets.QWidget):
    point_generator: PointGenerator
    color: str

    def __init__(
        self,
        a: float = 1.0,
        b: float = 1.0,
        h: float = 0.1,
        cnt: int = 1000,
        x: float = 2,
        y: float = 2,
        is_euler: bool = False,
    ) -> None:
        super().__init__()

        self.edit_a = QtWidgets.QLineEdit(str(a))
        self.edit_b = QtWidgets.QLineEdit(str(b))
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(QtWidgets.QLabel("a = "))
        hbox1.addWidget(self.edit_a)
        hbox1.addWidget(QtWidgets.QLabel("b = "))
        hbox1.addWidget(self.edit_b)

        self.edit_h = QtWidgets.QLineEdit(str(h))
        self.edit_cnt = QtWidgets.QLineEdit(str(cnt))
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(QtWidgets.QLabel("h = "))
        hbox2.addWidget(self.edit_h)
        hbox2.addWidget(QtWidgets.QLabel("cnt = "))
        hbox2.addWidget(self.edit_cnt)

        self.edit_x = QtWidgets.QLineEdit(str(x))
        self.edit_y = QtWidgets.QLineEdit(str(y))
        hbox3 = QtWidgets.QHBoxLayout()
        hbox3.addWidget(QtWidgets.QLabel("x = "))
        hbox3.addWidget(self.edit_x)
        hbox3.addWidget(QtWidgets.QLabel("y = "))
        hbox3.addWidget(self.edit_y)

        self.euler = QtWidgets.QRadioButton("Euler method")
        hbox4 = QtWidgets.QHBoxLayout()
        hbox4.addWidget(self.euler)
        hbox4.addWidget(QtWidgets.QRadioButton("Runge-Kutt method"))

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        self.edit_color = QtWidgets.QLineEdit("#000000")
        vbox.addWidget(self.edit_color)
        btn = QtWidgets.QPushButton("Ok")
        btn.pressed.connect(self.parameters_changed)
        vbox.addWidget(btn)

        self.setLayout(vbox)

    def parameters_changed(self):
        self.color = self.edit_color.text()
        if self.euler.isChecked():
            self.point_generator = Brusselator(
                float(self.edit_a.text()),
                float(self.edit_b.text()),
                float(self.edit_h.text()),
                int(self.edit_cnt.text()),
                float(self.edit_x.text()),
                float(self.edit_y.text()),
                True,
            )
        else:
            self.point_generator = Brusselator(
                float(self.edit_a.text()),
                float(self.edit_b.text()),
                float(self.edit_h.text()),
                int(self.edit_cnt.text()),
                float(self.edit_x.text()),
                float(self.edit_y.text()),
                False,
            )

        brusselator_widget = self.parent()
        if isinstance(brusselator_widget, BrusselatorWidget):
            brusselator_widget.repaint_charts()


class BrusselatorWidget(QtWidgets.QWidget):
    charts: list[BrusselatorInfoWidget] = []
    chart_widget: ChartWidget

    def __init__(self, chart_widget: ChartWidget) -> None:
        super().__init__()

        self.chart_widget = chart_widget

        self.btn = QtWidgets.QPushButton("+")
        self.btn.pressed.connect(self.add_brusselator)
        self.vbox = QtWidgets.QVBoxLayout()
        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(self.vbox)
        vbox.addWidget(self.btn)
        self.setLayout(vbox)

    def add_brusselator(self):
        b = BrusselatorInfoWidget()
        self.charts.append(b)
        self.vbox.addWidget(b)

    def repaint_charts(self):
        self.chart_widget.draw_callback.clear()
        for model in self.charts:
            self.chart_widget.point_generator_wrapper(
                model.point_generator, QtGui.QColor(model.color)
            )
        self.chart_widget.repaint()


class BrusselatorFabricWidget(ChartWidget):
    def __init__(
        self,
        a: float = 1.0,
        b: float = 1.0,
        h: float = 0.1,
        cnt: int = 1000,
        is_euler: bool = False,
        eps: float = None,
    ):
        super().__init__()
        self.a = a
        self.b = b

        def add_brusselator(x: float, y: float) -> PointGenerator:
            return Brusselator(self.a, self.b, h, cnt, x, y, is_euler=is_euler, eps=eps)

        self.add_brusselator = add_brusselator

        '''from PySide6.QtGui import QColor, QPen, Qt
        self.point_generator_wrapper(
            Brusselator(self.a, self.b, h, cnt, 1, 1, is_euler=is_euler, eps=10 ** (-5)),
            QPen(QColor('#FF0000'), 3, Qt.PenStyle.SolidLine)
        )'''

    def mouseDoubleClickEvent(self, e: QtGui.QMouseEvent):
        p = (self.shift - e.position()) / self.scale
        '''self.point_generator_wrapper(self.add_brusselator(-p.x(), p.y()))
        self.draw_callback[-1], self.draw_callback[-2] = self.draw_callback[-2], self.draw_callback[-1]
        self.repaint()'''
        if self.a > 0:
            print('===',self.a)
            self.point_generator_wrapper(self.add_brusselator(-p.x(), p.y()))
            self.repaint()
            self.a -= 0.05
