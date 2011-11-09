#!/usr/bin/python
# encoding: utf-8
from __future__ import division, print_function


class NoneReaction(object):
    def evaluate(self):
        return 0

    def getDamage(self, _):
        return 0, 0


class Action(object):
    def __init__(self, actor, maneuver, weapon, options = None):
        self.actor = actor
        self.maneuver = maneuver
        self.weapon = weapon
        self.options = options

    def evaluate(self):
        self.actor.AP -= self.getAP()
        return self.maneuver.roll(self.actor, self.weapon, self.options)

    def getDamage(self, successes):
        return self.maneuver.getDamage(self.actor, self.weapon, self.options, successes)

    def getAP(self):
        return self.maneuver.getActionPoints(self.actor, self.weapon, self.options)



class Announcement(object):
    def __init__(self, action, target, reaction = NoneReaction()):
        self.action = action
        self.target = target
        self.reaction = reaction

    def evaluate(self):
        AQ = self.action.evaluate()
        AQ -= self.reaction.evaluate()
        if AQ <= 0:
            impetus, sharpness = self.action.getDamage(0)
            reImpetus, _ = self.reaction.getDamage(0)
            impetus -= reImpetus
            if impetus <= 0:
                return False
        else :
            impetus, sharpness = self.action.getDamage(AQ)
        self.target.soak(impetus, sharpness)
        return True


