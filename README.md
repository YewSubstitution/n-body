# n-Body Problem Simulation Constructed in Python 3 (with numpy, matplotlib)

## A small-scope simulation of central-force (gravity) interactions between n bodies (represented by points) in space

Adjust necessary paramters held in params.py, add bodies in main.py and run the script.

This simulation utilizes two fundamental classes:

* Body: Holds values for the position, velocity, and change in velocity of a body as well as characteristics relating to the drawing of these bodies to the matplotlib figure.
* Physics: Effectively a wrapper for a list of bodies with built-in methods for handling the calculation of the force between bodies and their trajectories. Handles drawing bodies and other indicators within the matplotlib figure.