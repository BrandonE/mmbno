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

"""Send messages to the Twisted Server."""

try:
    import simplejson as json
except ImportError:
    import json

from client import factory

__all__ = ['config', 'move']

config = json.loads(open('config.json').read())

def move(self, rows = 0, cols = 0, force = False):
    """Move the character if possible."""
    factory.protocol.sendLine({
        'blue': config['blue'],
        'col': self.col,
        'function': 'move',
        'kwargs': {'rows': rows, 'cols': -cols, 'force': force},
        'row': self.row
    })