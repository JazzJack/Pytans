#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals


class Fighter(object):
    def __init__(self, name, AP, SN):
        self.name = name
        self.AP = AP
        self.SN = SN
        self.IN = 10
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


    def gainAP(self):
        bonus = [-2,-2,-2,-2,-2,-2,-1,-1,0,0,0,1,1,1,1,2,2,2,2,2,3,3,3,3,3,3,4]
        self.AP += 3 + bonus[self.SN]

    def endTurn(self):
        self.acted = False
        self.waited = False

    def wait(self, duration):
        self.AP -= duration
        self.waited = True

    def act(self, duration):
        self.AP -= duration
        self.acted = True

    def __str__(self):
        return self.name