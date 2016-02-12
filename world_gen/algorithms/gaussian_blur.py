# Implementation of fast Gaussian blur algorithm
# Source: http://blog.ivank.net/fastest-gaussian-blur.html

# import unittest
import math
import numpy as np


def gaussian_blur_image(image, channels, r, rounding=True):
    width = len(image)
    height = len(image[0])
    blurred = np.empty([width, height, channels], dtype=int)
    # Blur each channel and form into a new image
    for channel in range(channels):
        print("Working on channel " + str(channel + 1))
        blurred[:, :, channel] = gaussian_blur_channel(image[:, :, channel], r,
                                                       rounding)
    return blurred


def gaussian_blur_channel(channel, r, rounding=False):
    """ Channel is a 2D numpy array, returns a 2D numpy array, blurred """
    def boxes_for_gauss(sigma, n):
        """sigma is standard deviation, n is number of boxes"""
        w_ideal = math.sqrt((12 * sigma * sigma/n) + 1)
        w_i = math.floor(w_ideal)
        if w_i % 2 == 0:
            w_i -= 1
        wu = w_i + 2

        m_ideal = float((12*sigma*sigma-n*w_i*w_i-4*n*w_i-3*n)/(-4*w_i-4))
        m = round(m_ideal)

        sizes = []
        for i in range(n):
            if i < m:
                sizes.append(w_i)
            else:
                sizes.append(wu)
        return sizes

    def slow_box_blur(in_ch, out_ch, w, h, r):
        for i in range(h):
            for j in range(w):
                val = 0
                for iy in range(i-r, i+r+1):
                    for ix in range(j-r, j+r+1):
                        x = min(w-1, max(0, ix))
                        y = min(h-1, max(0, iy))
                        val += in_ch.flat[y*w+x]
                out_ch.flat[i*w+j] = val/((r+r+1)*(r+r+1))

    def box_blur(in_ch, out_ch, w, h, r, rounding):
        """ in_ch and out_ch are 2D arrays """
        def box_blur_h(in_ch, out_ch, w, h, r, rounding):
            iarr = float(1 / (r+r+1))
            for i in range(h):
                ti = i*w
                li = ti
                ri = ti+r
                fv = in_ch.flat[ti]
                lv = in_ch.flat[ti+w-1]
                val = (r+1) * fv
                for j in range(r):
                    val += in_ch.flat[ti+j]
                for j in range(r+1):
                    val += in_ch.flat[ri] - fv
                    ri += 1
                    if rounding:
                        out_ch.flat[ti] = round(val*iarr)
                    else:
                        out_ch.flat[ti] = (val*iarr)
                    ti += 1
                for j in range(r+1, w-r):
                    val += in_ch.flat[ri] - in_ch.flat[li]
                    ri += 1
                    li += 1
                    if rounding:
                        out_ch.flat[ti] = round(val*iarr)
                    else:
                        out_ch.flat[ti] = (val*iarr)
                    ti += 1
                for j in range(w-r, w):
                    val += lv - in_ch.flat[li]
                    li += 1
                    if rounding:
                        out_ch.flat[ti] = round(val*iarr)
                    else:
                        out_ch.flat[ti] = (val*iarr)
                    ti += 1
            return

        def box_blur_t(in_ch, out_ch, w, h, r, rounding):
            iarr = float(1 / (r+r+1))
            for i in range(w):
                ti = i
                li = ti
                ri = ti+r*w
                fv = in_ch.flat[ti]
                lv = in_ch.flat[ti+w*(h-1)]
                val = (r+1) * fv
                for j in range(r):
                    val += in_ch.flat[ti+j*w]
                for j in range(r+1):
                    val += in_ch.flat[ri] - fv
                    if rounding:
                        out_ch.flat[ti] = round(val*iarr)
                    else:
                        out_ch.flat[ti] = (val*iarr)
                    ri += w
                    ti += w
                for j in range(r+1, h-r):
                    val += in_ch.flat[ri] - in_ch.flat[li]
                    if rounding:
                        out_ch.flat[ti] = round(val*iarr)
                    else:
                        out_ch.flat[ti] = (val*iarr)
                    li += w
                    ri += w
                    ti += w
                for j in range(h-r, h):
                    val += lv - in_ch.flat[li]
                    if rounding:
                        out_ch.flat[ti] = round(val*iarr)
                    else:
                        out_ch.flat[ti] = (val*iarr)
                    li += w
                    ti += w
            return

        np.copyto(out_ch, in_ch)

        box_blur_h(out_ch, in_ch, w, h, r, rounding)
        box_blur_t(in_ch, out_ch, w, h, r, rounding)
        return

    width = len(channel)
    height = len(channel[0])
    channel_cp = np.empty([width, height], dtype=np.float32)
    np.copyto(channel_cp, channel, 'unsafe')
    blurred = np.empty([width, height], dtype=np.float32)

    boxes = boxes_for_gauss(r, 3)
    box_blur(channel_cp, blurred, width, height, int((boxes[0]-1)/2), rounding)
    box_blur(blurred, channel_cp, width, height, int((boxes[1]-1)/2), rounding)
    box_blur(channel_cp, blurred, width, height, int((boxes[2]-1)/2), rounding)
    # box_blur(channel, blurred, width, height, int((boxes[0]-1)/2))
    # box_blur(blurred, channel, width, height, int((boxes[1]-1)/2))
    # box_blur(channel, blurred, width, height, int((boxes[2]-1)/2))
    return blurred


def prepare_numpy_image(image):
    """ Converts numpy image into format used by blur algorithm """
    int_image = np.empty([len(image), len(image[0]),
                          len(image[0, 0])], dtype=int)
    for i in range(len(image.flat)):
        int_image.flat[i] = int(256 - image.flat[i] * 256)
    return int_image
