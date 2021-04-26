from PyQt5 import uic, QtWidgets, QtGui
import sys
from main_window import MainApp
import logging


def main():
    logging.basicConfig(level=logging.INFO)
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    sys.exit(app.exec_())  # и запускаем приложение


main()
# TODO english everywhere
