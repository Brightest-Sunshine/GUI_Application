from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QAction
from sympy import * # type: ignore
from app.libs import ERRORS, TextCreator
from app import UI_main_window
from app import optimization_src
import matplotlib.pyplot as plt # type: ignore
import numpy as np
from collections import namedtuple
import logging
from app.about import AboutView

checkBox_Parameter = namedtuple('checkBox_Parameter', ['name', 'qt_name', 'qt_obj'])
textEdit_Parameter = namedtuple('textEdit_Parameter', ['name', 'qt_name', 'qt_obj'])
textBrowser_Parameter = namedtuple('textBrowser_Parameter', ['name', 'qt_name', 'qt_obj'])
optimization_Parameter = namedtuple('optimization_Parameter', ['name', 'qt_name', 'qt_obj', 'color', 'plot_color'])
LEFT_BORDER_DEFAULT = 0
EPS_DEFAULT = 1e-2


class MainApp(QtWidgets.QMainWindow, UI_main_window.Ui_Main, QtWidgets.QMenuBar):

    def __init__(self):

        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле UI_main_window.py
        super().__init__()
        self.about_window = AboutView()  # Создаём объект класса ExampleApp
        self.setupUi(self)  # Это нужно для инициализации нашего дизайн

        # working buttons
        self.pushButton.clicked.connect(self.run_optimization)
        self.pushButton_2.clicked.connect(self.clear_all)
        # self.menuEq_Syntaxys.mousePressEvent.connect(self.clear_all)

        # Actions
        aboutAct = QAction('About', self)
        aboutAct.setShortcut('F1')
        aboutAct.setStatusTip('About application')
        aboutAct.triggered.connect(self.run_about)
        aboutMenu = self.menubar
        aboutMenu.addAction(aboutAct)

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

    def run_about(self):
        # self.hide()
        # app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
        self.about_window.show()  # Показываем окно
        # sys.exit(app.exec_())  # и

    def run_optimization(self):
        self.hide_all_needed()
        expr = self.equation.qt_obj.toPlainText()  # get eq from app
        try:
            x, working_function = self.get_var_and_func(expr)
            eps = self.set_eps()
        except Exception:
            return 1

        left_border, right_border = self.set_borders()
        text_answer, num_answer = self.run_param(working_function, left_border, right_border, eps)
        self.print_result(text_answer)
        return num_answer

    def set_eps(self):  # TODO ERROR
        if self.eps.qt_obj.toPlainText() == "":
            return EPS_DEFAULT
        else:
            try:
                return float(self.eps.qt_obj.toPlainText())
            except Exception:
                self.ERROR_handler(ERRORS.err_to_float)
                raise Exception

    def set_borders(self):  # TODO ERROR
        if self.left_border.qt_obj.toPlainText() == "":
            left = LEFT_BORDER_DEFAULT
        else:
            try:
                left = float(self.left_border.qt_obj.toPlainText())
            except Exception:
                self.ERROR_handler(ERRORS.err_to_float)
                raise Exception

        if self.right_border.qt_obj.toPlainText() == "":
            right = left + 1
        else:
            try:
                right = float(self.right_border.qt_obj.toPlainText())
            except Exception:
                self.ERROR_handler(ERRORS.err_to_float)
                raise Exception

        if left > right:
            self.ERROR_handler(ERRORS.err_borders)
            raise Exception
        return left, right

    def run_param(self, working_function, left_border, right_border, eps):
        text_answer = []
        num_answer = []
        if self.DICHOTOMY.qt_obj.isChecked():
            answer = optimization_src.dichotomy(working_function, left_border, right_border, eps)
            logging.info("dich result " + str(answer))
            text_answer.append(TextCreator.method_result_to_text(self.DICHOTOMY, answer, working_function))
            num_answer.append([answer, self.DICHOTOMY])

        if self.GOLDEN.qt_obj.isChecked():
            answer = optimization_src.goldenSection(working_function, left_border, right_border, eps)
            logging.info("gold result " + str(answer))
            text_answer.append(TextCreator.method_result_to_text(self.GOLDEN, answer, working_function))
            num_answer.append([answer, self.GOLDEN])
        if self.FIBONACCI.qt_obj.isChecked():
            answer = optimization_src.dichotomy(working_function, left_border, right_border, eps)
            logging.info("fib result " + str(answer))
            text_answer.append(TextCreator.method_result_to_text(self.FIBONACCI, answer, working_function))
            num_answer.append([answer, self.FIBONACCI])

        if self.PLOT.qt_obj.isChecked():
            try:
                self.function_plot(working_function, left_border, right_border, num_answer)
                logging.info("plot created")
            except Exception:
                self.ERROR_handler(ERRORS.err_plot)
                self.plot_picture.qt_obj.hide()
        return text_answer, num_answer

    def get_var_and_func(self, expr):
        if expr == "":
            self.ERROR_handler(ERRORS.err_null)
            raise Exception
        logging.info("expression "+str(expr))
        try:
            working_expr = sympify(expr)
        except SympifyError:
            self.ERROR_handler(ERRORS.err_sympy)
            raise Exception
        variables = working_expr.free_symbols
        if len(variables) > 1:
            self.ERROR_handler(ERRORS.err_var)
            raise Exception
        x = variables.pop()
        logging.info("var "+ str(x))
        working_function = lambda x_value: working_expr.subs(x, x_value)  # create standard function
        return x, working_function

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
        label_Image = self.plot_picture.qt_obj
        label_Image.show()
        image_profile = QtGui.QImage(image_path)  # QImage object
        image_profile = image_profile.scaled(label_Image.width(), label_Image.height())
        label_Image.setPixmap(QtGui.QPixmap.fromImage(image_profile))

    def ERROR_handler(self, error):
        LOG, msg = error
        # print(LOG)
        logging.error(LOG)
        self.textBrowser_5.clear()
        self.textBrowser_5.setText(msg)
        self.textBrowser_5.show()
        # TODO try except везде, где мы общаемся в библиотекой
