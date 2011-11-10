#!/usr/bin/python
# encoding: utf-8
from __future__ import division, print_function, unicode_literals
import numpy as np

from rules.Character import readCharacterFromXML
from rules.Maneuvers import readManeuversFromXML

from rules import *

testManeuver = readManeuversFromXML(os.path.join(basedir, "res/Manoever_test.xml"))

hieb2 = maneuvers["Hieb"].copy()
hieb2.level = 2
stich2 = maneuvers["Stich"].copy()
stich2.level = 2


testHieb2 = testManeuver["Hieb"].copy()
testHieb2.level = 2
testStich2 = testManeuver["Stich"].copy()
testStich2.level = 2

agilitus = readCharacterFromXML(os.path.join(basedir, "res/Charactere/Agilitus.xml"))
agilitus.weapon = weapons["GestochenerDegen"]
agilitus.maneuver = stich2
agilitus.tManeuver = testStich2

gravitus = readCharacterFromXML(os.path.join(basedir, "res/Charactere/Gravitus.xml"))
gravitus.weapon = weapons["Breitschwert"]
gravitus.maneuver = hieb2
gravitus.tManeuver = testHieb2

potestatus = readCharacterFromXML(os.path.join(basedir, "res/Charactere/Potestatus.xml"))
potestatus.weapon = weapons["Anderthalbhänder"]
potestatus.maneuver = hieb2
potestatus.tManeuver = testHieb2

queentius = readCharacterFromXML(os.path.join(basedir, "res/Charactere/Queentius.xml"))
queentius.weapon = weapons["Breitschwert"]
queentius.maneuver = hieb2
queentius.tManeuver = testHieb2

chars = [agilitus, gravitus, potestatus, queentius]



def fight(char, weapon, maneuver, target, RS = 0, SR = 0):
    char.reset()
    target.reset()
    AP = maneuver.getActionPoints(char, weapon, {})
    AQ = maneuver.roll(char, weapon, {})
    wucht, shaerfe = maneuver.getDamage(char, weapon, {}, AQ)
    wounds = target.soak(max(0, wucht - RS), max(1, shaerfe - SR))
    APR = 3 - char.attributes.getModifier("SN")
    WPR = wounds / AP * APR
    return np.array([AP, AQ, wucht, shaerfe, wounds, WPR])

def repeat(char, weapon, maneuver, target, iterations = 10000, RS = 0, SR = 0):
    results = np.array([]).reshape(0,6)
    for i in range(iterations):
        r = fight(char, weapon, maneuver, target, RS, SR)
        results = np.vstack((results, r))

    mean = results.mean(0)
    min = results.min(0)
    max = results.max(0)
    var = results.var(0)
    return min, mean, max, var

def printDokuWikiReport(resultTuple):
    print("^ Results ^ AP ^ AQ ^ Wucht ^ Schaerfe ^ Wunden ^ WPR ^")
    print("^ Min:  |" + ("{:<6.1f} |"*6).format(*tuple(resultTuple[0])))
    print("^ Mean: |" + ("{:<6.1f} |"*6).format(*tuple(resultTuple[1])))
    print("^ Max:  |" + ("{:<6.1f} |"*6).format(*tuple(resultTuple[2])))
    print("^ Var:  |" + ("{:<6.1f} |"*6).format(*tuple(resultTuple[3])))

def printCSVReport(resultTuple):
    print("\tResults\tAP\tAQ\tWucht\tSchaerfe\tWunden\tWPR")
    print(("Min:\t" + ("{:<6.1f}\t"*6).format(*tuple(resultTuple[0]))).replace(".", ","))
    print(("Mean:\t" + ("{:<6.1f}\t"*6).format(*tuple(resultTuple[1]))).replace(".", ","))
    print(("Max:\t" + ("{:<6.1f}\t"*6).format(*tuple(resultTuple[2]))).replace(".", ","))
    print(("Var:\t" + ("{:<6.1f}\t"*6).format(*tuple(resultTuple[3]))).replace(".", ","))


encounter = []
for i1 in range(len(chars)):
    for i2 in range(len(chars)) :
        encounter.append((chars[i1], chars[i2]))

for c1, c2 in encounter:
    r1 = repeat(c1, c1.weapon, c1.maneuver, c2)
    r2 = repeat(c1, c1.weapon, c1.tManeuver, c2)
    rDiff = np.asarray(r2) - np.asarray(r1)

    print ("=== %s VS %s ==="%(c1.name, c2.name))
    print ("== alte Regel ==")
    printCSVReport(r1)
    print ("== neue Regel ==")
    printCSVReport(r2)
    print ("== Differenz ==")
    printCSVReport(rDiff)
