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

__all__ = ['move', 'hit', 'update']

def move(character, rows = 0, cols = 0, blue = config['blue'], force = False):
    """Move the character if possible."""
    reactor.protocol.send({
        'function': 'move',
        'id': character.id,
        'kwargs': {
            'rows': rows,
            'cols': cols,
            'blue': blue,
            'force': force
        },
        'object': 'character'
    })

def hit(character, power, type = 'none'):
    reactor.protocol.send({
        'function': 'hit',
        'id': character.id,
        'kwargs': {
            'power': power,
            'type': type
        },
        'object': 'character'
    })

def update(callable, name):
    """Update the character's properties"""
    message = {
        'function': 'update',
        'kwargs': {},
        'object': name
    }
    if name == 'character':
        message['id'] = callable.id
        message['kwargs'] = {
            'health': callable.health,
            'maxhealth': callable.maxhealth,
            'name': callable.name,
            'power': callable.power,
            'status': list(callable.status),
            'type': callable.type
        }
    if name == 'game':
        message['kwargs'] = {'field': []}
        for row in callable.field[:]:
            cols = []
            for panel in row[:]:
                panel = panel.copy()
                if panel['character']:
                    panel['character'] = panel['character'].id
                cols.append(panel)
            message['kwargs']['field'].append(cols)
    reactor.protocol.send(message)