#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

npoints = 10
noise = 2 * np.random.randn(npoints)

x = np.linspace(0, 50, npoints) + noise
xerr = np.random.randn(npoints) + 2
y = 10 * x + noise
yerr = 5 * (np.random.randn(npoints) + 2)

np.savetxt("uniform_motion.tsv", np.transpose([x, xerr, y, yerr]), delimiter="\t", fmt='%1.6e')
