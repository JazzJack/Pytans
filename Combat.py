#!/usr/bin/python
# encoding: utf-8

from __future__ import division, print_function
import heapq

class Combat:
    def __init__(self, arena, players):
        self.arena = arena
        self.players = players

    def combatRound(self):
        # Determine the succession
        succession = []
        for player in self.players:
            succession.append((-player.character.AP, player, True))
        heapq.heapify(succession)
        # Call the players
        while len(succession):
            playerTuple = heapq.heappop(succession)
            # Option to wait
            if playerTuple[2]:
                waittime = playerTuple[1].wait()
                if waittime > 0:
                    heapq.heappush((-playerTuple[1].character.AP, playerTuple[1], False))
                    continue
            # Act
            playerTuple[1].act()

    def oneTeamWins(self):
        livingCharsInTheseTeams = set()
        for team in self.arena.teams:
            for character in self.arena.teams[team]:
                if character.isAlive():
                    livingCharsInTheseTeams.add(team)
        return len(livingCharsInTheseTeams)<=1


    def fightTillDefeat(self):
        # Start combat
        for player in self.players:
            player.doInitiative()
        # Simulate Rounds
        while True:
            self.combatRound()
            if self.oneTeamWins():
                return "One team wins!"