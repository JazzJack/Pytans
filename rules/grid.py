#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
from math import sqrt

sqrt_3 = sqrt(3)


def getCenter(row, col, radius = 1):
    x = (2*col + row) * radius
    y = sqrt_3 * row * radius
    return x, y

def getCornersClockwise(x, y, radius = 1):
    upper      = (x         , y + 2 / sqrt_3 * radius)
    upperRight = (x + radius, y + 1 / sqrt_3 * radius)
    lowerRight = (x + radius, y - 1 / sqrt_3 * radius)
    lower      = (x         , y - 2 / sqrt_3 * radius)
    lowerLeft  = (x - radius, y - 1 / sqrt_3 * radius)
    upperLeft  = (x - radius, y + 1 / sqrt_3 * radius)
    return [upper, upperRight, lowerRight, lower, lowerLeft, upperLeft]


import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import matplotlib.patches as mpatches



fig = plt.figure(figsize=(10,10))
ax = plt.axes([0,0,1,1])

patches = []
for r in range(10):
    for c in range(10):
        hexagon = mpatches.RegularPolygon(getCenter(r,c,radius=0.1), 6, 0.2/sqrt_3)
        patches.append(hexagon)

collection = PatchCollection(patches, facecolors="w")
ax.add_collection(collection)


playerPositions = []
circle = mpatches.Circle((0,0), 0.1)
collection2 = PatchCollection([circle], facecolors="g")
ax.add_collection(collection2)

plt.show()
