#!/usr/bin/env python3
import algorithms
import matplotlib.pyplot as plt


def main():
    hmap = algorithms.diamond_square(9, magnitude=25)
    hmap = algorithms.to_image(hmap)
    plt.imshow(hmap)
    plt.show()
    return


if __name__ == '__main__':
    main()
