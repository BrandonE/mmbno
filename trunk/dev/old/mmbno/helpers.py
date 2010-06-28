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

"""These are just helper functions that just don't deserve to be in a specific class.
Most of the functions here just perform calculations and whatnot."""

from hashlib import md5

def get_absolute(x2, y2):
    """Calculate absolute x and y coordinates based on x and y."""
    x, y = (0, 0)
    if x2 in (0, 1, 2, 3, 4, 5):
        x = 20 + (40 * x2)
    if y2 in (0, 1, 2):
        y = 87 + 12 + (24 * y2)
    return (x, y)

def get_relative(x, y):
    """Performs a reverse operation in order to calculate the relative
    coordinates from the absolute."""
    x2, y2 = (0, 0)
    if x in (0, 40, 80, 120, 160, 200):
        x2 = abs((20 - x) / 40)
    if y in (87, 111, 135):
        y2 = abs((99 - y) / 24)
    return (x2, y2)

def get_hash(string):
    """Generates a salt and a password hash for more secure authentication."""
    return md5(''.join(string, md5(string)))
