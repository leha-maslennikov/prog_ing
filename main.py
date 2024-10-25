import sys
from PySide6 import QtWidgets
from views.BrusselatorWidget import BrusselatorWidget
from views import ChartWidget


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    chart_widget = ChartWidget()
    brusselator = BrusselatorWidget(chart_widget)
    chart_widget.show()
    brusselator.show()
    app.exec()