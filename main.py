#!/usr/bin/env python3

import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt
import warnings


# Some sample functions and values
def logistic(t, y, r):
    return r * y * (1.0 - y)

r = .01
t0 = 0
y0 = 1e-5
t1 = 5000.0

# dopri5 is equivalent to ode45 in MATLAB
solver = ode(logistic).set_integrator('dopri5', nsteps=1)
solver.set_initial_value(y0, t0).set_f_params(r)

# Suppress warnings
solver._integrator.iwork[2] = -1
warnings.filterwarnings("ignore", category=UserWarning)

sol = []

# Integrate until t1
while solver.t < t1:
    solver.integrate(t1, step=True)
    sol.append([solver.t, solver.y])

# Set warnings back on
warnings.resetwarnings()

# Plot the data
sol = np.array(sol)
plt.plot(sol[:,0], sol[:,1], 'b.-')
plt.show()
