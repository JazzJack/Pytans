#!/usr/bin/python
# -*- coding: utf-8
from __future__ import division, print_function, unicode_literals

import xml.etree.ElementTree as ElementTree

from rules import defaultSkillTree
from rules.Utils import none2Empty

# Unit conversion factors to determine weights of items
weightUnits = {"kg" : 1.,
               "g"  : 0.001,
               "t"  : 1000,
               "pounds" : 0.5,
               "pfund" : 0.5,
               "stein" : 0.96,
               "zentner" : 50,
               "karat" : 0.0002,
               "Unze" : 0.0283,
               "mg"   : 0.000001,
               "kt"   : 1000000
}

class Weapon(dict):
    """
    Represents a weapon and acts mainly as a dictionary.
    you can access any value of the weapon by the [ ] operator.
    Only name, weight and weaponSkill are stored as attributes.
    """
    def __init__(self, name, **kwargs):
        dict.__init__(self, (), **kwargs)
        self.name = name
        self.weight = 0
        self.weaponSkill = ""

    def __repr__(self):
        r = "<Waffe " + self.name + ": "
        for a, v in self.items():
            r += a + "=" + str(v) + ", "
        return (r[:-2] + ">").encode("utf-8")

    def copy(self):
        copy = Weapon(self.name)
        copy.weight = self.weight
        copy.weaponSkill = self.weaponSkill
        copy.update(self)
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
        weapon.name = weaponName
    else:
        weapon = Weapon(weaponName)
        if weaponType != "" :
            import warnings
            warnings.warn("Unknown weapon type '%s' for %s!"%(weaponType, weaponName))
    # add evaluated attributs
    for a, v in weaponDict.items():
        weapon[a] = eval(v)
    # get Weight
    weapon.weight = getWeightInKg(tag)
    # get weapon skill
    xWT = tag.find("Talent")
    if xWT is not None:
        WT = xWT.text
        if WT in defaultSkillTree:
            weapon.weaponSkill = WT
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
