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
 
"""Client for Twisted Server."""
 
try:
    import simplejson as json
except ImportError:
    import json
 
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ClientFactory
from game import config, game

__all__ = ['factory', 'GameClient']

class GameClient(LineReceiver):
    def connectionMade(self):
        game.protocol = self

    def lineReceived(self, line):
        line = json.loads(line)
        if 'blue' in line and config['blue'] != line['blue']:
            line['col'] = range(5, -1, -1)[line['col']]
            if line['function'] == 'move':
                line['rows'] = -line['rows']
        getattr(
            game.field[line['row']][line['col']]['character'],
            line['function']
        )(**line['kwargs'])
 
factory = ClientFactory()
factory.protocol = GameClient