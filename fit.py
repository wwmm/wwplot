import scipy.odr
from numpy import *


class Fit(object):
    """docstring for Fit."""

    def __init__(self):
        super(Fit, self).__init__()

        self.x, self.xerr = [], []
        self.y, self.yerr = [], []

        self.initial_P = []
        self.output, self.output_err = [], []

        self.fit_function = None

    def init_function(self, equation_str):
        n_free = equation_str.count("P[")

        self.initial_P = []

        for n in range(0, n_free):
            self.initial_P.append(1)

        self.fit_function = lambda P, x: eval(equation_str)

        self.model = scipy.odr.Model(self.fit_function)

    def set_data(self, x, y, xerr, yerr):
        self.fit_data = scipy.odr.RealData(x, y, sx=xerr, sy=yerr)

    def run(self):
        odr = scipy.odr.ODR(self.fit_data, self.model, beta0=self.initial_P)

        out = odr.run()

        self.output_err = sqrt(diag(out.cov_beta))

        self.output = out.beta
