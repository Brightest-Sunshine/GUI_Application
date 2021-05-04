from collections import namedtuple

ERROR = namedtuple("ERROR", ['cause', 'info_to_user'])


class TextCreator:
    @staticmethod
    def method_result_to_text(method, x_result, function):
        msg_1 = " find minimum in x = "
        msg_2 = ", with value of function f(x)= "
        name = method.name
        color = method.color
        return name + "(" + color + " if plot is activated)" + msg_1 + str(x_result) + msg_2 + str(
            function(x_result)) + "\n" + "\n"


class ERRORS:
    err_var = ERROR('NOT_ONE_VARIABLE', 'Please, write one-dimensional function\n')
    err_null = ERROR('NO_EXPR', 'Please, write your function\n')
    err_sympy = ERROR('ERROR RUNNING SYMPY', 'Error during function recognition, please follow our example\n')
    err_to_float = ERROR('ERROR CONVERTING TO FLOAT', 'Please, write float number or scientific notation\n')
    err_borders = ERROR('ERROR left border bigger than right', 'Please, choose left border lesser than right\n')
    err_plot = ERROR('ERROR problems during plot creating', 'Unknown error during plot  creation\n')
    err_param_run = ERROR('Exception during param function running', 'Error during param running\n')
    err_optimization_run = ERROR('Exception during optimization run', 'Optimization error caused by following errors:\n')


checkBox_Parameter = namedtuple('checkBox_Parameter', ['name', 'qt_name', 'qt_obj'])
textEdit_Parameter = namedtuple('textEdit_Parameter', ['name', 'qt_name', 'qt_obj'])
textBrowser_Parameter = namedtuple('textBrowser_Parameter', ['name', 'qt_name', 'qt_obj'])
optimization_Parameter = namedtuple('optimization_Parameter',
                                    ['name', 'qt_name', 'qt_obj', 'function', 'color', 'plot_color'])
