#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

npoints = 30
noise = np.random.randn(npoints)

x = np.linspace(0, 50, npoints) + noise
xerr = np.random.randn(npoints) + 2
y = 10 + 100 * x - 2 * x*x
yerr = 10 * np.random.randn(npoints) + 10

np.savetxt("accelerated_motion.tsv", np.transpose([x, xerr, y, yerr]), delimiter="\t", fmt='%1.6e')
