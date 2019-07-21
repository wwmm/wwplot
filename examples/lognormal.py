#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

npoints = 10000

mu, sigma = np.log(100), 0.4
x = np.random.lognormal(mu, sigma, npoints)

xerr = np.zeros(npoints)
y = np.zeros(npoints)
yerr = np.zeros(npoints)

np.savetxt("lognormal_distribution.tsv", np.transpose([x, xerr, y, yerr]), delimiter="\t", fmt='%1.6e')
