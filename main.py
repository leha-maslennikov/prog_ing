import sys
from PySide6 import QtWidgets
from views.MainWindowWidget import MainWindowWidget


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindowWidget()
    window.chart_widget.scale = 20
    window.show()
    app.exec()