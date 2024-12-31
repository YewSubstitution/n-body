import numpy as np
from scipy.constants import G

import params
from include.func import parse_color_to_RGB, mag, unit_vector, linear_map

class Body:
    
    # Constructor
    def __init__(self, pos: tuple=(0.0, 0.0), vel: tuple=(0.0, 0.0),
                 mass: float=10.0, radius: float=10.0,
                 name: str="noName", color: str="red",
                 showVel: bool=False, showAcc: bool=False, showTraj: bool=False):
        
        self.pos, self.vel = np.array((pos[0], pos[1]), dtype=float), np.array((vel[0], vel[1]), dtype=float)
        self.mass, self.radius = mass, radius
        self.name, self.color = name, parse_color_to_RGB(color)
        self.showVel, self.showAcc, self.showTraj = showVel, showAcc, showTraj

        self.dv = np.zeros(2, dtype=float) # Change in velocity
        self.posHist, self.velHist, self.accHist = [], [], [] # Historical vectors of the body for animation purposes


    """ Mutators """

    def _update_dv(self, physics):
        """Updates dv of self given physics class containing list of other bodies. Where most of my problems lie."""

        F_intermediate = np.zeros(2, dtype=float)

        for body in physics.bodies:

            if (self != body): # Check if body is not self
                r_ji = self.pos - body.pos

                F_intermediate += (body.mass / mag(r_ji)**2) * unit_vector(r_ji) # (m_j / r^2) * r_ij

        self.dv = params.factor * -G * F_intermediate * params.dt 

    def _update_vel(self):
        """Adds to self velocity dv"""

        self.vel += self.dv
    
    def update_dv_and_vel(self, physics):
        """Wraps _update_dv() and _update_vel() for ease of use in Physics class."""

        self._update_dv(physics)
        self._update_vel()

    def update_pos(self):
        """Update the position of the body according to self velocity."""

        self.posHist.append([float(self.pos[0]), float(self.pos[1])])
        self.velHist.append([float(self.vel[0]), float(self.vel[1])])
        self.accHist.append([float(self.dv[0]/params.dt), float(self.dv[1]/params.dt)]) # a = dv / dt

        self.pos += self.vel * params.dt


    """ Accessors """

    def print_chars(self):
        """Print in simulation"""

        print('- ' + self.name)
        print(f"\tPos: {self.pos[0]:.4f}, {self.pos[1]:.4f}\tVel: {self.vel[0]:.4f}, {self.vel[1]:.4f}\tdV:{self.dv[0]:.15f}, {self.dv[1]:.15f}")

    
    """ Misc. Methods """

    def draw_body(self, frame:int):
        """Return the coordinates of the body given a frame."""

        return [self.posHist[frame][0]], [self.posHist[frame][1]]
    
    def draw_vel(self, frame: int, physics):
        """Return the coordinates of the body's velocity vector."""
        # TODO: Fix this. It is buggy, the vectors are too long

        if not self.showVel:
            return [0, 0], [0, 0]
        
        currPos = self.posHist[frame]
        currVel = self.velHist[frame]
        
        intVector = np.array((currVel[0], currVel[1]), dtype=float)
        intVector = (physics.screenDiag / params.vectorPortionOfScreen) * unit_vector(intVector)


        # Determine how large to display vector based on min and max velocity
        scaleFactor = linear_map(mag(currVel), (physics.minVel, physics.maxVel), (params.minVectorSizeProportion, params.maxVectorSizeProportion))

        velVecX, velVecY = [currPos[0], currPos[0] + scaleFactor * intVector[0]], [currPos[1], currPos[1] + scaleFactor * intVector[1]]

        return velVecX, velVecY

    def draw_acc(self, frame: int, physics):

        if not self.showAcc:
            return [0, 0], [0, 0]

        currPos = self.posHist[frame]
        currAcc = self.accHist[frame]
        
        intVector = np.array((currAcc[0], currAcc[1]), dtype=float)
        intVector = (physics.screenDiag / params.vectorPortionOfScreen) * unit_vector(intVector)

        # Determine how large to display vector based on min and max acceleration
        scaleFactor = linear_map(mag(currAcc), (physics.minAcc, physics.maxAcc), (params.minVectorSizeProportion, params.maxVectorSizeProportion))

        accVecX, accVecY = [currPos[0], currPos[0] + scaleFactor * intVector[0]], [currPos[1], currPos[1] + scaleFactor * intVector[1]]

        return accVecX, accVecY

    def draw_traj(self, frame):
        xBeforeFrame, yBeforeFrame = [], []

        if not self.showTraj:
            return [0, 0], [0, 0]

        posBeforeFrame = self.posHist[:frame]

        for point in posBeforeFrame:
            xBeforeFrame.append(point[0])
            yBeforeFrame.append(point[1]) 

        # Bad way to do this. Remakes list on every frame.
        
        return xBeforeFrame, yBeforeFrame
    
    def draw_graph(self, frame):
        """Draws a graph of kinetic and potential energy in the system"""
        

        # TODO: Potential energy

        pass