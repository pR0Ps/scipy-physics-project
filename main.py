#!/usr/bin/env python

from pylab import *
from scipy.integrate import odeint
from scipy.integrate import ode
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

    def state_function(self, dt, s, air=True):
        """Compute and return the next state based on the passed in state and dt"""
        vx = s[2]
        vy = s[3]
        ax = -self.B * math.sqrt(vx**2 + vy**2) * vx
        ay = -self.GRAVITY - self.B * math.sqrt(vx**2 + vy**2) * vy
        return [vx, vy, ax, ay]

    def get_path(self, v, ang):
        """Get the path of the baseball"""
        ang = math.radians(ang)

        # Initial state of the system (x_pos, y_pos, x_vel, y_vel)
        state = [0, 0, v * math.cos(ang), v * math.sin(ang)]

        # dopri5 is equivalent to ode45 in MATLAB
        solver = ode(self.state_function).set_integrator('dopri5')
        solver.set_initial_value(state, 0)

        sol = []

        # Integrate while the ball is above the ground
        while solver.y[1] >= 0:
            solver.integrate(solver.t + 0.1)
            sol.append([solver.y[0], solver.y[1]])

        # Plot the data
        return np.array(sol)

    def find_zero_intercept(self, p1, p2):
        """On the line from p1 to p2, find where it intersects with 0"""
        x1, y1 = p1
        x2, y2 = p2

        x3, y3 = x1, 0
        x4, y4 = x2, 0

        epsilon = 1e-5

        dist = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        # If dist is zero, there is no intersection
        if (dist == 0):
            return None

        # Get the x and y
        pre = (x1 * y2 - y1 * x2)
        post = (x3 * y4 - y3 * x4)
        x = (pre * (x3 - x4) - (x1 - x2) * post) / dist
        y = (pre * (y3 - y4) - (y1 - y2) * post) / dist

        # Check if the x and y coordinates are within both lines
        if (x < min(x1, x2) - epsilon or x > max(x1, x2) + epsilon or x < min(x3, x4) - epsilon or x > max(x3, x4) + epsilon):
            return None
        if (y < min(y1, y2) - epsilon or y > max(y1, y2) + epsilon or y < min(y3, y4) - epsilon or y > max(y3, y4) + epsilon):
            return None

        # Return the point of intersection
        return (x, y)

    def get_best_path(self, vel, ang_step=0.1):
        """Iterate over all angles and find the path with the max distance"""
        curr_max = None
        curr_angle = None
        path = None
        angle = 1
        while angle < 90:
            path = self.get_path(vel, angle)
            if len(path) > 1:
                intercept = self.find_zero_intercept(path[-1], path[-2])[0]
            else:
                intercept = path[-1][0]
            if curr_max is None or intercept > curr_max:
                curr_max = intercept
                curr_angle = angle
            else:
                break

            angle += ang_step


        return curr_angle, curr_max, path

    def finalize_plot(self, plot_, title, x_label, y_label, legend=False):
        """Finalize and show the plot"""

        if legend:
            plot_.legend(*plot_.get_legend_handles_labels())

        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

    def main(self):
        """Run the simulations"""

        pathfig = plt.figure()
        pathplot = pathfig.add_subplot(111)

        angledata = []

        v = 50
        while v < 10000:
            *best, path = self.get_best_path(v)
            angledata.append([v, best[0]])

            print ("Launch vel: {0}, Maximum distance {2:.1f} obtained by launching at angle {1:.2f}".format(v, *best))
            pathplot.plot(path[:,0], path[:,1], '-', label="{0}m/s @ {1:.1f}°".format(v, best[0]))

            v += int(v/2)
            if v > 10000:
                v = 10000

        x1,x2,y1,y2 = pathplot.axis()
        pathplot.axis((0, max(x2, y2), 0, max(x2, y2)))
        self.finalize_plot(pathplot, "Paths of the baseball", "Distance (m)", "Height (m)", legend=False)

        anglefig = plt.figure()
        angleplot = anglefig.add_subplot(111)
        angledata = np.array(angledata)
        angleplot.plot(angledata[:,0], angledata[:,1], '.-',)
        self.finalize_plot(angleplot, "Best launch angle at different velocities", "Velocity (m/s)", "Angle (°)")

        plt.show()

if __name__ == "__main__":
    Project().main()

