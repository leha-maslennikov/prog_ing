import sys
from PySide6 import QtCore, QtWidgets, QtGui


class ChartWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        size = QtWidgets.QApplication.primaryScreen().size()
        self.resize(size)
        self.setWindowTitle('ChartWinfow')
        #self.move()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ChartWindow()
    window.show()
    app.exec()