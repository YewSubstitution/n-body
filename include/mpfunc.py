import matplotlib.pyplot as plt
import matplotlib.animation as an

""" Plot Setup """

def axis_setup(ax, minMax=([-10.0, -10.0], [10.0, 10.0]), cosmetics=False, log=False):
    """Mutate given figure and axis to given attributes.
     
    Args:
    fig::matplotlib.pyplot.figure
    ax::matplotlib.pyplot.axis
    minMax::2-tuple - (min(minx, miny), max(maxx, maxy)),
    inches::2-tuple
    dpi::int
    """

    min, max = list(minMax[0]), list(minMax[1])
    xDist, yDist = abs(max[0] - min[0]), abs(max[1] - min[1])


    if log: print(f"\nModifying axes...\nx: [{min[0]:.2f}, {max[0]:.2f}]\ty: [{min[1]:.2f}, {max[1]:.2f}]")

    if (xDist < 1.0):                # If x bounds too small,
        max[0] = min[0] + 0.5                       # Set the x bounds to be centered on the minimum value
        min[0] = min[0] - 0.5
        if log: print(f"x bounds too small. \tNew bounds: \tx: [{min[0]:.2f}, {max[0]:.2f}]")
    if (yDist < 1.0):                # If the y bounds are too small,
        max[1] = min[1] + 0.5                       # Set the y bounds to be centered on the minimum value
        min[1] = min[1] - 0.5
        if log: print(f"y bounds too small. \tNew bounds: \ty: [{min[1]:.2f}, {max[1]:.2f}]")

    ax.set_xlim(min[0] - xDist * 0.10, max[0] + xDist * 0.10)
    ax.set_ylim(min[1] - yDist * 0.10, max[1] + yDist * 0.10)

    # Cosmetics:
    if cosmetics:
        ax.set_facecolor("black")


""" Matplotlib Animation """
