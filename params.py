
""" Plot Params """

figSize = (8.5, 4.5)                      # figSize in inches
dpi = 200
cosmetics = True                        # Figure will be default matplotlib window if false


""" Simulation Params """

# Time Params
dt = 0.01
startTime, endTime = 0.0, 15.0
factor = 1.0

# Logging
logSim = False


""" Animation Params """

logAnim = False

# Velocity, acceleration vector display
vectorPortionOfScreen = 20.0
minVectorSizeProportion, maxVectorSizeProportion = 0.5, 2.0












""" Calculations """
numFrames = int((endTime - startTime) / dt)