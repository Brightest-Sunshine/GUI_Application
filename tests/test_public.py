import os
import unittest
from collections import namedtuple
from app.main_window import *
from app import optimization_src

POSITION_OF_ANSWER = 0


class Libs_test(unittest.TestCase):
    def test_libs_Text_Creator(self):
        msg = "Incorrect text creation"
        example_method = namedtuple("example_method", ['name', 'color'])
        method = example_method("magic", "orange")
        func = lambda x: 2 * x
        line = TextCreator.method_result_to_text(method, 2, func)
        self.assertEqual(line, "magic(orange if plot is activated) find minimum in x = 2, with value of function f("
                               "x)= 4\n\n", msg=msg)


class Main_Window_test(unittest.TestCase):
    def setUp(self):
        self.app = QtWidgets.QApplication(['--platform offscreen'])
        self.form = MainApp()
        self.base_eq = "x"
        self.quadratic = "(x-0.5)**2"
        self.quadratic_ans = 0.5  # Depends on borders of course

    def test_default(self):
        msg = "Non-standard default state"
        for stuff in self.form.all_textEdit:
            self.assertEqual(stuff.qt_obj.toPlainText(), "", msg=msg)
        for box in self.form.all_checkBox:
            self.assertFalse(box.qt_obj.isChecked(), msg=msg)
        for element in self.form.all_hided:
            self.assertFalse(element.qt_obj.isVisible(), msg=msg)

    def test_bad_input_null(self):
        msg = "Dont show error about null input"
        self.form.equation.qt_obj.setText("")
        self.form.pushButton.click()
        self.assertEqual(self.form.error_label.qt_obj.toPlainText(), ERRORS.err_null.info_to_user, msg=msg)

    def test_bad_input_two_dim(self):
        msg = "Dont show error about  more than one dim"
        self.form.equation.qt_obj.setText("x+y")
        self.form.pushButton.click()
        self.assertEqual(self.form.error_label.qt_obj.toPlainText(), ERRORS.err_var.info_to_user, msg=msg)

    def test_bad_input_bad_sympy(self):
        msg = "Dont show error about bad sympy syntax"
        self.form.equation.qt_obj.setText("2x")
        self.form.pushButton.click()
        self.assertEqual(self.form.error_label.qt_obj.toPlainText(), ERRORS.err_sympy.info_to_user, msg=msg)

    def test_param_all_clicked(self):
        msg = "Dont return all clicked param result"
        self.form.equation.qt_obj.setText(self.base_eq)
        self.form.DICHOTOMY.qt_obj.click()
        self.form.GOLDEN.qt_obj.click()
        self.form.FIBONACCI.qt_obj.click()
        res = self.form.run_optimization()
        self.assertEqual(len(res), 3, msg=msg)  # 3

    def test_param_some_clicked(self):
        msg = "Dont return all clicked param result"
        self.form.equation.qt_obj.setText(self.base_eq)
        self.form.DICHOTOMY.qt_obj.click()
        self.form.FIBONACCI.qt_obj.click()
        res = self.form.run_optimization()
        self.assertEqual(len(res), 2, msg=msg)  # 2

    def test_param_no_clicked(self):
        msg="Return unidentified staff"
        self.form.equation.qt_obj.setText(self.base_eq)
        res = self.form.run_optimization()
        self.assertEqual(len(res), 0,msg=msg)

    def test_setting_bad_eps(self):
        msg = "Dont show error about bad eps"
        self.form.equation.qt_obj.setText(self.base_eq)
        self.form.eps.qt_obj.setText('1e--2')
        self.form.run_optimization()
        self.assertEqual(self.form.error_label.qt_obj.toPlainText(), ERRORS.err_to_float.info_to_user, msg=msg)

    def test_setting_eps(self):
        msg="Answer not close as eps value expected to be"
        self.form.equation.qt_obj.setText(self.quadratic)
        self.form.eps.qt_obj.setText('1e-6')
        eps = 1e-6
        self.form.DICHOTOMY.qt_obj.click()
        res = self.form.run_optimization()[0]
        self.assertLess(abs(res[0] - self.quadratic_ans), eps, msg=msg)
        self.form.clear_all()

    def test_clearing_all(self):
        msg = "Not clear what expected to be clean"
        equation = "2*x**2 - 3*x +2 "
        self.form.equation.qt_obj.setText(equation)
        self.form.DICHOTOMY.qt_obj.click()
        self.form.GOLDEN.qt_obj.click()
        self.form.PLOT.qt_obj.click()
        res = self.form.run_optimization()
        self.form.show()
        self.form.clear_all()
        self.assertFalse(self.form.DICHOTOMY.qt_obj.isChecked(),msg=msg)
        self.assertTrue(self.form.equation.qt_obj.toPlainText() == "",msg=msg)
        self.assertTrue(self.form.text_answer.qt_obj.toPlainText() == "",msg=msg)

    def test_run_plot(self):
        msg = "Dont create plot file, so where is nothing to show"
        self.form.equation.qt_obj.setText(self.base_eq)
        self.form.PLOT.qt_obj.click()
        self.form.pushButton.click()
        self.assertTrue(MainApp.WORKING_PLOT_PATH + MainApp.PLOT_FORMAT in os.listdir(),msg=msg)
        self.form.clear_all()

    def test_borders(self):
        msg = "Optimization not happening in expected borders"
        self.form.equation.qt_obj.setText(self.base_eq)
        self.form.left_border.qt_obj.setText("1")
        self.form.right_border.qt_obj.setText("2")
        self.form.DICHOTOMY.qt_obj.click()
        res = self.form.run_optimization()
        answer = 1
        this_res = res[0]
        self.assertLess(abs(this_res[POSITION_OF_ANSWER] - answer), EPS_DEFAULT, msg=msg)

    def test_bad_borders(self):
        msg = "Dont show error about bad borders"
        self.form.equation.qt_obj.setText(self.base_eq)
        self.form.left_border.qt_obj.setText("2")
        self.form.right_border.qt_obj.setText("1")
        self.form.run_optimization()
        self.assertEqual(self.form.error_label.qt_obj.toPlainText(), ERRORS.err_borders.info_to_user, msg=msg)


class OptimizationRunTest(unittest.TestCase):
    def setUp(self):
        self.equation = lambda x: 2 * x - 1  # "2*x-1"
        self.answer = 0
        self.left_border = 0
        self.right_border = 1
        self.eps = 1e-2

    def test_run_dichotomy(self):
        msg = "dichotomy dont show expected precision"
        res = optimization_src.dichotomy(self.equation, self.left_border, self.right_border, self.eps)
        self.assertLess(abs(res - self.answer), self.eps, msg=msg)

    def test_run_golden(self):
        msg="golden section dont show expected precision"
        res = optimization_src.goldenSection(self.equation, self.left_border, self.right_border, self.eps)
        self.assertLess(abs(res - self.answer), self.eps, msg=msg)

    def run_fib(self):
        pass

# TODO README + documentation
