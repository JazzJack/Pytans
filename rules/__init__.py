#!/usr/bin/python
# -*- coding: utf-8
from __future__ import division, print_function, unicode_literals

##################### Configure baseDir ########################################
import os
if os.path.exists("res") and os.path.exists("rules"):
    basedir = "."
elif os.path.exists("../res") and os.path.exists("../rules"):
    basedir = ".."
else:
    import warnings
    warnings.warn("Basedir not found!")
    basedir = "."

#################### read all Vantages #########################################
from rules.Vantages import readVantagesFromFile
vantages = readVantagesFromFile(os.path.join(basedir, "res/Teile.xml"))
raceVantages = readVantagesFromFile(os.path.join(basedir, "res/RassenTeile.xml"))

#################### read all Races ############################################
from rules.Race import readAllRaces
races = readAllRaces(os.path.join(basedir, "res/Rassen"))


#################### read Skilltree ############################################
from rules.Skilltree import readSkillTreeFromXML
defaultSkillTree = readSkillTreeFromXML(os.path.join(basedir, "res/SkillTree.xml"))

#################### read Arsenal ##############################################
from rules.Weapons import readWeaponsFromXML
weapons = readWeaponsFromXML(os.path.join(basedir, "res/Arsenal.xml"))

# conversion for interactive console
def u(s):
    return unicode(s, "utf-8")
