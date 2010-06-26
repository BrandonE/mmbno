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

"""Handles sending of Twisted messages."""

from twisted.internet import reactor

from config import config

def move(player, character, rows = 0, cols = 0, force = False):
    """Move the player if possible."""
    reactor.protocol.send({
        'function': 'move',
        'kwargs': {
            'cols': cols,
            'force': force,
            'info': {
                'flip': character.owner.flip,
                'status': list(character.status),
                'type': character.type
            },
            'player': player,
            'rows': rows,
        }
    })