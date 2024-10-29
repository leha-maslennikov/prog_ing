"""В разработке"""

from PySide6 import QtCore, QtWidgets, QtGui
from .ChartWidget import ChartWidget


class MainWindowWidget(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.resize(700, 700)
        self.chart_widget = ChartWidget()
        self.setCentralWidget(self.chart_widget)
