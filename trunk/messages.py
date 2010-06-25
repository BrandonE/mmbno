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
        'client': config['client'],
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
        'client': config['client'],
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
        'client': config['client'],
        'function': 'update',
        'kwargs': {},
        'object': name
    }
    if name == 'character':
        message['id'] = callable.id
        message['kwargs'] = {
            'col': callable.col,
            'health': callable.health,
            'maxhealth': callable.maxhealth,
            'name': callable.name,
            'power': callable.power,
            'row': callable.row,
            'status': list(callable.status),
            'type': callable.type
        }
    if name == 'game':
        field = callable.field[:]
        message['kwargs'] = {'blue': config['blue'], 'field': []}
        for row in range(0, 3):
            field[row] = field[row][:]
            for col in range(0, 6):
                panel = field[row][col]
                panel = panel.copy()
                del panel['character']
    reactor.protocol.send(message)