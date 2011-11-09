#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
from Arena import Arena
from Combat import Combat
from Player import Player, RandomPlayer
from rules import *
import logging
import sys

handler = logging.StreamHandler(sys.stdout)
frm = logging.Formatter("%(levelname)s:\t%(message)s")
handler.setFormatter(frm)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.critical("Ein wirklich kritischer Fehler")
logger.warning("Und eine Warnung hinterher")
logger.info("Dies hingegen ist nur eine Info")


# Create two characters
from rules.Announcement import Action, Announcement


hieb0 = maneuvers["Hieb"].copy()
hieb1 = maneuvers["Hieb"].copy()
hieb1.level = 1
hieb2 = maneuvers["Hieb"].copy()
hieb2.level = 2
hieb3 = maneuvers["Hieb"].copy()
hieb3.level = 3

block0 = maneuvers["Block"].copy()
block1 = maneuvers["Block"].copy()
block1.level = 1
block2 = maneuvers["Block"].copy()
block2.level = 2
block3 = maneuvers["Block"].copy()
block3.level = 3

gladius = weapons["Gladius"]




char1 = readCharacterFromXML(os.path.join(basedir, "res/Charactere/Agilitus.xml"))
char1.name = "Hugo"
action1 = Action(char1, hieb0, gladius)
reaction1 = Action(char1, block0, gladius)

char2 = readCharacterFromXML(os.path.join(basedir, "res/Charactere/Agilitus.xml"))
char2.name = "Herbert"
action2 = Action(char2, hieb0, gladius)
reaction2 = Action(char2, block0, gladius)

arena = Arena()
arena.addTeam("blue", [char1])
arena.addTeam("red", [char2])
print (arena.getCharacters())
# Create a Player for each character


player1 = RandomPlayer("Player1", char1, arena, action1, reaction1)
player2 = RandomPlayer("Player2", char2, arena, action2, reaction2)
players = [player1, player2]

points = [0,0]
for round in range(100):
    # reset chars
    char1.reset()
    char2.reset()
    # Create a combat
    combat = Combat(arena, players)
    # fight till the death of one team
    combat.fightTillDefeat()
    points[0] += 1 if char1.isAlive() else 0
    points[1] += 1 if char2.isAlive() else 0
print("%s VS %s   =>  (%d : %d)"%(char1.name, char2.name, points[0], points[1]))



