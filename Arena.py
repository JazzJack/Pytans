#!/usr/bin/python
# encoding: utf-8
from __future__ import division, print_function
from rules.Character import Character
from rules.Maneuvers import *
from rules.Weapons import *
import numpy as np

horst = Character("Horst")
horst.ST = 12
horst.KO = 16
horst.GE = 8
horst.SN = 8
horst.WT = 8


adrian = Character("Adrian")
adrian.ST = 8
adrian.KO = 8
adrian.GE = 16
adrian.SN = 12
adrian.WT = 15


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




