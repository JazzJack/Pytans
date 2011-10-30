#!/usr/bin/python
# -*- coding: utf-8
from __future__ import division, print_function
import xml.etree.ElementTree as ElementTree
from rules import defaultSkillTree

weaponAttributes = ["WW", "minST", "schaerfe", "handling"]
weightUnits = {"kg" : 1.,
               "g"  : 0.001,
               "t"  : 1000}

class Weapon(object):
    def __init__(self, name):
        self.name = name
        self.weaponSkill = "Nahkampf.Handgemenge"

    def __repr__(self):
        r = "<Waffe " + self.name + ": "
        for a in dir(self):
            v = self.__getattribute__(a)
            if type(v) is int:
                r += "%s=%d, "%(a, v)
            elif type(v) is float:
                r += "%s=%.2f, "%(a, v)
        return (r[:-2] + ">").encode("utf-8")

    @property
    def kopflastig(self):
        return self.WW > self.minST


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

def readWeaponsFromXML(filename):
    tree = ElementTree.parse(filename)
    xArsenal= tree.getroot()
    weapons = {}
    for xWeapon in xArsenal.findall("Waffe"):
        weaponName = xWeapon.get("id")
        weapon = Weapon(weaponName)
        for a in weaponAttributes:
            weapon.__setattr__(a, int(xWeapon.get(a, 0)))
        weapon.gewicht = getWeightInKg(xWeapon)
        xWT = xWeapon.find("Talent")
        if xWT is not None:
            WT = xWT.text
            if WT in defaultSkillTree:
                weapon.weaponSkill = WT
            else :
                import warnings
                warnings.warn(("Invalid WeaponSkill %s for %s"%(WT, weapon)).encode("utf-8"))
        weapons[weaponName] = weapon
    return weapons
