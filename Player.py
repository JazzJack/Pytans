#!/usr/bin/python
# encoding: utf-8

from __future__ import division, print_function
import random
from rules import Character
from rules.Announcement import Announcement

class Player(object):
    def __init__(self, name, character, arena):
        self.name = name
        self.character = character
        character.player = self
        self.arena = arena

    def doInitiative(self, diff = 6):
        self.character.doInitiative(diff)

    def wait(self):
        return 0

    def act(self):
        print("Act ist leer.")

    def react(self, announcement):
        print("React ist leer.")



class RandomPlayer(Player):
    def __init__(self, name, character, arena, action, reaction):
        Player.__init__(self, name, character, arena)
        self.action = action
        self.reaction = reaction

    def act(self):
        if self.character.AP < self.action.getAP() :
            return
        if random.randint(0,1) :
            # get enemy
            print("%s : ATTACK!!!!"%self.character.name)
            target = self.arena.getEnemy(self.character)[0]
            return Announcement(self.action, target)
        print("Wait...")

    def react(self, announcement):
        if self.character.AP > self.reaction.getAP() :
            announcement.reaction = self.reaction
