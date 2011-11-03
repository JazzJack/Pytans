#!/usr/bin/python
# encoding: utf-8

from __future__ import division, print_function
from rules import Character

class Player:
    def __init__(self, name, character):
        self.name = name
        self.character = character

    def doInitiative(self, diff = 6):
        self.character.doInitiative(diff)

    def wait(self):
        return 0

    def act(self):
        print("Act ist leer.")
