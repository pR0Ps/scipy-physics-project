#!/usr/bin/env python

from pylab import *
from scipy.integrate import odeint
import math

class Project(object):

    def __init__(self):
        self.GRAVITY = 9.8

        self.M = 0.145 # Mass (kg)
        self.CD = 0.2 # Drag coeff
        self.P = 1.2 # Air denity @ sea level (kg/m^3)
        self.RAD = 0.076/2 # Radius (m)
        self.A = math.pi * self.RAD**2 # Cross-sectional area (m^2)

        # Air resistance
        self.B = (1/2) * self.P * self.CD * self.A

    def state_function(self, s, dt):
        """Compute and return the next state based on the passed in state and dt"""
        vx = s[2] * dt
        vy = s[3] * dt
        ax = -self.B/self.M * math.sqrt(vx**2 + vy**2) * vx * dt
        ay = -self.GRAVITY - self.B/self.M * math.sqrt(vx**2 + vy**2) * vy * dt
        return [vx, vy, ax, ay]

    def get_path(self, v, ang):
        """Get the path of the baseball"""
        ang = math.radians(ang)

        # Initial state of the system (x_pos, y_pos, x_vel, y_vel)
        state = [0, 0, v * math.cos(ang), v * math.sin(ang)]

        # Make a list of times (start at 0, step by 0.05, end at 3 sec)
        # arange instead of range so floating points can be used
        t = arange(0, 3, 0.05)

        # Return the data from the integral
        return odeint(self.state_function, state, t)

    def show_paths(self, np_arrs):
        """Draw the passed in plots"""

        subplot = plt.subplot();

        arrs = list(np_arrs)

        plots = []
        for x in range(len(arrs)):
            plots.append(subplot.plot(arrs[x][:,0], arrs[x][:,1], '-', label=str(x)))

        handles, legends = subplot.get_legend_handles_labels()

        plt.legend(handles, legends)

        plt.title('Path of Baseball')
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')
        plt.show()

    def main(self):
        """Run the simulations"""

        self.show_paths((self.get_path(10, x) for x in range(1, 90, 10)))

if __name__ == "__main__":
    Project().main()

