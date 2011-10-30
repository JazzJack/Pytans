#!/usr/bin/python
# encoding: utf-8
from __future__ import division, print_function
from rules.Character import Character, readCharacterFromXML
from rules.Maneuvers import *
from rules.Weapons import *
import Combat
import Player
import numpy as np

class Arena:
    def __init__(self):
        self.teams = {}

    def addTeam(self,name, characters):
        self.teams[name] = characters

    def addCharacter(self, team, character):
        self.teams[team].append(character)

    def getCharacters(self):
        characters = []
        for team in self.teams:
            characters.extend(team)
        return characters

# Create two characters
char1 = readCharacterFromXML("res/Charaktere/Nostro.xml")
char2 = readCharacterFromXML("res/Charaktere/Nostro.xml")
arena = Arena()
arena.addTeam("blue", [char1])
arena.addTeam("red", [char2])
# Create a Player for each character
players = []
for character in arena.getCharacters():
    players.append("Player of "+character.name,Player(character),arena)
# Create a combat
combat = Combat(arena, players)
# fight till the death of one team
combat.fightTillDefeat()

print("Simulating 1000 %s by %s using %s..."%("Hiebe", "Adrian", "Gladius"))
successes = []
impetusses = []
sharpnesses = []
wounds = []
for i in range(1000):
    s = adrian.attack(Langschwert, Hieb3)
    impetus, sharpness = adrian.evaluateAttack(s, Langschwert, Hieb3)
    successes.append(s)
    impetusses.append(impetus)
    sharpnesses.append(sharpness)
    wound = horst.soak(impetus, sharpness)
    wounds.append(wound)


successes = np.array(successes)
impetusses = np.array(impetusses)
sharpnesses = np.array(sharpnesses)
wounds = np.array(wounds)

print("%f Successes at average with a variance of %f"%(successes.mean(), successes.var()))
print("%f Impetus at average with a variance of %f"%(impetusses.mean(), impetusses.var()))
print("%f Sharpness at average with a variance of %f"%(sharpnesses.mean(), sharpnesses.var()))
print("%f Wounds at average with a variance of %f"%(wounds.mean(), wounds.var()))




