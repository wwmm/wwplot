# -*- coding: utf-8 -*-

import scipy.odr
from numpy import *
from PySide2.QtCore import QObject, Signal


class Fit(QObject):
    finished = Signal()

    def __init__(self, maxit=100):
        QObject.__init__(self)

        self.maxit = maxit
        self.ready = False

        self.x, self.xerr = [], []
        self.y, self.yerr = [], []

        self.initial_P = []
        self.output, self.output_err = [], []

        self.fit_function = None

        self.myglobals = dict(globals())
        self.myglobals["__builtins__"] = {}

        print(self.myglobals)

    def init_function(self, equation_str):
        self.ready = False

        N = equation_str.count("P[")
        n_free = 0

        for n in range(0, N):
            test_str = "P[" + str(n) + "]"

            if equation_str.count(test_str) > 0:
                n_free = n_free + 1

        self.initial_P = []

        for n in range(0, n_free):
            self.initial_P.append(1)

        self.fit_function = lambda P, x: eval(equation_str, self.myglobals, locals())

        self.model = scipy.odr.Model(self.fit_function)

    def set_data(self, x, y, xerr=None, yerr=None):
        if xerr is not None and yerr is not None:
            self.fit_data = scipy.odr.RealData(x, y, sx=xerr, sy=yerr)
        else:
            self.fit_data = scipy.odr.RealData(x, y)

    def run(self):
        odr = scipy.odr.ODR(self.fit_data, self.model, maxit=self.maxit, beta0=self.initial_P)

        out = odr.run()

        out.pprint()

        self.output_err = sqrt(diag(out.cov_beta))

        self.output = out.beta

        self.ready = True

        self.finished.emit()

        return out.stopreason
