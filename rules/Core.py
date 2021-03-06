#!/usr/bin/python
# -*- coding: utf-8
from __future__ import division, print_function

def xpCosts(startValue, targetValue, multiplier):
    costs = targetValue * (targetValue + 1) / 2
    costs -= startValue * (startValue  + 1) / 2
    costs *= multiplier
    return costs