#!/usr/bin/python
# encoding: utf-8
from __future__ import division, print_function
import xml.etree.ElementTree as ElementTree
from rules.Core import xpCosts
from rules.Utils import none2Empty

SkillXPMultiplier = {
    0 : 0,
    1 : 10,
    2 : 3
}

class SkillTreeRoot(dict):
    def __init__(self, **kwargs):
        dict.__init__(self, {}, **kwargs)

    def summed(self):
        return 0

    def add(self, skill):
        if skill.name in self :
            self.replace(skill)
        else :
            self[skill.name] = skill
            skill.parent = self

    def __repr__(self):
        return "<SkillTree>"

    def replace(self, skill):
        ownSkill = self[skill.name]
        ownSkill.value = skill.value
        for subSkill in skill.values():
            ownSkill.add(subSkill)

    def getTotalCosts(self):
        costs = 0
        for v in self.values():
            costs += v.getCosts()
        return costs

    def getDepth(self):
        return 0


class Skill(dict):
    """
    Represent the element in a Skilltree.
    Has dict-like access:
    >> skillTree["Nahkampf.Ausweichen"]
    1
    and also:
    skillTree["Nahkampf"]["Ausweichen"]
    """
    def __init__(self, name, value, parent=None, **kwargs):
        dict.__init__(self, {}, **kwargs)
        self.name = name
        self.parent = parent
        self.value = int(value)

    def summed(self):
        if self.parent is not None:
            return self.value + self.parent.summed()
        else :
            return self.value

    def getDepth(self):
        return self.parent.getDepth() + 1

    def getCosts(self):
        depth = self.getDepth()
        mult = SkillXPMultiplier[depth]
        startVal = 1 if depth == 1 else 0 # BaseSkills first point is free
        return xpCosts(startVal, self.value, mult)

    def add(self, skill):
        if skill.name in self :
            self.replace(skill)
        else:
            self[skill.name] = skill
            skill.parent = self


    def replace(self, skill):
        ownSkill = self[skill.name]
        ownSkill.value = skill.value
        for subSkill in skill.values():
            ownSkill.add(subSkill)

    def __setitem__(self, key, value):
        if self.parent is not None:
            self.parent[self.name + "." + key] = value
        dict.__setitem__(self, key, value)

    def __repr__(self):
        r = "<Skill %s %d (%d)>"%(self.name, self.value, self.summed())
        return r.encode("utf-8")


def recursiveSkillAdd(root, xRoot):
    for xSkill in none2Empty(xRoot.findall("Fertigkeit")):
        skillName = xSkill.get("id")
        skillValue = xSkill.get("value", 0)
        if skillName is None:
            import warnings
            warnings.warn("Skill without id" + xSkill)
            continue
        skill = Skill(skillName, skillValue)
        root.add(skill)
        recursiveSkillAdd(root[skillName], xSkill)


def readSkillTreeFromXML(filename):
    tree = ElementTree.parse(filename)
    xSkillTree = tree.getroot()
    skillTree = SkillTreeRoot()
    recursiveSkillAdd(skillTree, xSkillTree)
    return skillTree


