import sys
from PySide6 import QtWidgets
from views.BrusselatorWidget import BrusselatorWidget, BrusselatorFabricWidget
from views import ChartWidget
from utils import *
from models import Brusselator


def example() -> list[ChartWidget]:
    chart_widget1 = ChartWidget()
    chart_widget1.setWindowTitle("Метод Эйлера: h = 0.1")
    chart_widget1.point_generator_wrapper(
        EulerMethod(
            x_prime=lambda x, y: y, y_prime=lambda x, y: -x, x=1, y=0, h=0.1, cnt=100
        )
    )
    chart_widget2 = ChartWidget()
    chart_widget2.setWindowTitle("Метод Эйлера: h = 0.01")
    chart_widget2.point_generator_wrapper(
        EulerMethod(
            x_prime=lambda x, y: y, y_prime=lambda x, y: -x, x=1, y=0, h=0.01, cnt=800
        )
    )
    chart_widget3 = ChartWidget()
    chart_widget3.setWindowTitle("Метод Рунге-Кутта: h = 0.1")
    chart_widget3.point_generator_wrapper(
        RungeKuttMethod(
            x_prime=lambda x, y: y, y_prime=lambda x, y: -x, x=1, y=0, h=0.1, cnt=1000
        )
    )
    chart_widget4 = ChartWidget()
    chart_widget4.setWindowTitle("Метод Рунге-Кутта: h = 0.01")
    chart_widget4.point_generator_wrapper(
        RungeKuttMethod(
            x_prime=lambda x, y: y, y_prime=lambda x, y: -x, x=1, y=0, h=0.01, cnt=1000
        )
    )
    return [chart_widget1, chart_widget2, chart_widget3, chart_widget4]


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    chart_widget = ChartWidget()
    b = 2
    h = 0.01
    cnt = 5000
    a = 8
    a = 2
    a = 1.5
    a = 1
    eps = 10 ** (-5)
    a = 0.9
    a = 0.2
    a = 0.1
    #brus = BrusselatorFabricWidget(a, b, h, cnt)
    brus = BrusselatorFabricWidget(0.16, b, h, cnt, eps = eps)
    brus.scale = 10
    brus.show()
    app.exec()
