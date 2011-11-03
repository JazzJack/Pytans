#!/usr/bin/python
# -*- coding: utf-8
from __future__ import division, print_function
from rules.Dicing import roll, getNumberOfSuccesses
from rules.Weapons import weaponAttributes


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
    def __init__(self, actionPoints = "0", baseDifficulty = "0", impetus = "0", pool = "0", level = 0, options = None):
        self.level = level
        self.baseDifficulty = baseDifficulty
        self.actionPoints = actionPoints
        self.impetus = impetus
        self.pool = pool
        self.options = options

    def createVarDict(self, char, weapon, options = None):
        variables = {}
        if options is not None:
            self.validateOptions(options)
            variables.update(options)
        if weapon is not None:
            variables["WT"] = char.getPoolSize(weapon.weaponSkill)
            variables.update(weapon.getVarDict(char))
        variables.update(char.attributes)
        variables.update(char.getSkillsDict())

    def roll(self, char, weapon, options = None):
        variables = self.createVarDict(char, weapon, options)
        difficulty = eval(self.baseDifficulty, variables) + weapon.handling
        pool = eval(self.pool, variables)
        r = roll(pool)
        return getNumberOfSuccesses(r, difficulty)

    def validateOptions(self, options):
        pass

    def getDamage(self, character, weapon, options, successes):
        variables = self.createVarDict(character, weapon, options)

        impetus = eval(self.impetus, variables)
        if self.level >= 2 :
            impetus += impetusSuccesses * 2
        return impetus

    @property
    def difficulty(self):
        if self.level < 1 :
            return self._baseDifficulty
        else:
            return self._baseDifficulty - 1

    @difficulty.setter
    def difficulty(self, bd):
        self._baseDifficulty = bd

    @property
    def AP(self):
        if self.level < 3:
            return self._actionPoints
        else :
            return self._actionPoints - 1

