from PyQt5 import uic, QtWidgets, QtGui
from sympy import *
import sys
from app import design
from app import optimization_src
import matplotlib.pyplot as plt
import numpy as np
from collections import namedtuple

Form, Window = uic.loadUiType("MyApplication.ui")


class TextCreator:
    @staticmethod
    def method_result_to_text(method, x_result, function):
        msg_1 = " find minimum in x = "
        msg_2 = ", with value of function f(x)= "
        name = method.name
        color = method.color
        return name + "(" + color + " if plot is activated)" + msg_1 + str(x_result) + msg_2 + str(
            function(x_result)) + "\n" + "\n"


checkBox_Parameter = namedtuple('checkBox_Parameter', ['name', 'qt_name', 'qt_obj'])
textEdit_Parameter = namedtuple('textEdit_Parameter', ['name', 'qt_name', 'qt_obj'])
textBrowser_Parameter = namedtuple('textBrowser_Parameter', ['name', 'qt_name', 'qt_obj'])
optimization_Parameter = namedtuple('optimization_Parameter', ['name', 'qt_name', 'qt_obj', 'color', 'plot_color'])
ERROR = namedtuple("Error", ['cause', 'info_to_user'])


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    err_var = ERROR('NOT_ONE_VARIABLE', 'Please, write one-dimension function')
    err_null = ERROR('NO_EXPR', 'Please, write your function')

    def __init__(self):

        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        # working buttons
        self.pushButton.clicked.connect(self.run_optimization)
        self.pushButton_2.clicked.connect(self.clear_all)

        # parameters of optimization
        self.PLOT = checkBox_Parameter("PLOT", "checkBox", self.checkBox)
        self.DICHOTOMY = optimization_Parameter("DICHOTOMY", "checkBox_2", self.checkBox_2, "red", "ro")
        self.GOLDEN = optimization_Parameter("GOLDEN", "checkBox_3", self.checkBox_3, "blue", "bo")
        self.FIBONACCI = optimization_Parameter("FIBONACCI", "checkBox_4", self.checkBox_4, "cyan", "co")
        # data of optimization
        self.equation = textEdit_Parameter("equation", "textEdit", self.textEdit)
        self.eps = textEdit_Parameter("eps", "textEdit_3", self.textEdit_3)
        self.left_border = textEdit_Parameter("left_border", "textEdit_2", self.textEdit_2)
        self.right_border = textEdit_Parameter("right_border", "textEdit_4", self.textEdit_4)
        # answer objects
        self.test_answer = textBrowser_Parameter("text_answer", "textBrowser_4", self.textBrowser_4)
        self.plot_picture = textBrowser_Parameter("plot_picture", "label", self.label)

        # other objects
        self.error_label = textBrowser_Parameter("error_label", "textBrowser_5", self.textBrowser_5)

        # lists of objects
        self.all_checkBox = [self.PLOT, self.GOLDEN, self.DICHOTOMY, self.FIBONACCI]
        self.all_textEdit = [self.equation, self.eps, self.left_border, self.right_border]
        self.all_hided = [self.test_answer, self.plot_picture, self.error_label]
        self.all_clear_req = [self.equation, self.eps, self.left_border, self.right_border, self.test_answer,
                              self.plot_picture, self.error_label]
        self.hide_all_needed()

    def hide_all_needed(self):
        for obj in self.all_hided:
            obj.qt_obj.hide()

    def clear_all_needed(self):
        for elem in self.all_clear_req:
            elem.qt_obj.clear()

    def clear_all_checkBox(self):
        for check_Box in self.all_checkBox:
            if check_Box.qt_obj.isChecked():
                check_Box.qt_obj.click()

    def clear_all(self):
        self.hide_all_needed()
        self.clear_all_needed()
        self.clear_all_checkBox()

    def run_optimization(self):

        expr = self.equation.qt_obj.toPlainText()  # get eq from app
        if expr == "":
            # print("nothing")
            return 0  # Нужно возвращать ошибку
        print("expression", expr)
        working_expr = sympify(expr)
        variables = working_expr.free_symbols
        if len(variables) > 1:
            print("to many vars")
            return 1
        x = variables.pop()
        print(x)
        active_param = []
        for par in self.all_checkBox:
            if par.qt_obj.isChecked():
                active_param.append(par.qt_name)
        print("pars", [par for par in active_param])
        working_function = lambda x_value: working_expr.subs(x, x_value)
        text_answer = []
        num_answer = []
        if self.DICHOTOMY.qt_name in active_param:
            _, answer, _ = optimization_src.dichotomy(working_function, 0, 1, 1e-2)
            print("dich", answer)
            text_answer.append(TextCreator.method_result_to_text(self.DICHOTOMY, answer, working_function))
            num_answer.append([answer, self.DICHOTOMY])

        if self.GOLDEN.qt_name in active_param:
            answer = optimization_src.goldenSection(working_function, 0, 1, 1e-2)
            print("gold ", answer)
            text_answer.append(TextCreator.method_result_to_text(self.GOLDEN, answer, working_function))
            num_answer.append([answer, self.GOLDEN])
        if self.FIBONACCI.qt_name in active_param:
            _, answer, _ = optimization_src.dichotomy(working_function, 0, 1, 1e-2)
            print("fib", answer)
            text_answer.append(TextCreator.method_result_to_text(self.FIBONACCI, answer, working_function))
            num_answer.append([answer, self.FIBONACCI])

        if self.PLOT.qt_name in active_param:
            self.function_plot(working_function, 0, 1, num_answer)
        self.print_result(text_answer)

    def print_result(self, list_msg):
        if list_msg:
            self.textBrowser_4.show()
            self.textBrowser_4.setText(''.join(list_msg))

    def function_plot(self, func, a, b, results):
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
        if results:
            for res, method in results:
                # color = self.color_from_method(method)
                plt.plot(res, func(res), method.plot_color)
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

    def ERROR_handler(self, error):
        LOG, msg = error
        # TODO Дописать обработчик ошибок


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    sys.exit(app.exec_())  # и запускаем приложение

