import os
import sys
import time
import unittest
from PyQt5 import QtCore
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from app.main_window import *
from app.data_structures import *
from app.about import *
from collections import namedtuple
from app.main_window import *
from app import optimization_src


class Libs_test(unittest.TestCase):
    def test_libs_Text_Creator(self):
        example_method = namedtuple("example_method", ['name', 'color'])
        method = example_method("magic", "orange")
        func = lambda x: 2 * x
        line = TextCreator.method_result_to_text(method, 2, func)
        self.assertEqual(line, "magic(orange if plot is activated) find minimum in x = 2, with value of function f("
                               "x)= 4\n\n")


class Main_Window_test(unittest.TestCase):
    def setUp(self):
        self.app = QtWidgets.QApplication(['--platform offscreen'])
        self.form = MainApp()
        self.base_eq = "x"
        self.quadratic = "(x-0.5)**2"
        self.quadratic_ans = 0.5

    def test_default(self):
        for stuff in self.form.all_textEdit:
            self.assertEqual(stuff.qt_obj.toPlainText(), "")
        for box in self.form.all_checkBox:
            self.assertFalse(box.qt_obj.isChecked())
        for element in self.form.all_hided:
            self.assertFalse(element.qt_obj.isVisible())

    def test_bad_input_null(self):
        # null
        self.form.equation.qt_obj.setText("")
        self.form.pushButton.click()
        self.assertEqual(self.form.error_label.qt_obj.toPlainText(), ERRORS.err_null.info_to_user)

    def test_bad_input_two_dim(self):
        # not one dim
        self.form.equation.qt_obj.setText("x+y")
        self.form.pushButton.click()
        self.assertEqual(self.form.error_label.qt_obj.toPlainText(), ERRORS.err_var.info_to_user)

    def test_bad_input_bad_sympy(self):
        # bad sympy
        self.form.equation.qt_obj.setText("2x")
        self.form.pushButton.click()
        self.assertEqual(self.form.error_label.qt_obj.toPlainText(), ERRORS.err_sympy.info_to_user)

    def test_param_all_clicked(self):
        self.form.equation.qt_obj.setText(self.base_eq)
        self.form.DICHOTOMY.qt_obj.click()
        self.form.GOLDEN.qt_obj.click()
        self.form.FIBONACCI.qt_obj.click()
        res = self.form.run_optimization()
        self.assertEqual(len(res), 3)  # 3

    def test_param_some_clicked(self):
        self.form.equation.qt_obj.setText(self.base_eq)
        self.form.DICHOTOMY.qt_obj.click()
        self.form.FIBONACCI.qt_obj.click()
        res = self.form.run_optimization()
        self.assertEqual(len(res), 2)  # 2

    def test_param_no_clicked(self):
        self.form.equation.qt_obj.setText(self.base_eq)
        res = self.form.run_optimization()
        self.assertEqual(len(res), 0)

    def test_setting_bad_eps(self):
        self.form.equation.qt_obj.setText(self.base_eq)
        self.form.eps.qt_obj.setText('1e--2')
        self.form.run_optimization()
        self.assertEqual(self.form.error_label.qt_obj.toPlainText(), ERRORS.err_to_float.info_to_user)

    def test_setting_eps(self):
        self.form.equation.qt_obj.setText(self.quadratic)
        self.form.eps.qt_obj.setText('1e-6')
        eps = 1e-6
        self.form.DICHOTOMY.qt_obj.click()
        res = self.form.run_optimization()[0]
        self.assertLess(abs(res[0]-self.quadratic_ans),eps)
        self.form.clear_all()

    def test_clearing_all(self):
        equation = "2*x**2 - 3*x +2 "
        self.form.equation.qt_obj.setText(equation)
        self.form.DICHOTOMY.qt_obj.click()
        self.form.GOLDEN.qt_obj.click()
        self.form.PLOT.qt_obj.click()
        res = self.form.run_optimization()
        self.form.show()
        self.form.clear_all()
        self.assertFalse(self.form.DICHOTOMY.qt_obj.isChecked())
        self.assertTrue(self.form.equation.qt_obj.toPlainText() == "")
        self.assertTrue(self.form.text_answer.qt_obj.toPlainText() == "")

    def test_run_plot(self):
        equation = "x"
        self.form.equation.qt_obj.setText(equation)
        self.form.PLOT.qt_obj.click()
        self.form.pushButton.click()
        self.assertTrue(MainApp.WORKING_PLOT_PATH + MainApp.PLOT_FORMAT in os.listdir())
        # self.form.show()
        # self.assertTrue(self.form.plot_picture.qt_obj.isVisible())
        self.form.clear_all()


class OptimizationRunTest(unittest.TestCase):
    def setUp(self):
        self.equation = lambda x: 2 * x - 1  # "2*x-1"
        self.answer = 0
        self.left_border = 0
        self.right_border = 1
        self.eps = 1e-2

    def test_run_dichotomy(self):
        res = optimization_src.dichotomy(self.equation, self.left_border, self.right_border, self.eps)
        self.assertLess(abs(res - self.answer), self.eps)

    def test_run_golden(self):
        res = optimization_src.goldenSection(self.equation, self.left_border, self.right_border, self.eps)
        self.assertLess(abs(res - self.answer), self.eps)

    def run_fibb(self):
        pass

# TODO clearing
# TODO different borders and eps
# TODO msg
# TODO Тесты на eps
