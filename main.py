#!/usr/bin/env python3

import numpy as np
from scipy.integrate import ode
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import warnings

import math


def logistic(t, y, r):
    return r * y * (1.0 - y)

def ode45_test():
    r = .01
    t0 = 0
    y0 = 1e-5
    t1 = 5000.0
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

def get_path(v, ang):
    """Show the path of the baseball"""
    ang = math.radians(ang)
    arr = []
    for t in range(1000):
        ms = t/100
        x_pos = math.cos(ang) * v * ms
        y_pos = math.sin(ang) * v * ms + 0.5 * -9.8 * math.pow(ms, 2)
        arr.append((x_pos, y_pos))
        if (y_pos < 0):
            break

    return np.array(arr)

class Project(object):

    def __init__(self):
        self.GRAVITY = -9.8

        self.BASEBALL_M = 0.145 # Mass (kg)
        self.BASEBALL_CD = 0.2 # Drag coeff 
        self.BASEBALL_P = 1.2 # Air denity @ sea level (kg/m^3)
        self.BASEBALL_RAD = 0.076/2 # Radius (m)
        self.BASEBALL_A = math.pi * self.BASEBALL_RAD ** 2 # Cross-sectional area (m^2)

        # Air resistance
        self.BASEBALL_B = 1/2 * self.BASEBALL_P * self.BASEBALL_CD * self.BASEBALL_A

    def get_path(self, v, ang):
        """Show the path of the baseball"""
        ang = math.radians(ang)
        arr = []
        for t in range(-1000, 1000):
            ms = t/100
            vt = (self.BASEBALL_M * self.GRAVITY)/self.BASEBALL_B

            x_pos = ((v * self.BASEBALL_M)/self.BASEBALL_B) * math.cos(ang) * (1 - math.exp((-self.BASEBALL_B * ms)/self.BASEBALL_M))
            #y_pos = (v * self.BASEBALL_M/self.BASEBALL_B) * math.sin(ang) * (1 - math.exp((-self.BASEBALL_B * t)/(self.BASEBALL_M))) - vt * t
            #y_pos = ((v * vt)/self.GRAVITY) * math.sin(ang) * (1 - math.exp((-self.GRAVITY * t)/(vt))) - (vt * t)
            y_pos = -(self.BASEBALL_M * self.GRAVITY/self.BASEBALL_B) * ms + (self.BASEBALL_M / self.BASEBALL_B) * (v * math.sin(ang) + (self.BASEBALL_M * self.GRAVITY)/self.BASEBALL_B) * (1 - math.exp((-self.BASEBALL_B * ms)/self.BASEBALL_M))
            arr.append((x_pos, y_pos))
            #if (y_pos < 0):
            #    break

        return np.array(arr)


    def show_paths(self, np_arrs):
        for x in np_arrs:
            plt.plot(x[:,0], x[:,1], 'b.-')
    
        plt.show()

    def main(self):
        
        #self.show_paths((self.get_path(10, x) for x in range(1, 90, 10)))
        self.show_paths((self.get_path(10, 45),))

if __name__ == "__main__":
    Project().main()

