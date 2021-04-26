from collections import namedtuple
ERROR = namedtuple("Error", ['cause', 'info_to_user'])

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
    err_var = ERROR('NOT_ONE_VARIABLE', 'Please, write one-dimensional function')
    err_null = ERROR('NO_EXPR', 'Please, write your function')
    err_sympy = ERROR('ERROR RUNNING SYMPY', 'Error during function recognition, please follow our example')
