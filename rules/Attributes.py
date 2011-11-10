#!/usr/bin/python
# -*- coding: utf-8
from __future__ import division, print_function, unicode_literals
from rules.Utils import xpCosts

# Mapping to translate long attribute names to abbreviations
mapping = {
    "Stärke" : "ST",
    "Konstitution" : "KO",
    "Geschick" : "GE",
    "Schnelligkeit" : "SN",
    "Intelligenz" : "IQ",
    "Intuition" : "IN",
    "Willenskraft" : "WK",
    "Charisma" : "CH"
}

# Default attributes + default values
attributes = {
    "ST" : 8,
    "KO" : 8,
    "GE" : 8,
    "SN" : 8,
    "WK" : 8,
    "IN" : 8,
    "IQ" : 8,
    "CH" : 8
}

# the XP cost multiplier to raise attributes
attributeXPMultiplier = 5


class Attributes(object):
    def __init__(self):
        self.baseValues = dict(attributes)
        self.mods = []

    def __getitem__(self, item):
        """
        Return the value of an attribute concerning all modifications.
        """
        return self.baseValues[item] + self.getModification(item)

    def __setitem__(self, key, value):
        """
        Set the baseValue of given attribute.
        """
        self.baseValues.__setitem__(key, value)

    def __iter__(self):
        return self.baseValues.items().__iter__()

    def addModDict(self, mod):
        """
        Add an attribute modification as a dictionary mapping attribute names to modification values.
        """
        self.mods.append(mod)

    def getXPCosts(self, att = None):
        """
        Return the XP costs of raising the given attribute from the default value to the current level,
        or the total costs if no attribute is given.
        """
        if att is None :
            costs = 0
            for att in self.baseValues.keys():
                costs += self.getXPCosts(att)
            return costs
        else :
            return xpCosts(attributes[att], self.baseValues[att], attributeXPMultiplier)

    def getModifier(self, att):
        """
        Return the attribute modifier, i.e. the difficulty modifier applied to skill rolls.
        """
        return (1000,4,3,3,2,2,1,1, 0,0,0, -1,-1,-1,-1, -2,-2,-2,-2,-2, -3)[self[att]]

    def getModification(self, att):
        """
        Return the modifications for a given attribute due to race, vantages, and so on.
        """
        mod = 0
        for m in self.mods :
            if att in m:
                mod += m[att]
        return mod


