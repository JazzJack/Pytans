#!/usr/bin/python
# -*- coding: utf-8
from __future__ import division, print_function, unicode_literals

import xml.etree.ElementTree as ElementTree
import copy

import rules
from rules import defaultSkillTree
from rules.Announcement import Announcement, Action
import rules.Attributes
from rules.Dicing import roll, getNumberOfSuccesses, isSuccessful
import rules.Race as Race
from rules.Skilltree import recursiveSkillAdd
from rules.Utils import none2Empty



class Character(object):

    def __init__(self, name):
        self.name = name
        self.attributes = rules.Attributes.Attributes()
        self.skills = copy.deepcopy(defaultSkillTree)
        self.vantages = []
        self.WT = 8
        self.RS = 0
        self.SR = 0
        self.exhaustion = 0
        self.AP = 0
        self.wounds = 0
        self.maneuvers = []
        self.feats = []

    def rollAttribute(self, att, diff, minSuccesses = 0):
        r = roll(self.attributes[att])
        if minSuccesses :
            return isSuccessful(r, diff, minSuccesses)
        else :
            return getNumberOfSuccesses(r, diff)

    def soak(self, damage, sharpness):
        """
        Macht den Widerstandswurf für den Charakter und gibt die Anzahl der Wunden zurück.
        """
        d = damage
        wounds = -1
        damage -= self.RS
        diff = sharpness - self.SR
        while damage > 0 :
            wounds += 1
            damage -= self.rollAttribute("KO", diff)
        wounds = max(0, wounds)
        self.wounds += wounds
        self.exhaustion += wounds
        #print("%s soaked %d against the %d and got %d wounds!"%(self.name, d, sharpness, wounds))
        return wounds

    def doInitiative(self, diff):
        self.AP = self.rollAttribute("IN", diff)

    def isAlive(self):
        return self.exhaustion < self.attributes["KO"] and self.wounds < 6

    def reset(self):
        self.wounds = 0
        self.exhaustion = 0
        self.AP = 0

    def getSkillsDict(self):
        skillsDict = {}
        for s, v in self.skills.items() :
            skillsDict[s] = self.getPoolSize(s)
        return skillsDict

    def getPoolSize(self, skill):
        assert skill in self.skills
        # todo: "Hart im Nehmen"
        return max(1, self.skills[skill].summed() - self.exhaustion)

    def rollSkill(self, skill, diff, minSuccesses = 0, att=None) :
        assert skill in self.skills
        if att is not None and att in self.attributes:
            diff = max(1, diff + self.attributes.getModifier(att))
        r = roll(self.getPoolSize(skill))
        if minSuccesses :
            return isSuccessful(r, diff, minSuccesses)
        else:
            return getNumberOfSuccesses(r, diff)

    def attack(self, weapon, maneuver, target, options = None):
        """
        Erzeugt ein Ansageobjekt und reduziert die AP
        """
        attack = Action(self, maneuver, weapon, options)
        assert self.AP >= 0
        announcement = Announcement(attack, target)
        return announcement

    def gainAP(self):
        gain = 3 - self.attributes.getModifier("SN")
        self.AP = min(self.attributes["GE"], self.AP + gain)
        print("Character %s got %d AP (total %d)"%(self.name, gain, self.AP))

    def __str__(self):
        indent = "  "
        result = "<Character " + self.name + "\n"
        for att, _ in self.attributes:
            result += indent + att + " = " + str(self.attributes[att]) + "\n"
        result += ">"
        return result.encode("utf-8")

    def __repr__(self):
        return self.__str__()

    def setRace(self, race):
        self.race = race
        self.attributes.addModDict(race.attributeMods)

    def addVantage(self, vantage):
        self.vantages.append(vantage)
        self.attributes.addModDict(vantage.mods)

    def getXPCosts(self):
        costs = self.race.getXPCosts()
        costs += self.attributes.getXPCosts()
        costs += self.skills.getTotalCosts()
        for v in self.vantages:
            costs += v.costs
        for m in self.maneuvers:
            costs += m.getXPCosts()
        for f in self.feats:
            costs += f.costs
        return costs

    def addFeat(self, feat):
        self.feats.append(feat)


def readCharacterFromXML(filename):
    tree = ElementTree.parse(filename)
    xChar = tree.getroot()
    # Name
    char = Character(xChar.find("Name").text)
    # Race
    raceName = xChar.find("Rasse").text
    char.setRace(Race.getRaceByName(raceName))
    # Attributes
    for att in xChar.find("Attribute"):
        char.attributes[rules.Attributes.mapping[att.tag]] = int(att.get("value"))
    # Vantages
    for v in none2Empty(xChar.find("Teile")) :
        vantageName = v.get("id")
        if vantageName in rules.vantages :
            char.addVantage(rules.vantages[vantageName])
        else :
            import warnings
            warnings.warn("Unknown Vantage '%s'"%vantageName)
    # Feats
    for f in none2Empty(xChar.find("Sonderfertigkeiten")) :
        featName = f.get("id")
        if featName in rules.feats:
            char.addFeat(rules.feats[featName])
        else :
            import warnings
            warnings.warn("Unknown Feat '%s' in char %s"%(featName, char.name))
    # Skills
    recursiveSkillAdd(char.skills, xChar.find("Fertigkeiten"))
    # Maneuvers
    for xManeuver in none2Empty(xChar.find("ManöverListe")):
        maneuverName = xManeuver.get("id")
        if maneuverName in rules.maneuvers:
            maneuver = rules.maneuvers[maneuverName].copy()
            maneuver.level = int(xManeuver.get("stufe"))
            char.maneuvers.append(maneuver)
        else :
            import warnings
            warnings.warn("Unknown Maneuver %s in Char %s"%(maneuverName, char.name))
    return char

