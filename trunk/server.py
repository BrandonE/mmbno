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

    def connectionLost(self, reason):
        print 'Client Disconnected.'
        self.factory.players.remove(self)

    def lineReceived(self, line):
        line = json.loads(line)
        if self.factory.queue:
            if line == 'Reset':
                self.factory.queue = False
            return
        self.factory.queue = True
        # Send a message to every player.
        line['reset'] = False
        for key, player in enumerate(self.factory.players):
            # Allow more messages if the last player has handled it.
            if key == len(self.factory.players) - 1:
                line['reset'] = True
            player.sendLine(json.dumps(line))

factory = ServerFactory()
factory.protocol = GameProtocol
factory.players = []
factory.queue = False
application = service.Application('mmbnonline')
server = internet.TCPServer(9634, factory)
server.setName('MMBN Online Server')
server.setServiceParent(application)