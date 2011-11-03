#!/usr/bin/python
# -*- coding: utf-8
from __future__ import division, print_function
from rules import Attributes, defaultSkillTree
import rules
from rules.Attributes import getDefaultAttributes
from rules.Dicing import roll, getNumberOfSuccesses, isSuccessful
import xml.etree.ElementTree as ElementTree
import rules.Race as Race
from rules.Skilltree import recursiveSkillAdd
import copy


class Character(object):

    def __init__(self, name):
        self.name = name
        self.attributes = getDefaultAttributes()
        self.skills = copy.deepcopy(defaultSkillTree)
        self.vantages = []
        self.WT = 8
        self.RS = 0
        self.SR = 0
        self.exhaustion = 0
        self.AP = 0
        self.wounds = 0

    def rollAttribute(self, att, diff, minSuccesses = 0):
        assert att in self.attributes
        r = roll(self.attributes[att])
        if minSuccesses :
            return isSuccessful(r, diff, minSuccesses)
        else :
            return getNumberOfSuccesses(r, diff)

    def soak(self, damage, sharpness):
        """
        Macht den Widerstandswurf für den Charakter und gibt die Anzahl der Wunden zurück.
        """
        wounds = -1
        damage -= self.RS
        diff = sharpness - self.SR
        while damage > 0 :
            wounds += 1
            damage -= self.rollAttribute("KO", diff)
        return max(0, wounds)

    def doInitiative(self, diff):
        self.AP = self.rollAttribute("IN", diff)

    def isAlive(self):
        return self.exhaustion < self.attributes["KO"] and self.wounds < 6

    def getSkillsDict(self):
        skillsDict = {}
        for s, v in self.skills :
            skillsDict[s] = self.getPoolSize(s)
        return skillsDict

    def getPoolSize(self, skill):
        assert skill in self.skills
        # todo: "Hart im Nehmen"
        return max(1, self.skills[skill].summed() - self.exhaustion)

    def rollSkill(self, skill, diff, minSuccesses = 0, att=None) :
        assert skill in self.skills
        if att is not None and att in self.attributes:
            diff = max(1, diff + Attributes.getModificator(self.attributes["att"]))
        r = roll(self.getPoolSize(skill))
        if minSuccesses :
            return isSuccessful(r, diff, minSuccesses)
        else:
            return getNumberOfSuccesses(r, diff)

    def attack(self, weapon, maneuver):
        """
        Macht den Angriffswurf für den Charakter und gibt die Anzahl der Erfolge zurück
        """
        poolsize = max(1, self.WT - self.exhaustion)
        diff = maneuver.difficulty + weapon.handling
        r = roll(poolsize)
        return getNumberOfSuccesses(r, diff)

    def evaluateAttack(self, successes, weapon, maneuver, contraSuccesses = 0):
        # subtract all the contraSuccesses
        successes -= contraSuccesses
        if successes <= 0:
            return 0, 0       # Attack failed
        sharpness = min(weapon.schaerfe, successes * 2)
        successes = max(0, successes - (weapon.schaerfe+1)//2)
        impetus = maneuver.getImpetus(self, weapon, successes)
        return impetus, sharpness

    def __str__(self):
        indent = "  "
        result = "<Character " + self.name + "\n"
        for att in self.attributes.keys():
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
        char.attributes[Attributes.mapping[att.tag]] = int(att.get("value"))
    # Vantages
    for v in xChar.find("Teile") :
        vantageName = v.get("id")
        if vantageName in rules.vantages :
            char.addVantage(rules.vantages[vantageName])
        else :
            import warnings
            warnings.warn("Unknown Vantage '%s'"%vantageName)
    # Skills
    recursiveSkillAdd(char.skills, xChar.find("Fertigkeiten"))
    return char

