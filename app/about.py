from PyQt5 import uic, QtWidgets, QtGui
from app import UI_about
import sys

#TODO
class AboutView(QtWidgets.QWidget, UI_about.Ui_About):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.ok_pressed)

    def ok_pressed(self):
        self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = AboutView()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    sys.exit(app.exec_())  # и
