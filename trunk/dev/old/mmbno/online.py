#
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
#
# Copyright (C) 2008-2009 Chris Santiago
# http://mmbnonline.net/

"""Twisted Factory and Protocol classes for in-game use."""

from twisted.internet.protocol import Protocol, ClientFactory, ServerFactory

class RegistryProtocol(Protocol):

    def dataReceived(self, data):
        print "Server said:", data
        self.transport.loseConnection()

    def connectionLost(self, reason):
        print 'Lost connection to server registry.'

    def connectionMade(self):
        self.transport.write('Hiii')

    def clientConnectionFailed(self, connector, reason):
        self.transport.write('Connection failed: %s' % (reason,))

    def connectionMade(self):
        self.transport.write('Connected to server registry: Olympus (%s)' % 
            (config['registry.host'],))

    def dataReceived(self, data = ''):
        print data


class GameServerProtocol(Protocol):

    def connectionMade(self):
        self.factory.connected = self.factory.connected + 1
        if self.factory.connected > 100:
            self.transport.write('Max user quota (100 users) exceeded. \
                Please come on at a later time.')
            self.transport.loseConnection()

    def clientConnectionLost(self, connector, reason):
        self.factory.connected = self.factory.connected - 1
        print 'Lost connection: %s' % (reason,)

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed: ' % (reason,)


class Registry(ServerFactory):
    protocol = RegistryProtocol()

class RegistryClient(ClientFactory):
    protocol = RegistryProtocol()

class GameServer(ServerFactory):
    protocol = GameServerProtocol()