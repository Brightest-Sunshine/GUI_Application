from PyQt5 import QtWidgets
import sys
from app.main_window import MainApp  # type: ignore
import logging


def main():
    logging.basicConfig(level=logging.INFO)
    app = QtWidgets.QApplication(sys.argv)  # new instance QApplication
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


main()
