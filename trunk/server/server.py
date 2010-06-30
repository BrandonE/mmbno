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

__all__ = ['application', 'config', 'factory', 'GameProtocol', 'server']

config = json.loads(open('config.json').read())

class GameProtocol(LineReceiver):
    def characters(self, player, health, name, status, type):
        """Send this characters data."""
        player = self.factory.players[player - 1]
        player.health = health
        player.name = name
        player.status = status
        player.type = type

    def connectionMade(self):
        print 'Client Connected.'
        self.factory.players.append(self)
        if len(self.factory.players) == 1:
            self.field()
        self.place(self.factory.players[len(self.factory.players) - 1])
        self.start()

    def connectionLost(self, reason):
        print 'Client Disconnected.'
        deleted = False
        for value in self.factory.players:
            if deleted and self.factory.field[
                value.row
            ][value.col]['character']:
                self.factory.field[value.row][value.col]['character'] -= 1
            if value == self:
                deleted = True
        self.factory.players.remove(self)
        self.factory.field[self.row][self.col]['character'] = None
        self.update()

    def field(self):
        """Create an empty field."""
        if config['rows'] < 1 or config['cols'] < 1 or config['cols'] % 2:
            raise Exception('Field dimensions invalid')
        self.factory.field = []
        for row in range(0, config['rows']):
            cols = []
            for col in range(0, config['cols']):
                panel = {
                    'character': None,
                    'stolen': False,
                    'status': 'normal',
                    'time': 0
                }
                cols.append(panel)
            self.factory.field.append(cols)

    def lineReceived(self, line):
        line = json.loads(line)
        for key, value in line['kwargs'].items():
            del line['kwargs'][key]
            line['kwargs'][str(key)] = value
        getattr(self, line['function'])(**line['kwargs'])
        self.update()

    def hit(self, row, col, flip, power, type, flinch):
        """Forward damage."""
        if flip:
            col = range(config['cols'] - 1, -1, -1)[col]
        player = self.factory.field[row][col]['character']
        if not player:
            return
        self.sendone(
            {
                'function': 'hit',
                'kwargs': {'power': power, 'type': type},
                'object': 'character'
            },
            player
        )

    def move(self, row, col, flip, info, rows, cols, force):
        """Move the character if possible."""
        if flip:
            col = range(config['cols'] - 1, -1, -1)[col]
        player = self.factory.field[row][col]['character']
        if not player:
            return
        character = self.factory.players[player - 1]
        # Grab the panel the character is on.
        panel = self.factory.field[character.row][character.col]
        if flip:
            cols = -cols
        # Define the new coordinates.
        newrow = character.row - rows
        newcol = character.col + cols
        if not force:
            # If the new coordinates aren't on the field, fail.
            if (
                newrow < 0 or
                newrow > config['rows'] - 1 or
                newcol < 0 or
                newcol > config['cols'] - 1
            ):
                return
        # As the coordinates are valid, grab the new panel.
        newpanel = self.factory.field[newrow][newcol]
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
                    (newcol > ((config['cols'] / 2) - 1)) ^
                    newpanel['stolen'] ^
                    character.flip
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
        self.update()
        self.sendone(
            {
                'function': 'move',
                'kwargs': {
                    'row': character.row,
                    'col': character.col,
                    'fire': fire
                },
                'object': 'character'
            },
            player
        )
        if not 'floatshoes' in info['status'] and not force:
            # Slide if on ice.
            if newpanel['status'] == 'ice':
                self.move(row, col, flip, info, rows, cols, force)

    def panel(self, row, col, flip, status, stolen):
        """Change a panel."""
        if flip:
            col = range(config['cols'] - 1, -1, -1)[col]
        panel = self.factory.field[row][col]
        if status != None:
            panel['status'] = status
        if stolen != None:
            panel['stolen'] = stolen

    def place(self, player):
        """Place a character."""
        length = len(self.factory.players)
        player.row = 0
        player.col = 0
        player.flip = False
        if not self.factory.field[0][0]['character']:
            self.factory.field[0][0]['character'] = length
        else:
            self.factory.field[0][config['cols'] - 1]['character'] = length
            player.col = config['cols'] - 1
            player.flip = True

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

    def start(self):
        length = len(self.factory.players)
        player = self.factory.players[length - 1]
        self.sendone(
            {
                'function': 'start',
                'kwargs': {
                    'field': self.factory.field,
                    'row': player.row,
                    'col': player.col,
                    'flip': player.flip,
                    'player': length
                },
                'object': 'game'
            },
            length
        )

    def time(self):
        """Handle a unit of time."""
        for row in self.factory.field:
            for panel in row:
                # If the panel is broken
                if panel['status'] == 'broken':
                    # Prepare to restore.
                    panel['time'] += 1
                    # Restore if ready.
                    if panel['time'] == 10:
                        panel['status'] = 'normal'
                        panel['time'] = 0

    def restart(self):
        self.field()
        for value in self.factory.players:
            self.place(value)
        self.sendall({
            'function': '__init__',
            'kwargs': {},
            'object': 'character'
        })
        self.sendall({'function': 'custom', 'kwargs': {}, 'object': 'game'})

    def update(self):
        """Update the game data."""
        players = []
        for value in self.factory.players:
            players.append({
                'health': value.health,
                'name': value.name,
                'status': value.status,
                'type': value.type
            })
        self.sendall({
            'function': 'update',
            'kwargs': {
                'field': self.factory.field,
                'players': players
            },
            'object': 'game'
        })

factory = ServerFactory()
factory.protocol = GameProtocol
factory.players = []
factory.queue = False
application = service.Application('mmbnonline')
server = internet.TCPServer(config['port'], factory)
server.setName('MMBN Online Server')
server.setServiceParent(application)