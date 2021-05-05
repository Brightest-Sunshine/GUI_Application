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


class AppException(Exception):
    def to_log(self):
        pass


class ErrNullException(AppException):
    def __str__(self):
        return 'Please, write your function\n'

    def to_log(self):
        return 'NO_EXPR'


class ErrVarException(AppException):
    def __str__(self):
        return 'Please, write one-dimensional function\n'

    def to_log(self):
        return 'NOT_ONE_VARIABLE'


class ErrSympyException(AppException):
    def __str__(self):
        return 'Error during function recognition, please follow our example\n'

    def to_log(self):
        return 'ERROR RUNNING SYMPY'


class ErrFloatException(AppException):
    def __str__(self):
        return 'Please, write float number or scientific notation\n'

    def to_log(self):
        return 'ERROR CONVERTING TO FLOAT'


class ErrBordersException(AppException):
    def __str__(self):
        return 'Please, choose left border lesser than right\n'

    def to_log(self):
        return 'ERROR left border bigger than right'


class ErrPlotException(AppException):
    def __str__(self):
        return 'Unknown error during plot  creation\n'

    def to_log(self):
        return 'ERROR problems during plot creating'


class ErrParamException(AppException):
    def __str__(self):
        return 'Error during param running\n'

    def to_log(self):
        return 'Exception during param function running'


checkBox_Parameter = namedtuple('checkBox_Parameter', ['name', 'qt_name', 'qt_obj'])
textEdit_Parameter = namedtuple('textEdit_Parameter', ['name', 'qt_name', 'qt_obj'])
textBrowser_Parameter = namedtuple('textBrowser_Parameter', ['name', 'qt_name', 'qt_obj'])
optimization_Parameter = namedtuple('optimization_Parameter',
                                    ['name', 'qt_name', 'qt_obj', 'function', 'color', 'plot_color'])
