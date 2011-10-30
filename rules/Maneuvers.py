#!/usr/bin/python
# -*- coding: utf-8
from __future__ import division, print_function


def createValueDict(character):
    """
    Creates a dictionary of all integer/float/bool attributes of a given object and maps them to their values.
    """
    valDict = {}
    for att in dir(character):
        f = character.__getattribute__(att)
        if type(f) in [int, float, bool] :
            valDict[att] = f
    return valDict

class Maneuver(object):
    def __init__(self, actionPoints = 5, baseDifficulty = 8, impetus = "ST + WW", level = 0):
        self.level = level
        self._baseDifficulty = baseDifficulty
        self._actionPoints = actionPoints
        self.impetus = impetus

    def getImpetus(self, character, weapon, impetusSuccesses):
        values = createValueDict(character)
        values.update(createValueDict(weapon))
        impetus = eval(self.impetus, values)
        if self.level >= 2 :
            impetus += impetusSuccesses * 2
        return impetus

    @property
    def baseDifficulty(self):
        if self.level < 1 :
            return self._baseDifficulty
        else:
            return self._baseDifficulty - 1

    @baseDifficulty.setter
    def baseDifficulty(self, bd):
        self._baseDifficulty = bd

    @property
    def AP(self):
        if self.level < 3:
            return self._actionPoints
        else :
            return self._actionPoints - 1


Hieb = Maneuver(6, 6)
Hieb1 = Maneuver(6, 6, level = 1)
Hieb2 = Maneuver(6, 6, level = 2)
Hieb3 = Maneuver(6, 6, level = 3)

Stich = Maneuver(baseDifficulty=7, impetus="ST")
Stich1 = Maneuver(baseDifficulty=7, impetus="ST", level = 1)
Stich2 = Maneuver(baseDifficulty=7, impetus="ST", level = 2)
Stich3 = Maneuver(baseDifficulty=7, impetus="ST", level = 3)