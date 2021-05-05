from PyQt5 import QtWidgets
from app import UI_about
import sys


class AboutView(QtWidgets.QWidget, UI_about.Ui_About):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.ok_pressed)

    def ok_pressed(self):
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AboutView()
    window.show()
    sys.exit(app.exec_())
