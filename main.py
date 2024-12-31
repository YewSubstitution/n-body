import matplotlib.pyplot as plt
import matplotlib.animation as an

from params import *
from include.mpfunc import *

from classes.Body import Body
from classes.Physics import Physics


""" Physics Environment Setup """

physics = Physics()
physics.offset = False
physics.add_bodies(

# Add bodies here
Body(pos=(1.0, 0.0), vel=(0.0, 0.5),
     mass=1e10, radius=10.0,
     name="Sun", color="red", showVel=False, showAcc=True, showTraj=True),
Body(pos=(-1.0, 0.0), vel=(0.0, -0.5),
     mass=1e10, radius=10.0,
     name="Alpha Centauri", color="blue", showVel=False, showAcc=True, showTraj=True),
Body(pos=(1.0, 1.0), vel=(-0.5, 0.0),
     mass=1e10, radius=10.0,
     name="Betelgeuse", color="Green", showVel=False, showAcc=True, showTraj=True),
Body(pos=(-10.0, 1.0), vel=(1.5, 1.5),
     mass=3e11, radius=10.0,
     name="Sag. A*", color="red", showVel=False, showAcc=True, showTraj=True)

)


"""Don't touch this"""
if __name__ == "__main__":

     """ Simulation """

     physics.run(numFrames, log=logSim)


     """ Matplotlib Display Setup """

     fig, ax = plt.subplots(1, 2, figsize=figSize, dpi=dpi)
     display, graph1 = ax

     # Set up axes
     axis_setup(display, minMax=(physics.minPos, physics.maxPos), log=False, cosmetics=cosmetics)
     axis_setup(graph1)


     """ Matplotlib Animation Setup """

     physics.mp_animation_setup(display)

     def anim_func(frame):
          """Looping function for animation in main."""

          animObjs = []

          for object in physics.draw_bodies(frame, log=logAnim):
               animObjs.append(object)

          return animObjs

     animation = an.FuncAnimation(fig, anim_func, frames=numFrames, interval=10, blit=1)

     plt.show()