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

import os
import random

from pyglet import window, image, media, resource
from pyglet.graphics import Batch
from pyglet.sprite import Sprite

from mmbno import config
from mmbno.helpers import get_absolute, get_relative

class Field(window.Window):
    def __init__(self, background = 'acdc'):
        """Create 6 * 3 list of lists and act as grid to set panel state.
        The structure goes like so: self.grid[x2][y2][index]
        x2 and y2 being the relative x and y coordinates.
        index Values:
        instance - object - Obstacle() or Navi() instance occupying the panel.
        color - string - Panel Color (red, blue)
        status - string - Panel Status (fixed, damaged, broken, sanctuary,
        poison)
        """
        super(Field, self).__init__(width=256, height=192,
            caption='MMBNOnline')
        # Create a list that represents the total of number of panels in the
        # arena.
        self.grid = []
        for x in range(0, 6):
            column = []
            for y in range(0, 3):
                column.append({'instance': 0, 'color': 0, 'status': 0})
            self.grid.append(column)
        # Load necessary resources.
        resources_dir = 'mmbno/res/'
        self.load_background(resources_dir, background)
        self.load_panels(resources_dir)
        self.load_music(resources_dir)

    def on_draw(self):
        """First the screen is cleared, then the background and panels are
        drawn on the field."""
        self.clear()
        #self.draw_background()
        self.draw_panels()

    def draw_background(self):
        """Draw a background that tiles vertically and horizontally on
        the screen.
        """
        batch = Batch()
        background = self.background
        backgrounds = [Sprite(background, x=0, y=0, batch=batch),
                    Sprite(background, x=0, y=64, batch=batch),
                    Sprite(background, x=0, y=128, batch=batch),
                    Sprite(background, x=0, y=192, batch=batch),
                    Sprite(background, x=128, y=0, batch=batch),
                    Sprite(background, x=128, y=64, batch=batch),
                    Sprite(background, x=128, y=128, batch=batch),
                    Sprite(background, x=128, y=192, batch=batch)]
        batch.draw()

    def draw_panels(self):
        panels = Batch()
        panel = []
        for i in range(0, 18):
            if i > 8:
                color = self.panels['fixed_blue']
                xoffset = 120
                yoffset = 9
            else:
                color = self.panels['fixed_red']
                xoffset = 0
                yoffset = 0

            x = ((i + 3) % 3) * 40 + xoffset
            y = 87 + (24 * ((i - yoffset) / 3))
            x2, y2 = get_relative(x, y)
            self.grid[x2][y2]['instance'] = None
            self.grid[x2][y2]['color'] = 'blue'
            self.grid[x2][y2]['status'] = 'fixed'

            if color == self.panels['fixed_red']:
                 self.grid[x2][y2]['color'] = 'red'

            panel.append(Sprite(color, x, y, batch=panels))
        panels.draw()

    def load_background(self, path, background):
        path = path + 'images/backgrounds'
        img = resource.image('%s/%s.png' % (path, background))
        grid = image.TextureGrid(image.ImageGrid(img, columns=1,
                rows=7, item_width=128, item_height=64))
        self.background = grid.get_animation(2, loop=True)

    def load_music(self, path):
        path = path + 'music'
        filename = 'battle_%i.ogg' % (random.randint(1, 11))
        player = media.Player()
        player.eos_action = player.EOS_LOOP
        source = resource.media('%s/%s' % (path, filename))
        player.queue(source)
        player.play()

    def load_panels(self, path):
        """Loads all panel images."""
        self.panels = {}
        path = path + 'images/panels'
        for panel in os.listdir(path):
            key = panel.split('.')[0]
            self.panels[key] = resource.image('%s/%s' % (path, panel))


field = Field()

class Character(Sprite):
    """This class will act as the base for all instances, also being a
    sub-class of pyglet.sprite.Sprite.

    x2 and y2 are relative coordinates. The values are useless on their
    own, meaning that you must pass them through the get_absolute
    function in order to fetch the real x and y values for positioning.
        
    If no relative coordinates are supplied, then the Navi is positioned
    at the center of the field.

    An ImageGrid will be used, one for each type of sprite. The spacing
    between the images must be the same for each row, for alignment
    purposes."""

    def __init__(self, obj, panels, x2, y2):
        _x, _y = get_absolute(x2, y2)
        super(Character, self).__init__(image.load(obj['file']), _x, _y,
            batch=None)
        self.x2, self.y2 = x2, y2
        self.status = 'normal'
        self.panels = 'red'
        if panels in ('red', 'blue'):
            self.panels = panels

    def can_move(self, x2, y2):
        """Determines if a Navi may move from a designated area to
        the next, after evaluating these conditions:

        (1) Are the relative coordinates valid?
        (2) Is the designated area's panel color differing from what the
            panels attribute is set to?
        (3) Is the panel broken?
        (4) Is the panel occupied?
        (5) Is the instance immobilized?
        
        If one of the above conditions are False, then True is returned."""

        if (((x2 < 0 or x2 > 5) or (y2 < 0 or y2 > 2))
        or (field.grid[x2][y2]['instance'] != None)
        or (field.grid[x2][y2]['color'] != self.panels)
        or (field.grid[x2][y2]['status'] == 'broken')
        or (self.status == 'paralyzed')):
            return

        return True

    def _move(self, x2, y2):
        # Empty the previous panel so that the new one is now occupied by
        # this instance.
        field.grid[self.x2][self.y2]['instance'] = None
        field.grid[x2][y2]['instance'] = self
        # Update the relative and absolute coordinates
        self.x2, self.y2 = x2, y2
        self.x, self.y = get_absolute(self.x2, self.y2)


class Navi(Character):
    def __init__(obj, panels='red', x2=5, y2=2):
        pass

    def move(self, symbol):
        """Define the keys needed to move the navi, granted the
        Navi is allowed to move.

        After checking which arrow key was pressed, a function is run to
        check if the Navi instance is allowed to move. The function just
        returns if this condition is false. Once the relative coordinate is
        added, then the previous panel that we were on is set to a vacant
        state.

        The relative coordinate attributes are then updated. The animation
        sequence then takes place, and the Navi moves to the designated
        panel after getting the absolute coordinates."""
        x2, y2 = self.x2, self.y2
        key = field.key
        if ((symbol == key.UP and not self.can_move(x2, y2 + 1))
        or (symbol == key.DOWN and not self.can_move(x2, y2 - 1))
        or (symbol == key.DOWN and not self.can_move(x2, y2 - 1))
        or (symbol == key.LEFT and not self.can_move(x2 - 1, y2))
        or (key.RIGHT and self.can_move(x2 + 1, y2))):
            return

        if symbol == key.UP:
            y2 += 1
        if symbol == key.DOWN:
            y2 -= 1
        if symbol == key.LEFT:
            x2 -= 1
        if symbol == key.RIGHT:
            x2 += 1
        self._move(x2, y2)


class Obstacle(Character):
    def __init__(self, obstacle, x, y):
        self.image = image.load('res/images/obstacle/%s.png' % (obstacle,))
        self.health = 50


class Virus(Character):
    def __init__(self):
        pass
