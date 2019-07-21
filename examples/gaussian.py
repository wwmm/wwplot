#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

npoints = 10000

mu, sigma = 100, 15
x = mu + sigma * np.random.randn(npoints)

xerr = np.zeros(npoints)
y = np.zeros(npoints)
yerr = np.zeros(npoints)

np.savetxt("gaussian_distribution.tsv", np.transpose([x, xerr, y, yerr]), delimiter="\t", fmt='%1.6e')
