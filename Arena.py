#!/usr/bin/python
# encoding: utf-8
from __future__ import division, print_function
import os
from rules import basedir
from rules.Character import readCharacterFromXML
from Combat import Combat
from Player import Player


class Arena:
    def __init__(self):
        self.teams = {}

    def addTeam(self,name, characters):
        self.teams[name] = characters

    def addCharacter(self, team, character):
        self.teams[team].append(character)

    def getCharacters(self):
        characters = []
        for team in self.teams.values():
            characters += team
        return characters

# Create two characters
char1 = readCharacterFromXML(os.path.join(basedir, "res/Charactere/Nostro.xml"))
char2 = readCharacterFromXML(os.path.join(basedir, "res/Charactere/Nostro.xml"))
arena = Arena()
arena.addTeam("blue", [char1])
arena.addTeam("red", [char2])
print (arena.getCharacters())
# Create a Player for each character
players = []
for character in arena.getCharacters():
    players.append(Player("Player of " + character.name, character))
# Create a combat
combat = Combat(arena, players)
# fight till the death of one team
combat.fightTillDefeat()





