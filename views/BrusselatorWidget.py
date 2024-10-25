from typing import Callable
from PySide6 import QtCore, QtGui, QtWidgets
from utils import EulerMethod, RungeKuttMethod
from views import ChartWidget
from models import PointGenerator, SimpleCachedPointGenerator


class BrusselatorInfoWidget(QtWidgets.QWidget):
    a: float = 1.0
    b: float = 1.0
    point_generator: PointGenerator
    color: str

    def __init__(self) -> None:
        super().__init__()

        self.edit_a = QtWidgets.QLineEdit("1")
        self.edit_b = QtWidgets.QLineEdit("1")
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(QtWidgets.QLabel("a = "))
        hbox1.addWidget(self.edit_a)
        hbox1.addWidget(QtWidgets.QLabel("b = "))
        hbox1.addWidget(self.edit_b)

        self.edit_h = QtWidgets.QLineEdit("0.1")
        self.edit_cnt = QtWidgets.QLineEdit("1000")
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(QtWidgets.QLabel("h = "))
        hbox2.addWidget(self.edit_h)
        hbox2.addWidget(QtWidgets.QLabel("cnt = "))
        hbox2.addWidget(self.edit_cnt)

        self.edit_x = QtWidgets.QLineEdit("2")
        self.edit_y = QtWidgets.QLineEdit("2")
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
        self.a = float(self.edit_a.text())
        self.b = float(self.edit_b.text())
        self.color = self.edit_color.text()
        if self.euler.isChecked():
            self.point_generator = SimpleCachedPointGenerator(
                EulerMethod(
                    self.x_prime,
                    self.y_prime,
                    float(self.edit_x.text()),
                    float(self.edit_y.text()),
                    float(self.edit_h.text()),
                    int(self.edit_cnt.text()),
                )
            )
        else:
            self.point_generator = SimpleCachedPointGenerator(
                RungeKuttMethod(
                    self.x_prime,
                    self.y_prime,
                    float(self.edit_x.text()),
                    float(self.edit_y.text()),
                    float(self.edit_h.text()),
                    int(self.edit_cnt.text()),
                )
            )

        brusselator_widget = self.parent()
        if isinstance(brusselator_widget, BrusselatorWidget):
            brusselator_widget.repaint_charts()

    def x_prime(self, x: float, y: float):
        return 1 - (self.b + 1) * x + self.a * x * x * y

    def y_prime(self, x: float, y: float):
        return self.b * x - self.a * x * x * y


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
