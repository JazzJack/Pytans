#!/usr/bin/python
# -*- coding: utf-8
from __future__ import division, print_function, unicode_literals
from rules.Dicing import roll, getNumberOfSuccesses
import xml.etree.ElementTree as ElementTree
from rules.Utils import none2Empty


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
    def __init__(self, name, actionPoints = "0", baseDifficulty = "0", impetus = "0", pool = "0", level = 0, options = None):
        self.name = name
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
            variables["WT"] = char.getPoolSize(weapon["Waffentalent"])
            variables.update(weapon.getVarDict(char.attributes))
        variables.update(char.attributes)
        variables.update(char.getSkillsDict())
        return variables

    def roll(self, char, weapon, options = None):
        variables = self.createVarDict(char, weapon, options)
        difficulty = eval(self.baseDifficulty, variables) + weapon.handling
        pool = eval(self.pool, variables)
        r = roll(pool)
        return getNumberOfSuccesses(r, difficulty)

    def validateOptions(self, options):
        # todo
        pass

    def getDamage(self, character, weapon, options, successes):
        variables = self.createVarDict(character, weapon, options)
        impetus = eval(self.impetus, variables)
        if self.level >= 2 :
            impetus += successes * 2
        return impetus

    def getActionPoints(self, character, weapon, options):
        variables = self.createVarDict(character, weapon, options)
        AP = eval(self.actionPoints, variables)
        if variables["leicht"] :
            AP -= 1
        if variables["schwer"] :
            AP += 1
        if self.level >= 3 :
            AP -= 1
        return AP


def readManeuverFromXElement(xManeuvers):
    maneuvers = {}
    for xManeuver in none2Empty(xManeuvers.findall("Manöver")):
        # get name action points and base difficulty
        maneuverName = xManeuver.get("id")
        AP = xManeuver.get("AP")
        baseDiff = xManeuver.get("GS")
        maneuver = Maneuver(maneuverName, actionPoints=AP, baseDifficulty=baseDiff)
        # get Pool
        xPool = xManeuver.find("Pool")
        if xPool is not None :
            maneuver.pool = xPool.text
        # get impetus
        xImpetus = xManeuver.find("Wucht")
        if xImpetus is not None :
            maneuver.impetus = xImpetus.text
        # todo get options
        maneuvers[maneuverName] = maneuver
    return maneuvers

def readManeuversFromXML(filename):
    tree = ElementTree.parse(filename)
    xManeuvers= tree.getroot()
    actions = readManeuverFromXElement(xManeuvers.find("Aktionen"))
    reactions = readManeuverFromXElement(xManeuvers.find("Reaktionen"))
    return actions, reactions
