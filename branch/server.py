# -*- coding: utf-8 -*-
# This file is part of MMBN Online
# MMBN Online is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# MMBN Online is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with MMBN Online.  If not, see <http://www.gnu.org/licenses/>.

# Copyright (C) 2008-2010 Chris Santiago and Brandon Evans.
# http://mmbnonline.net/

"""Create the Twisted server."""

try:
    import simplejson as json
except ImportError:
    import json

from twisted.protocols.basic import LineReceiver
from twisted.application import internet, service
from twisted.internet.protocol import ServerFactory

__all__ = ['application', 'factory', 'GameProtocol', 'server']

class GameProtocol(LineReceiver):
    def connectionMade(self):
        print 'Client Connected.'
        self.factory.players.append(self)
        player = len(self.factory.players)
        self.factory.players[player - 1].row = 1
        self.factory.players[player - 1].col = 1
        flip = False
        if not field[1][1]['character']:
            field[1][1]['character'] = player
        else:
            field[1][4]['character'] = player
            self.factory.players[player - 1].col = 4
            flip = True
        self.sendone(
            {
                'function': 'start',
                'kwargs': {'field': field, 'flip': flip, 'players': player},
                'object': 'game'
            },
            player
        )

    def connectionLost(self, reason):
        print 'Client Disconnected.'
        self.factory.players.remove(self)
        field[self.row][self.col]['character'] = None
        self.update()

    def sendone(self, line, player):
        """Send a message to one player."""
        line = json.dumps(line)
        self.factory.players[player - 1].sendLine(line)

    def sendall(self, line):
        """Send a message to every player."""
        line = json.dumps(line)
        for player in self.factory.players:
            # Allow more messages if the last player has handled it.
            player.sendLine(line)

    def lineReceived(self, line):
        line = json.loads(line)
        for key, value in line['kwargs'].items():
            del line['kwargs'][key]
            line['kwargs'][str(key)] = value
        getattr(self, line['function'])(**line['kwargs'])
        self.update()

    def move(self, player, info, rows, cols, force):
        """Move the character if possible."""
        character = self.factory.players[player - 1]
        # Grab the panel the character is on.
        panel = field[character.row][character.col]
        if info['flip']:
            cols = -cols
        # Define the new coordinates.
        newrow = character.row - rows
        newcol = character.col + cols
        if not force:
            # If the new coordinates aren't on the field, fail.
            if newrow < 0 or newrow > 2 or newcol < 0 or newcol > 5:
                return
        # As the coordinates are valid, grab the new panel.
        newpanel = field[newrow][newcol]
        if not force:
            # If the panel doesn't contain the character, something went
            # horribly wrong.
            if panel['character'] != player:
                raise Exception('Field desync')
            # If the new panel is out of bounds, contains a character, is
            # broken without the character having airshoes, or the character is
            # paralyzed, fail.
            if (
                (
                    ((newcol > 2) ^ newpanel['stolen']) ^
                    info['flip']
                ) or
                newpanel['character'] or
                (
                    newpanel['status'] == 'broken' and
                    not 'airshoes' in info['status']
                ) or
                'paralyzed' in info['status']
            ):
                return
        # Empty the old panel.
        panel['character'] = None
        # Add the character to the new panel.
        newpanel['character'] = player
        fire = False
        if not 'floatshoes' in info['status']:
            # If the panel is cracked and the character moved, break it.
            if (
                panel['status'] == 'cracked' and
                (character.row != newrow or character.col != newcol)
            ):
                panel['status'] = 'broken'
            # If the character moved onto a lava panel and is not a fire type
            if newpanel['status'] == 'lava' and self.type != 'fire':
                fire = True
                # Revert the panel.
                newpanel['status'] = 'normal'
        # Adjust to the new coordinates.
        character.row = newrow
        character.col = newcol
        self.sendone(
            {
                'function': 'move',
                'kwargs': {'fire': fire},
                'object': 'character'
            },
            player
        )
        if not 'floatshoes' in info['status'] and not force:
            # Slide if on ice.
            if newpanel['status'] == 'ice':
                self.move(character, rows, cols, flip, force)

    def update(self):
        self.sendall({
            'function': 'update',
            'kwargs': {'field': field, 'players': len(self.factory.players)},
            'object': 'game'
        })

field = []
for row in range(0, 3):
    cols = []
    for col in range(0, 6):
        character = None
        panel = {
            'character': character,
            'stolen': False,
            'status': 'normal',
            'time': 0
        }
        cols.append(panel)
    field.append(cols)
factory = ServerFactory()
factory.protocol = GameProtocol
factory.players = []
factory.queue = False
application = service.Application('mmbnonline')
server = internet.TCPServer(9634, factory)
server.setName('MMBN Online Server')
server.setServiceParent(application)