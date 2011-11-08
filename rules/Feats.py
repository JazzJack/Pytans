#!/usr/bin/python
# encoding: utf-8
from __future__ import division, print_function, unicode_literals
import xml.etree.ElementTree as ElementTree
from rules.Utils import none2Empty


class Feat(object):
    def __init__(self, name, costs = "0"):
        self.name = name
        self.costs = costs
        self.mods = {}

    def __repr__(self):
        r = "<Feat " + self.name + "(" + str(self.costs) + " EP)>"
        return r.encode("utf-8")


def readFeatsFromFile(filename):
    feats = {}
    parser = ElementTree.XMLParser(encoding="utf-8")
    tree = ElementTree.parse(filename, parser)
    xFeats = tree.getroot()
    for xVantage in none2Empty(xFeats.findall("Sonderfertigkeit")):
        featName = xVantage.get("id")
        featCost = xVantage.get("kosten", "0")
        if featName is not None:
            feat = Feat(featName, int(featCost))
            feats[featName] = feat
    return feats