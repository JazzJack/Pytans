#!/usr/bin/python
# -*- coding: utf-8
from __future__ import division, print_function, unicode_literals
import xml.etree.ElementTree as ElementTree
from rules import defaultSkillTree
from rules.Utils import none2Empty

weightUnits = {"kg" : 1.,
               "g"  : 0.001,
               "t"  : 1000}

weaponAttributes = ["WW", "minST", "schaerfe", "handling"]
derivedAttributes = {"kopflastig" : "WW > minST",
                     "leicht" : "2*WW <= ST",
                     "schwer" : "WW > ST"}

class Weapon(dict):
    def __init__(self, name, **kwargs):
        defaultValues = {"Waffentalent" : "Nahkampf.Handgemenge"}
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
        for d, v in derivedAttributes.items():
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
    for xWeapon in none2Empty(xArsenal.findall("Waffe")):
        # get weapon name
        weaponName = xWeapon.get("id")
        weapon = Weapon(weaponName)
        # get weapon attributes
        for a in weaponAttributes:
            weapon[a] = eval(xWeapon.get(a, "0"))
        # get weapon weight
        weapon.weight = getWeightInKg(xWeapon)
        # get weapon skill
        xWT = xWeapon.find("Talent")
        if xWT is not None:
            WT = xWT.text
            if WT in defaultSkillTree:
                weapon["Waffentalent"] = WT
            else :
                import warnings
                warnings.warn(("Invalid WeaponSkill %s for %s"%(WT, weapon)).encode("utf-8"))
        # add weapon to weapons dict
        weapons[weaponName] = weapon
    return weapons
