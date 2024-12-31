import numpy as np


""" Vector Functions """

def mag(vector):
    """Return the magnitude of numpy 2-array."""
    mag = -1

    if (type(vector) == np.ndarray):
        mag = np.sqrt(vector.dot(vector))
    if ((type(vector) == list) or (type(vector) == tuple)):
        mag = np.sqrt(vector[0]**2 + vector[1]**2)

    return mag

# Smallest allowed magnitude
def unit_vector(vector: np.array, EPSILON=1e-5):
    """Return the unit vector of vector. If the magnitude of vector is less than EPSILON, return the zero vector"""
    
    unitVector = np.zeros(2, dtype=float)
    
    vmag = mag(vector)

    if (vmag > EPSILON):
        unitVector = vector / vmag

    return unitVector


""" Accessory Functions for Body """

def parse_color_to_RGB(colorStr: str):
    """Turn informal strings holding the name of a color into rgb"""
    
    colorStr = colorStr.lower()

    colorRGB = (1, 0, 0) # Red by default
    if colorStr == "green": colorRGB = (0, 1, 0)
    if colorStr == "blue": colorRGB = (0, 0, 1)
    # TODO: Add more colors
    
    return colorRGB

""" Accessory Functions for Physics """

def get_bounds_of_points(points):
    """Returns two tuples containing the smallest and largest points in the list of all points accessed"""

    min_x, max_x = 0.0, 0.0
    min_y, max_y = 0.0, 0.0

    if len(points) == 0:
        return max_x, max_y
    
    for point in points:
        if points.index(point) == 0:
            min_x, max_x = point[0], point[0]
            min_y, max_y = point[1], point[1]

        # Assign minimums
        if point[0] < min_x:
            min_x = point[0]
        if point[1] < min_y:
            min_y = point[1]

        # Assign maximums
        if point[0] > max_x:
            max_x = point[0]
        if point[1] > max_y:
            max_y = point[1]

    return (min_x, min_y), (max_x, max_y)

def get_scalar_bounds_of_points(points):
    """Returns two floats containing the smallest and largest magnitudes in the list of all points accessed"""

    min, max = 0.0, 0.0

    for point in points:
        if points.index(point) == 0:
            min = mag(point)
            max = mag(point)
        
        if mag(point) < min:
            min = mag(point)

        if mag(point) > max:
            max = mag(point)

    return min, max


""" Misc Math"""

def linear_map(x, firstInterval: tuple=(0, 1), secondInterval: tuple=(0, 100)):
    """A simple linear map from interval [a, b] to interval [c, d]"""

    num = (x - firstInterval[0]) * (secondInterval[1] - secondInterval[0])
    denum = firstInterval[1] - firstInterval[0]
    frac = num / denum

    return secondInterval[0] + frac


""" Debug """

if __name__ == "__main__":
    v1 = np.array((5, 3), dtype=float)
    v2 = np.array((0, 0), dtype=float)

    print(type(v1))

    print(unit_vector(v1 - v2))