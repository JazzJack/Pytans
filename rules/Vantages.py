#!/usr/bin/python
# -*- coding: utf-8
from __future__ import division, print_function, unicode_literals
import xml.etree.ElementTree as ElementTree
from rules.Utils import none2Empty


class Vantage(object):
    def __init__(self, name, costs = 0):
        self.name = name
        self.costs = costs
        self.mods = {}

    def __repr__(self):
        if self.costs > 0 :
            r = "<Advantage "
        else :
            r = "<Disadvantage "
        r += self.name + "(" + str(self.costs) + " EP)>"
        return r.encode("utf-8")



def readVantagesFromFile(filename):
    vantages = {}
    parser = ElementTree.XMLParser(encoding="utf-8")
    tree = ElementTree.parse(filename, parser)
    xVantages = tree.getroot()
    xAdvantages = none2Empty(xVantages.findall("Vorteil"))
    xDisadvantages = none2Empty(xVantages.findall("Nachteil"))
    for xVantage in xAdvantages + xDisadvantages:
        vantageName = xVantage.get("id")
        vantageCost = xVantage.get("kosten", 0)
        if vantageName is not None:
            vantage = Vantage(vantageName, int(vantageCost))
            for attMod in none2Empty(xVantage.findall("Attributsmod")) :
                vantage.mods[attMod.get("attr")] = int(attMod.get("mod", 0))
            vantages[vantageName] = vantage
    return vantages

