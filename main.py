from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication
from sympy import *
import sys
import design
import optimization_src
import matplotlib.pyplot as plt
import numpy as np

Form, Window = uic.loadUiType("MyApplication.ui")

PLOT = "checkBox"
DICHOTOMY = "checkBox_2"
GOLDEN = "checkBox_3"
FIBONACCI = "checkBox_4"


class TextCreator:
    @staticmethod
    def method_result_to_text(method_name, x_result, function):
        msg_1 = " find minimum in x = "
        msg_2 = ", with value of function f(x)= "
        return method_name + msg_1 + str(x_result) + msg_2 + str(function(x_result)) + "\n"


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(self.run_optimization)
        self.pushButton_2.clicked.connect(self.clear_all)
        self.textBrowser_4.hide()
        self.label.hide()

    def clear_all(self):
        self.textBrowser_4.hide()
        self.textBrowser_4.clear()
        self.label.hide()
        self.label.clear()
        if self.checkBox.isChecked():
            self.checkBox.click()
        if self.checkBox_3.isChecked():
            self.checkBox_3.click()
        if self.checkBox_2.isChecked():
            self.checkBox_2.click()
        if self.checkBox_4.isChecked():
            self.checkBox_4.click()
        self.textEdit.clear()
        self.textEdit_2.clear()
        self.textEdit_3.clear()

        pass

    def run_optimization(self):

        expr = self.textEdit.toPlainText()
        if expr == "":
            #print("nothing")
            return 0  # Нужно возвращать ошибку
        print("expression", expr)
        working_expr = sympify(expr)
        variables = working_expr.free_symbols
        if len(variables) > 1:
            print("to many vars")
            return 1
        x = variables.pop()
        print(x)
        param = [self.checkBox, self.checkBox_2, self.checkBox_3, self.checkBox_4]
        active_param = []
        for par in param:
            if par.isChecked():
                active_param.append(par.objectName())
        print("pars", [par for par in active_param])
        working_function = lambda x_value: working_expr.subs(x, x_value)
        text_answer = []
        num_answer = []
        if DICHOTOMY in active_param:
            _, answer, _ = optimization_src.dichotomy(working_function, 0, 1, 1e-2)
            print("dich", answer)
            text_answer.append(TextCreator.method_result_to_text("Dichotomy", answer, working_function))
            num_answer.append(answer)

        if GOLDEN in active_param:
            answer = optimization_src.goldenSection(working_function, 0, 1, 1e-2)
            print("gold ", answer)
            text_answer.append(TextCreator.method_result_to_text("GOLDEN SECTION", answer, working_function))
            num_answer.append(answer)
        if FIBONACCI in active_param:
            # TODO Сделать его нормально.
            pass
        if PLOT in active_param:
            self.function_plot(working_function, 0, 1, num_answer)
        self.print_result(text_answer)

    def print_result(self, list_msg):
        if list_msg:
            self.textBrowser_4.show()
            self.textBrowser_4.setText(''.join(list_msg))

    def function_plot(self, func, a, b, result):
        x = np.linspace(a, b, 100)
        y = [func(i) for i in x]
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.spines['left'].set_position('center')
        ax.spines['bottom'].set_position('center')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        # plot the function
        plt.plot(x, y, 'r')
        if result:
            for res in result:
                plt.plot(res, func(res), 'bo')
        # show the plot
        # plt.show()
        plt.savefig('plot_img')
        plt.close()
        image_path = 'plot_img.png'
        # show plot
        frame = self  # Replace it with any frame you will putting this label_image on it
        label_Image = self.label
        label_Image.show()
        image_profile = QtGui.QImage(image_path)  # QImage object
        image_profile = image_profile.scaled(label_Image.width(), label_Image.height())
        label_Image.setPixmap(QtGui.QPixmap.fromImage(image_profile))


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    sys.exit(app.exec_())  # и запускаем приложение


main()
