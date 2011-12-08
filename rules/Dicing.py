#!/usr/bin/python
# -*- coding: utf-8
from __future__ import division, print_function

import numpy as np
import numpy.random as npr

def roll(poolSize):
    """
    Würfelt einen Pool der gegebenen größe mit evtl. nachwürfeln und gibt ein np-array mit den Ergebnissen zurück.
    """
    result = npr.randint(0,10, size = poolSize)
    for i, r in enumerate(result) :
        if r == 9 :
            a = npr.randint(0,10)
            r += a
            while a == 9:
                a = npr.randint(0,10)
                r += a
            result[i] = r
    return result
            
def isLucky(rolls, difficulty):
    """
    Überprüft ob ein Wurf ein glücklicher Erfolg ist.
    """
    assert len(rolls) >= 1
    return rolls[0] >= difficulty + 9

def getNumberOfSuccesses(rolls, difficulty):
    """
    Bestimmt die Anzahl der Erfolge eines Wurfes
    """
    s = len(rolls[rolls>=difficulty])
    if isLucky(rolls, difficulty) :
        s *= 2
    return s

def isSuccessful(rolls, difficulty, requiredSuccesses = 1):
    return getNumberOfSuccesses(rolls, difficulty) >= requiredSuccesses

def isBotch(rolls, difficulty):
    return getNumberOfSuccesses(rolls, difficulty) == 0 and rolls[0] == 0


def doAVerboseRoll(poolsize, difficulty, requiredSuccesses):
    r = roll(poolsize)
    print("Rolled:", r)
    successes = r[r >= difficulty]
    print(getNumberOfSuccesses(r, difficulty), "Successes:", successes)
    print("Alpha-Die:", r[0])
    if isLucky(r, difficulty):
        print("LUCKY!!")
    if isBotch(r, difficulty):
        print("BOTCH!!")
    if isSuccessful(r, difficulty, requiredSuccesses):
        print("=> Check passed")
    else :
        print("=> Failed")

