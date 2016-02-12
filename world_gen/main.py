#!/usr/bin/env python3
import algorithms
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def main():
    size_order = 8
    blur_radius = 10  # int(size_order / 2)

    # Create terrain
    hmap = algorithms.diamond_square(8, magnitude=15, wrapping=True)
    # Smooth terrain
    hmap_blurred = algorithms.gaussian_blur_channel(hmap, blur_radius, True)

    # Convert to images
    hmap_image = algorithms.to_image(hmap)
    hmap_blurred_image = algorithms.to_image(hmap_blurred)
    # hmap_image = mpimg.imread('in_01.png')
    # int_image = algorithms.prepare_numpy_image(hmap_image)
    # hmap_blurred_image = algorithms.gaussian_blur_image(int_image, 3, 5)

    # Draw 2D terrain
    plt.imshow(hmap_image)
    plt.draw()
    plt.figure()
    plt.imshow(hmap_blurred_image)

    # Render 3D terrain
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    hmap_x = np.empty((len(hmap), len(hmap)))
    hmap_y = np.empty((len(hmap), len(hmap)))
    hmap_z = np.empty((len(hmap), len(hmap)))
    for x in range(len(hmap)):
        for y in range(len(hmap)):
            hmap_x[x][y] = x
            hmap_y[x][y] = y
            hmap_z[x][y] = hmap[x][y]

    ax.plot_wireframe(hmap_x, hmap_y, hmap_z)
    fig_blurred = plt.figure()
    ax_blurred = fig_blurred.add_subplot(111, projection='3d')
    hmap_blurred_x = np.empty((len(hmap_blurred), len(hmap_blurred)))
    hmap_blurred_y = np.empty((len(hmap_blurred), len(hmap_blurred)))
    hmap_blurred_z = np.empty((len(hmap_blurred), len(hmap_blurred)))
    for x in range(len(hmap_blurred)):
        for y in range(len(hmap_blurred)):
            hmap_blurred_x[x][y] = x
            hmap_blurred_y[x][y] = y
            hmap_blurred_z[x][y] = hmap_blurred[x][y]
    ax_blurred.plot_wireframe(hmap_blurred_x, hmap_blurred_y, hmap_blurred_z)
    plt.show()
    return


if __name__ == '__main__':
    main()
