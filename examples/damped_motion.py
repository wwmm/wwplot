#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

npoints = 100
noise = np.random.randn(npoints)

x = np.linspace(0, 50, npoints)
xerr = 0.1 * (np.random.randn(npoints) + 2)
y = 10 * np.exp(-0.1 * x) * np.cos(2 * np.pi * 10 * x)
yerr = 0.1 * (np.random.randn(npoints) + 2)

np.savetxt("damped_motion.tsv", np.transpose([x, xerr, y, yerr]), delimiter="\t", fmt='%1.6e')
