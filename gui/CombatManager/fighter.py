#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals

class Fighter(object):
    def __init__(self, name, AP=0, SN=11, GE=11, IN=11):
        self.name = name
        self.AP = AP
        self.SN = SN
        self.GE = GE
        self.IN = IN
        self.acted = False
        self.active = False

    @property
    def priority(self):
        priority = 0
        if self.active :
            priority = -1000000
        elif self.acted :
            priority = +1000000
        return priority - self.AP * 1000 - self.IN

    @property
    def background(self):
        if self.active:
            return 0, 255, 0, 128
        elif self.acted :
            return 196, 196, 196, 128
        else :
            return 0, 128, 0, 64

    @property
    def APGain(self):
        bonus = [-2,-2,-2,-2,-2,-2,-1,-1,0,0,0,1,1,1,1,2,2,2,2,2,3,3,3,3,3,3,4]
        return 3 + bonus[self.SN]

    def __str__(self):
        return self.name