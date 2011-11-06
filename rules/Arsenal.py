#!/usr/bin/python
# -*- coding: utf-8
from __future__ import division, print_function, unicode_literals
import xml.etree.ElementTree as ElementTree
from rules import defaultSkillTree
from rules.Utils import none2Empty

weightUnits = {"kg" : 1.,
               "g"  : 0.001,
               "t"  : 1000}

class Weapon(dict):
    def __init__(self, name, attributes, **kwargs):
        dict.__init__(self, attributes, **kwargs)
        self.name = name
        self.weight = 0
        self.weaponSkill = ""

    def __repr__(self):
        r = "<Waffe " + self.name + ": "
        for a, v in self.items():
            r += a + "=" + v + ", "
        return (r[:-2] + ">").encode("utf-8")

    def copy(self):
        copy = Weapon(self.name, self)
        copy.weight = self.weight
        copy.weaponSkill = self.weaponSkill
        return copy



def getWeightInKg(xTag):
    weight = 0
    xWeight = xTag.find("Gewicht")
    if xWeight is not None:
        unit = xWeight.get("unit")
        factor = 1.
        if unit is not None:
            factor = weightUnits[unit]
        weight = float(xWeight.text) * factor
    return weight

def readWeaponFromXMLTag(tag, patterns):
    # get weapon name
    weaponDict = dict(tag.items())
    weaponName = weaponDict.pop("id")
    # get weapon Type and inherit if possible
    weaponType = weaponDict.pop("typ", "")
    if weaponType in patterns:
        weapon = patterns[weaponType].copy()
        weapon.update(weaponDict)
        weapon.name = weaponName
    else:
        weapon = Weapon(weaponName, weaponDict)
        if weaponType != "" :
            import warnings
            warnings.warn("Unknown weapon type '%s' for %s!"%(weaponType, weaponName))
    # get Weight
    weapon.weight = getWeightInKg(tag)
    # get weapon skill
    xWT = tag.find("Talent")
    if xWT is not None:
        WT = xWT.text
        if WT in defaultSkillTree:
            weapon["Waffentalent"] = WT
        else :
            import warnings
            warnings.warn(("Invalid WeaponSkill %s for %s"%(WT, weapon)).encode("utf-8"))
    return weapon


def readWeaponsFromXML(filename):
    tree = ElementTree.parse(filename)
    xArsenal= tree.getroot()
    # First we read all weapon-patterns
    patterns = {}
    for xPattern in none2Empty(xArsenal.findall("Muster")):
        pattern = readWeaponFromXMLTag(xPattern, patterns)
        patterns[pattern.name] = pattern
    # Now we read all actual weapons
    weapons = {}
    for xWeapon in none2Empty(xArsenal.findall("Waffe")):
        weapon = readWeaponFromXMLTag(xWeapon, patterns)
        weapons[weapon.name] = weapon
    return weapons
