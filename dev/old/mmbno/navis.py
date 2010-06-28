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

"""
This "module" is a collection of dicts with information to pass to the `mmbno.arena.Navi`
class.

Each dict is composed of:

anchor (list/tuple) - x and y coordinates from where the sprite is drawn. Commonly
found in shadows.

file (string) - is path for the navi sprite sheet to be used.

size (list/tuple) - width and height of all of the sprites.

sprites (list/tuple) - list of lists formatted as such:
        ('position', row, starting frame, ending frame)
    'position' may be: stand, move, shoot, sword, bomb, cast
"""

dustman = {
    'anchor': [100, 100],
    'columns': 5,
    'file': 'res/images/navi/dustman.png',
    'rows': 9,
    'size': [100, 100],
    'sprites': {
        'stand': [1, 2],
        'move': [2, 4],
        'bomb': [9, 14],
        'shoot': [15, 18],
        'cast': [19, 22]
    }
}