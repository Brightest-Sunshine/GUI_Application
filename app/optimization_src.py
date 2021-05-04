from math import sqrt


def dichotomy(func, a, b, eps, counter=0):
    while b - a > eps:
        mean = (a + b) / 2
        delta = 0.001 * (b - a)
        x1, x2 = mean - delta, mean + delta
        f_x1, f_x2 = func(x1), func(x2)
        counter = counter + 2
        if f_x1 <= f_x2:
            b = x2
        else:
            a = x1
    x_min = (a + b) / 2
    return x_min


def goldenSection(func, a, b, eps):
    phi = (1 + sqrt(5)) / 2
    x1 = b - (b - a) / phi
    x2 = a + (b - a) / phi
    f_x1, f_x2 = func(x1), func(x2)
    tau = 1 / phi
    eps_n = (b - a) / 2
    while eps_n > eps:
        if f_x1 <= f_x2:
            b = x2
            x2 = x1
            f_x2 = f_x1
            x1 = b - tau * (b - a)
            f_x1 = func(x1)
        else:
            a = x1
            x1 = x2
            f_x1 = f_x2
            x2 = a + tau * (b - a)
            f_x2 = func(x2)
        eps_n = tau * eps_n
    x_min = (a + b) / 2
    return x_min


def fibonacciSequence(n):
    if n == 1 or n == 2:
        return 1
    step_1 = 1
    step_2 = 1
    for i in range(2, n):
        tmp = step_2
        step_2 = step_1
        step_1 = tmp + step_2
    return step_1


def fibonacci(func, a, b, eps):
    N = (b - a) / eps
    n = 2  # first and second fib number are eq
    fib = 1
    fib_2 = 1
    while fib < N:
        n += 1
        tmp = fib_2
        fib_2 = fib
        fib = tmp + fib_2
    return _fibonacci(func, a, b, n, 0, eps)


def _fibonacci(func, a, b, n, k, eps, lambd=float('inf'), mu=float('inf'), prev_f=float('inf')):
    if k <= n - 2:
        if lambd == float('inf'):
            lambd = a + fibonacciSequence(n - k - 1) / fibonacciSequence(n - k + 1) * (b - a)
            if k != 0:
                f1 = func(lambd)
                f2 = prev_f
        if mu == float('inf'):
            mu = a + fibonacciSequence(n - k) / fibonacciSequence(n - k + 1) * (b - a)
            if k != 0:
                f1 = prev_f
                f2 = func(mu)
        if k == 0:
            f1 = func(lambd)
            f2 = func(mu)
    else:
        x_min = (a + b) / 2
        return x_min
    if f1 > f2:
        k += 1
        prev_f = f2
        if k < n - 2:
            a = lambd
            lambd = float('inf')
        else:
            b = mu
    else:
        prev_f = f1
        k += 1
        if k < n - 2:
            b = mu
            mu = float('inf')
        else:
            a = lambd
    return _fibonacci(func, a, b, n, k, mu, lambd, prev_f, eps)
