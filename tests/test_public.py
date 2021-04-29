import os
import sys
import time
import unittest
from PyQt5 import QtCore
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from app.main_window import *
from app.libs import *
from app.about import *
from collections import namedtuple
from app.main_window import *


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

    def test_default(self):
        for stuff in self.form.all_textEdit:
            self.assertEqual(stuff.qt_obj.toPlainText(), "")
        for box in self.form.all_checkBox:
            self.assertFalse(box.qt_obj.isChecked())
        for element in self.form.all_hided:
            self.assertFalse(element.qt_obj.isVisible())

    def test_bad_input(self):
        # null
        self.form.equation.qt_obj.setText("")
        self.form.pushButton.click()
        self.assertEqual(self.form.error_label.qt_obj.toPlainText(), ERRORS.err_null.info_to_user)

        # not one dim
        self.form.equation.qt_obj.setText("x+y")
        self.form.pushButton.click()
        self.assertEqual(self.form.error_label.qt_obj.toPlainText(), ERRORS.err_var.info_to_user)

        # bad sympy
        self.form.equation.qt_obj.setText("2x")
        self.form.pushButton.click()
        self.assertEqual(self.form.error_label.qt_obj.toPlainText(), ERRORS.err_sympy.info_to_user)

        # not choose checkbox

    def test_run_optimization_methods(self):
        equation = "2*x-1"
        answ = 0
        self.form.equation.qt_obj.setText(equation)
        self.form.DICHOTOMY.qt_obj.click()
        self.form.GOLDEN.qt_obj.click()
        res = self.form.run_optimization()
        dich, gold = res
        self.assertLess(abs(answ - dich[0]), EPS_DEFAULT)
        self.assertLess(abs(answ - gold[0]), EPS_DEFAULT)
        self.form.clear_all()

    def test_run_plot(self):
        equation = "x"
        self.form.equation.qt_obj.setText(equation)
        self.form.PLOT.qt_obj.click()
        self.form.pushButton.click()
        self.assertTrue("plot_img.png" in os.listdir())  # TODO Default pic name?
        self.form.show()
        self.assertTrue(self.form.plot_picture.qt_obj.isVisible())
        self.form.clear_all()
