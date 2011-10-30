#!/usr/bin/python
# -*- coding: utf-8
from __future__ import division, print_function
import xml.etree.ElementTree as ElementTree
from rules import *
import os
from rules.Utils import none2Empty

attributeModCost = {
    -4 : -350,
    -3 : -225,
    -2 : -125,
    -1 : -50,
    0 : 0,
    1 : 55,
    2 : 135,
    3 : 240,
    4 : 370
}


class Race(object):
    def __init__(self, name):
        self.name = name
        self.attributeMods = {}
        self.vantages = []

    def __repr__(self):
        r = "<Race " + self.name + ">"
        return r.encode("utf-8")

    def getVantageCosts(self):
        costs = 0
        for v in self.vantages:
            costs += raceVantages[v].costs
        return costs

    def getAttributeModCosts(self):
        costs = 0
        for att, v in self.attributeMods.items():
            costs += attributeModCost[v]
        return costs

    @property
    def costs(self):
        return self.getVantageCosts() + self.getAttributeModCosts()



def readRaceFromFile(filename):
    tree = ElementTree.parse(filename)
    xRace = tree.getroot()
    raceName = xRace.find("Name").text
    race = Race(raceName)
    # Read Attribute Modifiers

    for attMod in none2Empty(xRace.find("Attribute")):
        assert attMod.tag == "Attributsmod"
        attributeName = attMod.get("attribut")
        attributeMod = int(attMod.get("mod"))
        race.attributeMods[attributeName] = attributeMod
    # Read Advantages and Disadvantages
    for vantage in none2Empty(xRace.find("Teile")):
        assert vantage.tag in ["Vorteil", "Nachteil"]
        race.vantages.append(unicode(vantage.get("id")))
    return race

def getRaceByName(name) :
    basePath = "res/Rassen/"
    return readRaceFromFile(basePath + name + ".xml")

def readAllRaces(path):
    races = {}
    for f in os.listdir(path):
        if f.endswith(".xml") :
            r = readRaceFromFile(os.path.join(path, f))
            races[r.name] = r
    return races