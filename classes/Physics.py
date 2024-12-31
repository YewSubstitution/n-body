import numpy as np

from include.func import get_bounds_of_points, get_scalar_bounds_of_points
from classes.Body import Body

class Physics():

    # Static Variables
    numBodies = 0
    offset = False      # TODO: Implement automatic position offset


    # Constructor
    def __init__(self, *args):
        self.bodies = []            # List containing all bodies
        self.animationList = []     # List containing all animation objects for the bodies
        self.graphList = []         # List containinng all animation objects for the graph

        self.minPos, self.maxPos = [], []
        self.minVel, self.maxVel = 0.0, 0.0
        self.minAcc, self.maxAcc = 0.0, 0.0
        self.screenDiag = 0.0               # Useful data for sizing the screen. Does not work well when one bound is much larger than the other

        for arg in args:
            if type(arg) == Body:
                self.bodies.append(arg)
                Physics.numBodies += 1


    """Mutators"""

    def add_bodies(self, *args):
        """Add bodies to the physics simulation."""

        for arg in args:
            if type(arg) == Body:
                self.bodies.append(arg)
                Physics.numBodies += 1

    def _update(self):
        """"Main loop of Physics class."""

        for body in self.bodies:            # Update force and velocity
            body.update_dv_and_vel(self)
        for body in self.bodies:            # Update position from new velocity
            body.update_pos()

    def run(self, end, log=False, desiredBodies: tuple=()):
        """Run physics simulation until specified frame"""

        if log:
            self.print_in_sim(0, end, desiredBodies)

        for frame in range(0, end):
            self._update()

            if log:
                self.print_in_sim(frame, end, desiredBodies)

            # Once finsished, ascertain the extrema of the simulation
            if frame == end - 1:
                listOfAllPoints = self.get_list_of_all_points()

                self.minPos, self.maxPos = get_bounds_of_points(listOfAllPoints[0])
                self.minVel, self.maxVel = get_scalar_bounds_of_points(listOfAllPoints[1])
                self.minAcc, self.maxAcc = get_scalar_bounds_of_points(listOfAllPoints[2])

                # Calculating screenDiag
                w = self.maxPos[0] - self.minPos[0]
                h = self.maxPos[1] - self.minPos[1]
                self.screenDiag = np.sqrt(w**2 + h**2)

                # TODO: Calculate potential energies for each body


    """Accessors"""

    def get_list_of_all_points(self):
        """Return a list of all points, velocities, and accelerations accessed by all bodies."""

        allPos, allVel, allAcc = [], [], []

        for body in self.bodies:
            for pos in body.posHist:
                allPos.append(pos)
            for vel in body.velHist:
                allVel.append(vel)
            for acc in body.accHist:
                allAcc.append(acc)

        return allPos, allVel, allAcc

    def print_in_sim(self, frame: int, end: int, desiredBodies: tuple=()):
        """In *args, specify a tuple of names to print only the objects with those names."""
        
        # TODO: Figure out a better way to do this. This runs a bunch of times
        listOfPrintableIndices = []

        # If bodies are specified, ascertain indices of desired bodies and print only their details
        if len(desiredBodies) != 0:
            for arg in desiredBodies:
                for body in self.bodies:
                    if arg == body.name:
                        listOfPrintableIndices.append(self.bodies.index(body))
            # Print only details from desired bodies
            print(f"Frame: {frame+1} / {end}")
            for i in listOfPrintableIndices:
                self.bodies[i].print_chars()
            print("-------------------------")

        # If no details are specified, print details of all bodies
        else:
            print(f"Frame: {frame+1} / {end}")
            for body in self.bodies:
                body.print_chars()
            print("-------------------------")

    def print_in_anim(self):
        # TODO: Implement this

        pass

    """Misc Methods"""

    def mp_animation_setup(self, axis):
        """Create the objects used for animation.
        index mod n true:
        for n = 0 (body); for n = 1 (velocity); for n = 2 (trajectory)"""

        for body in self.bodies:
            self.animationList.append(axis.plot([], [], 'o', color=body.color, zorder=5)[0])        # Body object
            self.animationList.append(axis.plot([], [], color=body.color, zorder=3)[0])             # Velocity line
            self.animationList.append(axis.plot([], [], color=(0, 1, 0), zorder=2)[0])              # Accceleration/force line
            self.animationList.append(axis.plot([], [], color=body.color, zorder=1)[0])             # Trajectory curve

            self.graphList.append(axis.plot([], [], color=body.color)[0])                           # Energy graph

    def draw_bodies(self, frame:int, log=False):
        """Iterate through animationList and update the data for each object to resemble the current frame"""

        # TODO: Implement logging in animation (self.print_in_anim)

        # Iterate through all animation objects. If there are n bodies, there will be 3n objects
        for animObj in self.animationList:
            objIndex = self.animationList.index(animObj)

            # Decide which body animation object belongs to
            bodyIndex = -1 # Contains the index of the body for which the current animation object is tied to. Will throw error if not reassigned from -1
            for body in self.bodies:
                bodyIndex = self.bodies.index(body)

                if objIndex in range(4*bodyIndex, 4 * (bodyIndex+1)): # Check if the number is in the interval [4(bodyIndex), 4(bodyIndex+1)] 
                    break

            # Decide whether or not the animation object is a body, velocity, acceleration/force, or trajectory
            isBody, isVel, isAcc, isTraj = False, False, False, False
            if (objIndex % 4 == 0): isBody = True
            elif (objIndex % 4 == 1): isVel = True
            elif (objIndex % 4 == 2): isAcc = True
            elif (objIndex % 4 == 3): isTraj = True

            # Update the object
            if isBody:
                self.animationList[objIndex].set_data(body.draw_body(frame)[0], body.draw_body(frame)[1])
            elif isVel:
                self.animationList[objIndex].set_data(body.draw_vel(frame, self)[0], body.draw_vel(frame, self)[1])
            elif isAcc:
                self.animationList[objIndex].set_data(body.draw_acc(frame, self)[0], body.draw_acc(frame, self)[1])
            elif isTraj:
                self.animationList[objIndex].set_data(body.draw_traj(frame)[0], body.draw_traj(frame)[1])
            else:
                raise ValueError("Animation object cannot be classified")

        return self.animationList

    def draw_graphs(self, frame:int):
        """Draw the graph of the mechanical energy of the system"""
        
        for graphObj in self.graphList:
            body = self.graphList.at(graphObj)

            drawGraph = body._draw_graph(frame)
            self.graphList.at(graphObj).set_data(drawGraph[0], drawGraph[1])

        return self.graphList