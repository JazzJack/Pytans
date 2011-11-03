#!/usr/bin/python
# -*- coding: utf-8
from __future__ import division, print_function
import xml.etree.ElementTree as ElementTree
from rules import defaultSkillTree

weightUnits = {"kg" : 1.,
               "g"  : 0.001,
               "t"  : 1000}

weaponAttributes = ["WW", "minST", "schaerfe", "handling"]
derivedAttributes = {"kopflastig" : "WW > minST",
                     "leicht" : "ST >= 2*WW",
                     "schwer" : "ST < WW"}

class Weapon(dict):
    def __init__(self, name, **kwargs):
        defaultValues = {"WT" : "Nahkampf.Handgemenge"}
        dict.__init__(self, defaultValues, **kwargs)
        self.name = name
        self.weight = 0

    def __repr__(self):
        r = "<Waffe " + self.name + ": "
        for a, v in self.items():
            r += a + "=" + v + ", "
        return (r[:-2] + ">").encode("utf-8")

    def getVarDict(self, charValues):
        values = dict(self)
        values.update(charValues)
        result = dict(self)
        for d, v in derivedAttributes:
            result[d] = eval(v, values)
        return result



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
        weapon.weight = getWeightInKg(xWeapon)
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
