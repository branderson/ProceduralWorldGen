import unittest
import numpy as np
from numpy import random as rand


def diamond_square(n, seed=None, magnitude=16, wrapping=False):
    """Takes a seed and a value n and returns a heightmap of size 2^n+1"""

    # Diamond step
    def diamond_step(square, magnitude, distance):
        """Takes a square of a 2D array and performs the diamond step on it"""

        # Check if we center already set, otherwise fire off in 4 quadrants
        if square[get_center(square)].val is not None:
            diamond_step(square[0:distance + 1, 0:distance + 1],
                         magnitude, distance // 2)
            diamond_step(square[0:distance + 1, distance:len(square) + 1],
                         magnitude, distance // 2)
            diamond_step(square[distance:len(square) + 1, 0:distance + 1],
                         magnitude, distance // 2)
            diamond_step(square[distance:len(square) + 1,
                         distance:len(square) + 1], magnitude, distance // 2)

        # Take average of corner values
        corner_sum = 0
        for corner in get_corners(square):
            corner_sum += square[corner].val
        corner_avg = corner_sum // 4
        center = get_center(square)

        # Set center to corner average +- random value
        square[center].set_val(corner_avg +
                               rand.randint(-magnitude, magnitude + 1))

    # Square step
    def square_step(square, magnitude, distance):
        """Takes a square of a 2D array and peforms the square step on it"""

        # Get averages between adjacent corners
        corners = get_corners(square)

        # Find midpoint locations
        north_mid = square[(corners[2][0] // 2, 0)]
        south_mid = square[(corners[3][0] // 2, corners[3][1])]
        east_mid = square[(corners[2][0], corners[3][1] // 2)]
        west_mid = square[(0, corners[1][1] // 2)]

        # Check if we've done this level and fire off in quadrants if not
        if (north_mid.val is not None and south_mid.val is not None
                and east_mid.val is not None and west_mid.val is not None):
            square_step(square[0:distance + 1, 0:distance + 1],
                        magnitude, distance // 2)
            square_step(square[0:distance + 1, distance:len(square) + 1],
                        magnitude, distance // 2)
            square_step(square[distance:len(square) + 1, 0:distance + 1],
                        magnitude, distance // 2)
            square_step(square[distance:len(square) + 1,
                        distance:len(square) + 1], magnitude, distance // 2)

        # For each midpoint get average of "adjacent" points
        # North
        north_east = get_adjacent(north_mid, 0, distance)
        north_north = get_adjacent(north_mid, 1, distance)
        north_west = get_adjacent(north_mid, 2, distance)
        north_south = get_adjacent(north_mid, 3, distance)
        # East
        east_east = get_adjacent(east_mid, 0, distance)
        east_north = get_adjacent(east_mid, 1, distance)
        east_west = get_adjacent(east_mid, 2, distance)
        east_south = get_adjacent(east_mid, 3, distance)
        # South
        south_east = get_adjacent(south_mid, 0, distance)
        south_north = get_adjacent(south_mid, 1, distance)
        south_west = get_adjacent(south_mid, 2, distance)
        south_south = get_adjacent(south_mid, 3, distance)
        # West
        west_east = get_adjacent(south_mid, 0, distance)
        west_north = get_adjacent(south_mid, 1, distance)
        west_west = get_adjacent(south_mid, 2, distance)
        west_south = get_adjacent(south_mid, 3, distance)

        node_count = 4
        if north_mid.edge:
            node_count = 3
        north_avg = ((north_east.val + north_north.val +
                      north_west.val + north_south.val) // node_count)
        node_count = 4
        if east_mid.edge:
            node_count = 3
        east_avg = ((east_east.val + east_north.val +
                     east_west.val + east_south.val) // node_count)
        node_count = 4
        if south_mid.edge:
            node_count = 3
        south_avg = ((south_east.val + south_north.val +
                      south_west.val + south_south.val) // node_count)
        node_count = 4
        if west_mid.edge:
            node_count = 3
        west_avg = ((west_east.val + west_north.val +
                     west_west.val + west_south.val) // node_count)

        # Set midpoints to averages +- random value
        north_mid.set_val(north_avg + rand.randint(-magnitude, magnitude + 1))
        south_mid.set_val(south_avg + rand.randint(-magnitude, magnitude + 1))
        east_mid.set_val(east_avg + rand.randint(-magnitude, magnitude + 1))
        west_mid.set_val(west_avg + rand.randint(-magnitude, magnitude + 1))
        # north_mid.set_val(north_avg + rand.randint(0, magnitude + 1))
        # south_mid.set_val(south_avg + rand.randint(0, magnitude + 1))
        # east_mid.set_val(east_avg + rand.randint(0, magnitude + 1))
        # west_mid.set_val(west_avg + rand.randint(0, magnitude + 1))

        return

    # Test inputs
    assert isinstance(n, int), "n is not an integer: %r" % n
    assert n > 0, "n must be > 0: %r" % n

    # Set the seed for the RNG
    if seed is None:
        # Set seed to any value between 0 and max seed value
        seed = rand.randint(0, 4294967295)
    rand.seed(seed)
    width = pow(2, n) + 1  # Size of square
    hmap = np.empty([width, width], dtype=Node)  # 2D array of the heightmap

    print("Generating heightmap of size " + str(width) + " x " + str(width)
          + " using seed " + str(seed))

    # Build nodes
    for x in range(len(hmap)):
        for y in range(len(hmap)):
            hmap[x, y] = Node()
            hmap[x, y].x = x
            hmap[x, y].y = y
    # Build node connections
    for x in range(width):
        for y in range(width):
            node = hmap[x, y]
            # Check if node is an edge node or not and set adjacent to wrap
            # if wrapping is enabled otherwise make fake nodes
            if x == 0:
                if wrapping:
                    node.left = hmap[width - 2, y]
                else:
                    node.left = Node()
                    node.left.fake = True
                    node.edge = True
            else:
                node.left = hmap[x - 1, y]
            if x == width - 1:
                if wrapping:
                    node.right = hmap[1, y]
                else:
                    node.right = Node()
                    node.right.fake = True
                    node.edge = True
            else:
                node.right = hmap[x + 1, y]
            if y == 0:
                if wrapping:
                    node.up = hmap[x, width - 2]
                else:
                    node.up = Node()
                    node.up.fake = True
                    node.edge = True
            else:
                node.up = hmap[x, y - 1]
            if y == width - 1:
                if wrapping:
                    node.down = hmap[x, 1]
                else:
                    node.down = Node()
                    node.down.fake = True
                    node.edge = True
            else:
                node.down = hmap[x, y + 1]

    # Set corners to random values
    corners = get_corners(hmap)
    for corner in corners:
        # hmap[corner].set_val(rand.randint(0, 256))
        hmap[corner].set_val(rand.randint(64, 192))
    # Wrap
    # hmap[corners[1]] = hmap[corners[3]]
    # hmap[corners[0]] = hmap[corners[2]]

    distance = width // 2
    step_size = distance

    while step_size >= 1:
        # if step_size == 1:
        #     magnitude = 0
        print("Working on squares of size: " + str(step_size))
        print("\tMagnitude: " + str(magnitude))
        diamond_step(hmap, magnitude, distance)
        square_step(hmap, magnitude, distance)
        magnitude *= .9
        # Decrease magnitude
        # magnitude = int(magnitude * ((1.5*distance + step_size)
        #                          / (1.5*distance + distance))) + 1
        step_size = step_size // 2

    # Convert hmap from Nodes to ints
    intmap = np.empty([width, width], dtype=int)
    for x in range(len(hmap)):
        for y in range(len(hmap)):
            assert hmap[x, y].val is not None, "(" + str(x) + \
                ", " + str(y) + ") has no value"
            intmap[x, y] = hmap[x, y].val

    return intmap


class TestDiamondSquare(unittest.TestCase):

    def test_zero(self):
        with self.assertRaises(AssertionError):
            diamond_square(0)

    def test_not_int(self):
        with self.assertRaises(AssertionError):
            diamond_square(1.5)


def get_corners(arr):
    """Takes a 2D array and returns a list of the indices of its corners in
        order of top-left, bottom-left, top-right, bottom-right"""

    width = len(arr) - 1
    corners = []
    corners.append((0, 0))
    corners.append((0, width))
    corners.append((width, 0))
    corners.append((width, width))
    return corners


def get_center(arr):
    """Takes a 2D array and returns a tuple of the index of its center"""

    width = len(arr)
    # Make sure a center exists
    assert width % 2 == 1, "array has no midpoint. size is %r" % width
    # Find center index
    center = width // 2
    return (center, center)


def get_adjacent(point, dir, distance):
    """Find node distance away from point in direction dir"""
    cur_point = point
    for step in range(distance):
        cur_point = cur_point.get_adjacent(dir)
        # Fake edge nodes when not wrapping should return 0
        if cur_point.fake:
            temp_node = Node()
            temp_node.val = 0
            return temp_node
    return cur_point


def to_image(arr):
    """Takes a 2D array of values and returns a 2D array of arrays of
        3 equal float32s"""

    width = len(arr)
    img = np.empty([width, width, 3], dtype=np.float32)
    for x in range(width):
        for y in range(width):
            img[x, y, :] = arr[x, y]
    return img


class Node():
    """Graph node with references to adjacent points"""

    def __init__(self):
        self.fake = False
        self.up = None
        self.down = None
        self.right = None
        self.left = None
        self.x = 0
        self.y = 0
        self.edge = False
        self.val = None
        return

    def set_val(self, val):
        self.val = val
        if self.val < 0:
            self.val = 0
        if self.val > 255:
            self.val = 255

    def set_adjacent(self, dir, other):
        assert isinstance(other, Node), "must pass in an object of type Node"
        if dir == 0:
            self.right = other
        elif dir == 1:
            self.up = other
        elif dir == 2:
            self.left = other
        elif dir == 3:
            self.down = other
        else:
            raise ValueError("dir has an illegal value. dir is %r" % dir)

    def get_adjacent(self, dir):
        if dir == 0:
            return self.right
        elif dir == 1:
            return self.up
        elif dir == 2:
            return self.left
        elif dir == 3:
            return self.down
        else:
            raise ValueError("dir has an illegal value. dir is %r" % dir)


if __name__ == "__main__":
    unittest.main()
