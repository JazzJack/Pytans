#!/usr/bin/python
# -*- coding: utf-8
from __future__ import division, print_function

mapping = {
    u"Stärke" : "ST",
    u"Konstitution" : "KO",
    u"Geschick" : "GE",
    u"Schnelligkeit" : "SN",
    u"Intelligenz" : "IQ",
    u"Intuition" : "IN",
    u"Willenskraft" : "WK",
    u"Charisma" : "CH"
}

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

class Attributes(dict):
    def __init__(self, **kwargs):
        dict.__init__(self, attributes, **kwargs)
        self.mods = []

    def addModDict(self, mod):
        self.mods.append(mod)

    def __getitem__(self, item):
        mod = 0
        for m in self.mods :
            if item in m:
                mod += m[item]
        return dict.__getitem__(self, item) + mod



def getDefaultAttributes() :
    return Attributes()


def getModificator(value):
    """
    Gibt den entsprechenden Attributsmodifikator zurück.
    """
    return (1000,4,3,3,2,2,1,1, 0,0,0, -1,-1,-1,-1, -2,-2,-2,-2,-2, -3)[value]

