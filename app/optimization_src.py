import functools
from math import sqrt


# from book "Лесин В.В.  и Лисовец Ю.П., Основы методов отпимизации",3-rd edition p.37
def dichotomy(func, a, b, eps):
    while b - a > eps:
        mean = (a + b) / 2
        delta = 0.001 * (b - a)  # 0.001 constant choose from book
        x1, x2 = mean - delta, mean + delta  # get points delta far from mean
        # start location a.........x1.mean.x2...........b
        f_x1, f_x2 = func(x1), func(x2)  # cal function where
        if f_x1 <= f_x2:
            b = x2
        else:
            a = x1
    x_min = (a + b) / 2  # return result between borders
    return x_min


# from book "Лесин В.В.  и Лисовец Ю.П. ,Основы методов отпимизации",3-rd edition p.39
def golden_section(func, a, b, eps):
    phi = (1 + sqrt(5)) / 2  # golden section
    x1 = b - (b - a) / phi
    x2 = a + (b - a) / phi
    f_x1, f_x2 = func(x1), func(x2)
    tau = 1 / phi
    eps_n = (b - a) / 2
    # so start location of point look this : a .... x1....x2....b
    while eps_n > eps:
        if f_x1 <= f_x2:  #
            b = x2  # change right of borders to x2
            x2 = x1  # make new x2 as x1
            f_x2 = f_x1  # to not call again
            x1 = b - tau * (b - a)  # calc new x1
            f_x1 = func(x1)  # get func value where
            # after this section we have a ....x1=new(x1)....x2=old(x1) ....b=odl(x2)
        else:
            a = x1  # change left border to x1
            x1 = x2
            f_x1 = f_x2
            x2 = a + tau * (b - a)  # calc new x2
            f_x2 = func(x2)
            # after this section we have a=old(x1) ....x1=old(x2)....x2=new(x2) ....b
        eps_n = tau * eps_n  # make our eps even smaller
    x_min = (a + b) / 2  # return result between borders
    return x_min


def memoize(function):  # memorize calculated numbers, so we dont need to calc them again
    memo = {}

    @functools.wraps(function)
    def helper(x):
        if x not in memo:
            memo[x] = function(x)
        return memo[x]

    return helper


@memoize
def fibonacci_sequence(n):
    if n == 0 or n == 1:
        return 1
    else:
        return fibonacci_sequence(n - 1) + fibonacci_sequence(n - 2)


# from book "Ногин В.Д, Протодьяконов И.О.,Евлампиев И.И. Основы теории оптимизации" , p.113

def fibonacci(func, a, b, eps):
    N = (b - a) / eps
    n = 2  # first and second fib number are eq
    fib = 1
    fib_2 = 1
    while fib < N:  # counting number of fib number who first upper than N
        n += 1
        tmp = fib_2
        fib_2 = fib
        fib = tmp + fib_2
    return _fibonacci(func, a, b, n, 0)


def _fibonacci(func, a, b, n, k):
    start_delta = b - a  # to use in method run
    x1 = a + fibonacci_sequence(n) / fibonacci_sequence(n + 2) * start_delta
    x2 = a + b - x1
    # a.....x1.....(mean).......x2........b
    # same as dichotomy
    while k < n - 1:
        f_x1, f_x2 = func(x1), func(x2)
        if f_x1 <= f_x2:
            b = x2
        else:
            a = x1
        # different new x1,x2 calculating
        x1 = a + fibonacci_sequence(n - k) / fibonacci_sequence(n + 2) * start_delta
        x2 = a + fibonacci_sequence(n - k + 1) / fibonacci_sequence(n + 2) * start_delta
        k += 1
    x_min = (a + b) / 2
    return x_min


def setUp():
    fibonacci_sequence(30)
