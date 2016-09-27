import scipy.odr
from numpy import *


class Fit(object):
    """docstring for Fit."""

    def __init__(self, maxit=100):
        super(Fit, self).__init__()

        self.maxit = maxit

        self.x, self.xerr = [], []
        self.y, self.yerr = [], []

        self.initial_P = []
        self.output, self.output_err = [], []

        self.fit_function = None

    def init_function(self, equation_str):
        N = equation_str.count("P[")
        n_free = 0

        for n in range(0, N):
            test_str = "P[" + str(n) + "]"

            if equation_str.count(test_str) > 0:
                n_free = n_free + 1

        self.initial_P = []

        for n in range(0, n_free):
            self.initial_P.append(1)

        self.fit_function = lambda P, x: eval(equation_str)

        self.model = scipy.odr.Model(self.fit_function)

    def set_data(self, x, y, xerr=None, yerr=None):
        if xerr is not None and yerr is not None:
            self.fit_data = scipy.odr.RealData(x, y, sx=xerr, sy=yerr)
        else:
            self.fit_data = scipy.odr.RealData(x, y)

    def run(self):
        odr = scipy.odr.ODR(self.fit_data, self.model,
                            maxit=self.maxit, beta0=self.initial_P)

        out = odr.run()

        out.pprint()

        self.output_err = sqrt(diag(out.cov_beta))

        self.output = out.beta

        return out.stopreason
