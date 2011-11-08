#!/usr/bin/python
# -*- coding: utf-8
from __future__ import division, print_function, unicode_literals
from rules.Dicing import roll, getNumberOfSuccesses
import xml.etree.ElementTree as ElementTree
from rules.Utils import none2Empty


maneuverXPCosts = {
    0 : 0,
    1 : 20,
    2 : 60,
    3 : 120
}

class Maneuver(object):
    def __init__(self, name, attributes = ()):
        self.name = name
        self.level = 0
        self.attributes = dict(attributes)
        self.mods = []
        self.sets = []
        self.options = []

    def createVarDict(self, char, weapon, options = None):
        variables = {"level" : self.level}
        # add options
        if options is not None:
            variables.update(options)
        # add weapon values
        if weapon is not None:
            variables["WT"] = char.getPoolSize(weapon.weaponSkill)
            variables.update(weapon)
        # add character values
        variables.update(char.attributes)
        variables.update(char.getSkillsDict())
        # validate options
        self.validateOptions(variables)
        return variables


    def evaluate(self, variables):
        # add sets
        for name, value in self.sets:
            try :
                variables[name] = eval(value, variables)
            except NameError as e:
                import warnings
                warnings.warn("could not evaluate Set: %s=%s because %s"%(name, value, e))
        # evaluate own values
        for k in self.attributes:
            try :
                variables[k] = eval(self.attributes[k], variables)
            except NameError as e:
                import warnings
                warnings.warn("could not evaluate Var: %s=%s because %s"%(k, self.attributes[k], e))

        # incorporate all possible modifications
        for name, value in self.mods :
            try :
                variables[name] += eval(value, variables)
            except NameError as e:
                import warnings
                warnings.warn("could not evaluate Mod: %s=%s because %s"%(k, self.attributes[k], e))

    def roll(self, char, weapon, options = None):
        variables = self.createVarDict(char, weapon, options)
        self.evaluate(variables)
        difficulty = variables["GS"]
        pool = variables["pool"]
        r = roll(pool)
        return getNumberOfSuccesses(r, difficulty)

    def validateOptions(self, varDict):
        for o in self.options:
            o.validate(varDict)

    def getDamage(self, char, weapon, options, successes):
        variables = self.createVarDict(char, weapon, options)
        variables["AQ"] = successes
        self.evaluate(variables)
        impetus = variables["wucht"]
        sharpness = variables["shaerfe"]
        return impetus, sharpness

    def getActionPoints(self, character, weapon, options):
        variables = self.createVarDict(character, weapon, options)
        self.evaluate(variables)
        AP = variables["AP"]
        return AP

    def copy(self):
        maneuver = Maneuver(self.name, self.attributes)
        # todo do we need to deep-copy those?
        maneuver.mods = list(self.mods)
        maneuver.sets = list(self.sets)
        maneuver.options = list(self.options)
        maneuver.level = self.level
        return maneuver

    def getXPCosts(self):
        return maneuverXPCosts[self.level]

class Option(object):
    def __init__(self, name, type, condition):
        self.name = name
        self.type = eval(type)
        self.condition = condition

    def validate(self, valuesDict):
        assert self.name in valuesDict
        assert valuesDict[self.name] is self.type
        assert eval(self.condition, globals = valuesDict)


def readManeuversFromXElement(xManeuvers):
    maneuvers = {}
    for xManeuver in none2Empty(xManeuvers.findall("Manoever")) :
        # get name action points and base difficulty
        maneuverName = xManeuver.get("id")
        AP = xManeuver.get("AP")
        baseDiff = xManeuver.get("GS")
        maneuver = Maneuver(maneuverName, actionPoints=AP, baseDifficulty=baseDiff)
        # get Pool
        xPool = xManeuver.find("Pool")
        if xPool is not None :
            maneuver.pool = xPool.text
        # get impetus
        xImpetus = xManeuver.find("Wucht")
        if xImpetus is not None :
            maneuver.impetus = xImpetus.text
        # todo get options
        maneuvers[maneuverName] = maneuver
    return maneuvers


def readModFromXMLTag(modTag):
    assert modTag.tag == "Mod"
    varName = modTag.get("var")
    modAmount = modTag.get("value")
    assert varName is not None
    assert modAmount is not None
    return varName, modAmount

def readSetFromXMLTag(setTag):
    assert setTag.tag == "Set"
    varName = setTag.get("var")
    value = setTag.get("value")
    assert varName is not None
    assert value is not None
    return varName, value

#<Option name="X" type="int" bedingung="0 &lt; X and X &lt;= Nahkampf.Ausweichen"/>
def readOptionFromXMLTag(optionTag):
    assert optionTag.tag == "Option"
    optName = optionTag.get("name")
    optType = optionTag.get("type", "int")
    optCondition = optionTag.get("bedingung")
    assert optName is not None
    option = Option(optName, optType, optCondition)
    return option


def readManeuverFromXMLTag(tag, patterns):
    maneuverDict = dict(tag.items())
    assert "id" in maneuverDict
    assert "AP" in maneuverDict
    # get maneuver name
    maneuverName = maneuverDict.pop("id")
    # get maneuver Type and inherit if possible
    maneuverType = maneuverDict.pop("typ", "")
    if maneuverType in patterns :
        maneuver = patterns[maneuverType].copy()
        maneuver.attributes.update(maneuverDict)
        maneuver.name = maneuverName
    else :
        maneuver = Maneuver(maneuverName, maneuverDict)
        if maneuverType != "" :
            import warnings
            warnings.warn("Unknown maneuver type '%s' for %s!"%(maneuverType, maneuverName))
    # Read Modifiers and Setters
    for subTag in tag:
        if subTag.tag == "Mod":
            maneuver.mods.append(readModFromXMLTag(subTag))
        if subTag.tag == "Set":
            maneuver.sets.append(readSetFromXMLTag(subTag))
        if subTag.tag == "Option":
            maneuver.options.append(readOptionFromXMLTag(subTag))
    return maneuver


def readManeuversFromXML(filename):
    tree = ElementTree.parse(filename)
    xManeuvers= tree.getroot()
    # first we read all maneuver-patterns
    patterns = {}
    for xPattern in none2Empty(xManeuvers.findall("Muster")):
        pattern = readManeuverFromXMLTag(xPattern, patterns)
        patterns[pattern.name] = pattern
        # Now we read all actual maneuvers
    maneuvers = {}
    for xManeuver in none2Empty(xManeuvers.findall("Manoever")):
        maneuver = readManeuverFromXMLTag(xManeuver, patterns)
        maneuvers[maneuver.name] = maneuver
    return maneuvers
