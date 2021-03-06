from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QAction
from sympy import *  # type: ignore
from app.data_structures import *
from app import UI_main_window
from app import optimization_src
import matplotlib.pyplot as plt  # type: ignore
import numpy as np
import logging
from app.about import AboutView

LEFT_BORDER_DEFAULT = 0
EPS_DEFAULT = 1e-2


class MainApp(QtWidgets.QMainWindow, UI_main_window.Ui_Main, QtWidgets.QMenuBar):
    WORKING_PLOT_PATH = 'plot_img'
    PLOT_FORMAT = ".png"

    def __init__(self):

        super().__init__()
        self.about_window = AboutView()
        self.setupUi(self)

        # working buttons
        self.init_working_buttons()

        # Actions
        self.init_actions()

        # parameters of optimization
        self.init_parameters_of_optimization()
        # objects for plot
        self.init_plot()
        # data from user
        self.init_data_of_optimization()
        # objects to show results
        self.init_answer_objects()

        # other objects
        self.init_error_obj()

        # lists of objects
        self.init_lists_of_objects()

        # for safe
        self.hide_all_needed()

    def init_working_buttons(self):
        self.pushButton.clicked.connect(self.run_optimization)
        self.pushButton_2.clicked.connect(self.clear_all)

    def init_lists_of_objects(self):
        self.all_checkBox = [self.PLOT, self.GOLDEN, self.DICHOTOMY, self.FIBONACCI]
        self.all_param = [self.GOLDEN, self.DICHOTOMY, self.FIBONACCI]
        self.all_textEdit = [self.equation, self.eps, self.left_border, self.right_border]
        self.all_hided = [self.text_answer, self.plot_picture, self.error_label]
        self.all_clear_req = [self.equation, self.eps, self.left_border, self.right_border, self.text_answer,
                              self.plot_picture, self.error_label]

    def init_answer_objects(self):
        self.text_answer = textBrowser_Parameter("text_answer", "textBrowser_4", self.textBrowser_4)
        self.plot_picture = textBrowser_Parameter("plot_picture", "label", self.label)

    def init_actions(self):
        aboutAct = QAction('About', self)
        aboutAct.setShortcut('F1')
        aboutAct.setStatusTip('About application')
        aboutAct.triggered.connect(self.run_about)
        aboutMenu = self.menubar
        aboutMenu.addAction(aboutAct)

    def init_parameters_of_optimization(self):

        self.DICHOTOMY = optimization_Parameter("DICHOTOMY", "checkBox_2", self.checkBox_2
                                                , optimization_src.dichotomy, "red", "ro")
        self.GOLDEN = optimization_Parameter("GOLDEN", "checkBox_3", self.checkBox_3,
                                             optimization_src.golden_section, "blue", "bo")
        self.FIBONACCI = optimization_Parameter("FIBONACCI", "checkBox_4", self.checkBox_4,
                                                optimization_src.fibonacci, "cyan", "co")
        optimization_src.setUp() # precalculate fibonacci number

    def init_data_of_optimization(self):
        self.equation = textEdit_Parameter("equation", "textEdit", self.textEdit)
        self.eps = textEdit_Parameter("eps", "textEdit_3", self.textEdit_3)
        self.left_border = textEdit_Parameter("left_border", "textEdit_2", self.textEdit_2)
        self.right_border = textEdit_Parameter("right_border", "textEdit_4", self.textEdit_4)

    def init_error_obj(self):
        self.error_label = textBrowser_Parameter("error_label", "textBrowser_5", self.textBrowser_5)

    def init_plot(self):
        # plot
        self.PLOT = checkBox_Parameter("PLOT", "checkBox", self.checkBox)

    def hide_all_needed(self):
        for obj in self.all_hided:
            obj.qt_obj.hide()

    def clear_all_obj(self):
        for elem in self.all_clear_req:
            elem.qt_obj.clear()

    def clear_all_checkBox(self):
        for check_Box in self.all_checkBox:
            if check_Box.qt_obj.isChecked():
                check_Box.qt_obj.click()

    def is_empty_text(self, window_elem):
        return window_elem.qt_obj.toPlainText() == ""

    def clear_all(self):
        self.hide_all_needed()
        self.clear_all_obj()
        self.clear_all_checkBox()

    def run_about(self):
        self.about_window.show()

    def run_optimization(self):
        self.hide_all_needed()
        self.error_label.qt_obj.clear()
        try:
            x, working_function = self.get_var_and_func()
            eps = self.set_eps()
            left_border, right_border = self.set_borders()
            text_answer, num_answer = self.run_parameters(working_function, left_border, right_border, eps)
        except AppException as ex:
            self.ERROR_handler(ex)
            return 1
        self.print_result(text_answer)
        return num_answer

    def safe_float(self, line):
        try:
            return float(line)
        except Exception:
            raise ErrFloatException

    def set_eps(self):
        if self.is_empty_text(self.eps):
            logging.warning("No epsilon chosen, running default")
            return EPS_DEFAULT
        else:
            return self.safe_float(self.eps.qt_obj.toPlainText())

    def set_borders(self):
        if self.is_empty_text(self.left_border):
            left = LEFT_BORDER_DEFAULT
        else:
            left = self.safe_float(self.left_border.qt_obj.toPlainText())

        if self.is_empty_text(self.right_border):
            right = left + 1
        else:
            right = self.safe_float(self.right_border.qt_obj.toPlainText())
        if left > right:
            raise ErrBordersException
        return left, right

    def run_parameters(self, working_function, left_border, right_border, eps):
        text_answer = []  # text to show User
        num_answer = []  # num to plot
        for param in self.all_param:
            if param.qt_obj.isChecked():  # checkBox chosen
                answer = self.run_parameter(param, working_function, left_border, right_border, eps)
                text_answer.append(TextCreator.method_result_to_text(param, answer, working_function))
                num_answer.append([answer, param])

        if self.PLOT.qt_obj.isChecked():
            try:
                self.function_plot(working_function, left_border, right_border, num_answer)
                logging.info("plot created")
            except Exception:
                self.plot_picture.qt_obj.hide()
                raise ErrPlotException
        return text_answer, num_answer

    def run_parameter(self, param, working_function, left_border, right_border, eps):
        try:
            answer = param.function(working_function, left_border, right_border, eps)
            logging.info(param.name + " result " + str(answer))
            return answer
        except Exception:
            logging.error(param.name + "crushed during running")
            raise ErrParamException

    def get_var_and_func(self):  # function to scan incoming expr for var and func
        if self.is_empty_text(self.equation):
            raise ErrNullException
        expr = self.equation.qt_obj.toPlainText()
        logging.info("expression " + str(expr))
        try:
            working_expr = sympify(expr)
        except Exception:
            raise ErrSympyException
        variables = working_expr.free_symbols
        if len(variables) > 1:
            raise ErrVarException
        x = variables.pop()  # get our variable
        logging.info("var " + str(x))
        working_function = lambda x_value: working_expr.subs(x, x_value)  # create standard function
        return x, working_function

    def print_result(self, list_msg):  # to show user msg
        if list_msg:
            self.text_answer.qt_obj.show()
            self.text_answer.qt_obj.setText(''.join(list_msg))

    def function_plot(self, func, a, b, results):  # making and show plot
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
                plt.plot(res, func(res), method.plot_color)
        plt.savefig(MainApp.WORKING_PLOT_PATH)
        plt.close()
        image_path = MainApp.WORKING_PLOT_PATH + MainApp.PLOT_FORMAT
        label_Image = self.plot_picture.qt_obj
        label_Image.show()
        image_profile = QtGui.QImage(image_path)  # QImage object
        image_profile = image_profile.scaled(label_Image.width(), label_Image.height())
        label_Image.setPixmap(QtGui.QPixmap.fromImage(image_profile))

    def ERROR_handler(self, errException):
        LOG = errException.to_log()
        msg = str(errException)
        logging.error(LOG)
        self.error_label.qt_obj.setText(msg)
        self.error_label.qt_obj.show()
