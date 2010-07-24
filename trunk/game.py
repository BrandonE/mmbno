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

"""Contains the game's data."""

import os
from random import randint, shuffle
try:
    import simplejson as json
except ImportError:
    import json

from pyglet import clock, image, media, resource
from pyglet.gl import GL_QUADS
from pyglet.graphics import Batch, draw, OrderedGroup
from pyglet.sprite import Sprite
from pyglet.window import key, Window as Parent

from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver

__all__ = [
    'ChipFolderError', 'config', 'factory', 'GameProtocol',
    'InvalidChipcodeError', 'loader', 'loadmedia', 'Window'
]

config = json.loads(open('config.json').read())

class InvalidChipcodeError(Exception):
    """Raised when a given chip code for a chip is not in the list of valid
    chip codes.
    """
    pass

class ChipFolderError(Exception):
    """Raised when a given chipfolder does not have 30 chips, or has more than
    30 chips.
    """
    pass

class Window(Parent):
    def __init__(self, owner, **kwargs):
        """Creates the Pyglet Window."""
        self.owner = owner
        self.batch = Batch()
        super(Window, self).__init__(**kwargs)
        
        self.fx = loader(os.path.join('res', 'sound', 'fx'), loadmedia)
        self.groups = {}
        self.images = loader(os.path.join('res', 'images'), resource.image)
        self.sprites = {'icons': [], 'selected': [], 'stack': []}
        self.set_icon(
            image.load(
                os.path.join(
                    'res',
                    'images',
                    'icons',
                    '32x32.png'
                ).replace('\\', '/')
            )
        )
        player = media.Player()
        player.eos_action = player.EOS_LOOP
        if config['music']:
            source = resource.media(
                os.path.join(
                    'res',
                    'sound',
                    'music',
                    config['music']
                ).replace('\\', '/')
            )
            player.queue(source)
            player.play()

    def on_close(self):
        """Return true to ensure that no other handlers on the stack receive
        the on_close event"""
        reactor.callFromThread(reactor.stop)
        return True

    def on_draw(self):
        """Draw the screen."""
        self.clear()
        self.batch.draw()
        if (
            self.owner.ready and
            not self.owner.select and
            len(self.owner.winners()) != 1 and
            self.owner.custombar < 10
        ):
            rows = len(self.owner.field)
            cols = len(self.owner.field[0])
            width = 0
            if self.owner.custombar:
                width = 12.8 * self.owner.custombar
            x = (self.width / 2.0) - ((40 * cols) / 2.0) - 64 + (
                40 * (cols / 2.0)
            )
            y = (self.height / 2.0) - (((25 * rows) + 80) / 2.0) + 70 + (
                25 * rows
            )
            border = (120 / 255.0, 152 / 255.0, 216 / 255.0)
            draw(
                4,
                GL_QUADS,
                ('v2f', (x, y, x, y + 1, x + width, y + 1, x + width, y)),
                ('c3f', border * 4)
            )
            draw(
                4,
                GL_QUADS,
                (
                    'v2f',
                    (x, y + 5, x, y + 6, x + width, y + 6, x + width, y + 5)
                ),
                ('c3f', border * 4)
            )
            draw(
                4,
                GL_QUADS,
                (
                    'v2f',
                    (x, y + 1, x, y + 5, x + width, y + 5, x + width, y + 1)
                ),
                ('c3f', (224 / 255.0, 232 / 255.0, 248 / 255.0) * 4)
            )

class GameProtocol(LineReceiver):
    """Client for Twisted Server."""
    def battle(self):
        """Start the battle"""
        self.fx('send')
        # Finish the selection.
        self.select = False
        # Add the chips to the player.
        for chip in self.selected:
            self.character.chips.append(self.chips[chip])
        # Make the first selected the first used.
        self.character.chips.reverse()
        # Remove the chips from the library.
        self.selected.sort()
        for offset, chip in enumerate(self.selected):
            del self.chips[chip - offset]

    def characters(self):
        """Send this characters data."""
        self.send({
            'function': 'characters',
            'kwargs': {
                'player': self.player,
                'element': self.character.element,
                'health': self.character.health,
                'image': self.character.image,
                'maxhealth': self.character.maxhealth,
                'name': self.character.name,
                'status': list(self.character.status)
            }
        })

    def connectionMade(self):
        reactor.protocol = self
        self.ready = False
        self.field = []
        self.players = []
        self.window = Window(self, caption='MMBN Online', resizable=True)
        self.window.maximize()
        #self.images(self.window.images['characters'])
        @self.window.event
        def on_key_press(symbol, modifiers):
            """Handle key presses for Pyglet."""
            # If the player is prompted to select a chip
            if self.select:
                selection = self.selection
                if symbol == key.RETURN:
                    if not selection['row'] and selection['col'] == 5:
                        self.battle()
                    else:
                        self.fx('cursor')
                        selection['row'] = 0
                        selection['col'] = 5
                if symbol == key.UP or symbol == key.DOWN:
                    self.cursor(rows=1)
                if symbol == key.RIGHT:
                    self.cursor(cols=1)
                if symbol == key.LEFT:
                    self.cursor(cols=-1)
                if symbol == key.A:
                    chip = self.highlighted()
                    if not selection['row'] and selection['col'] == 5:
                        self.battle()
                    elif selection['row'] and selection['col'] == 3:
                        self.fx('shuffle')
                        self.shuffle()
                        self.shuffled = True
                    elif self.equipable(chip):
                        self.fx('select')
                        # Prepare to add the chip.
                        self.selected.append(chip)
                    else:
                        self.fx('invalid')
                if symbol == key.S and self.selected:
                    self.fx('cancel')
                    # Undo the selection.
                    self.selected.pop()
            else:
                if len(self.winners()) != 1:
                    row = self.character.row
                    col = self.character.col
                    if symbol == key.UP:
                        self.move(row, col, rows=1)
                    if symbol == key.DOWN:
                        self.move(row, col, rows=-1)
                    if symbol == key.RIGHT:
                        self.move(row, col, cols=1)
                    if symbol == key.LEFT:
                        self.move(row, col, cols=-1)
                    if symbol == key.A and self.character.chips:
                        self.character.usechip()
                    if symbol == key.S:
                        self.character.buster()
                    if symbol == key.D:
                        # Start the selection only if the custom bar is full.
                        if self.custombar == 10:
                            self.custom()
                    if symbol == key.F:
                        self.time()
                    if symbol == key.C:
                        self.character.charge()
                elif symbol == key.R:
                    self.send({'function': 'restart', 'kwargs': {}})
            self.draw()

        @self.window.event
        def on_resize(width, height):
            self.draw()

    def cursor(self, rows=0, cols=0):
        """Move the cursor for chip selection."""
        selection = self.selection
        old = selection.copy()
        chips = len(self.chips)
        if rows == 1:
            if selection['row']:
                selection['row'] = 0
                if selection['col'] == 3 and self.right:
                    selection['col'] = 4
                if self.highlighted() > chips - 1:
                    selection['row'] = 1
                    selection['col'] = 3
            elif (
                (
                    selection['col'] != 5 and
                    selection['col'] + 5 < chips and
                    config['extra']
                ) or
                (
                    selection['col'] in (3, 4) and
                    config['shuffle']
                )
            ):
                selection['row'] = 1
                if selection['col'] == 4 and config['shuffle']:
                    selection['col'] = 3
                    self.right = True
        elif cols == 1:
            if selection['col'] == 5 and self.chips:
                selection['col'] = 0
            elif (
                selection['row'] and (
                    selection['col'] == 3 or
                    (
                        selection['col'] == 2 and
                        not config['shuffle']
                    )
                )
            ):
                selection['row'] = 0
                selection['col'] = 5
            else:
                selection['col'] += 1
                if self.highlighted() > chips - 1:
                    if config['shuffle']:
                        if not selection['row']:
                            self.right = True
                        selection['row'] = 1
                        selection['col'] = 3
                    else:
                        selection['row'] = 0
                        selection['col'] = 5
        elif cols == -1:
            if selection['col'] == 5 and chips < 5 and config['shuffle']:
                selection['row'] = 1
                selection['col'] = 3
                self.right = True
            elif selection['col'] == 0:
                selection['row'] = 0
                selection['col'] = 5
            elif selection['row'] and selection['col'] == 3 and chips < 6:
                selection['row'] = 0
                selection['col'] = 2
            elif not selection['row'] or config['extra']:
                selection['col'] -= 1
            while self.highlighted() > chips - 1 and selection['col']:
                selection['col'] -= 1
            if not self.chips:
                selection['row'] = 0
                selection['col'] = 5
        if selection['row'] != 1 or selection['col'] != 3:
            self.right = False
        if self.selection != old:
            self.fx('cursor')

    def custom(self):
        """Redefine all the necessary values when prompting the custom bar."""
        self.fx('menu')
        self.custombar = 0
        self.character.chips = []
        self.right = False
        self.select = True
        self.selected = []
        self.selection = {'row': 0, 'col': 0}
        if not self.chips:
            self.selection['col'] = 5
            if config['shuffle']:
                self.selection['row'] = 1
                self.selection['col'] = 3
        self.shuffled = False

    def draw(self):
        """Draw the screen"""
        os.system('cls')
        # Graphically display a character or chip's element.
        elements = {'wind': 'A', 'none': 'N', 'plus': 'P'}
        if not self.ready:
            return
        # If the player is prompted to select a chip
        if self.select:
            # Display the chip selection.
            menu = 'Custom: '
            for index in range(0, len(self.chips)):
                if index == 8:
                    break
                chip = self.chips[index]
                menu += '|'
                cursor = '  '
                if index == self.selection:
                    cursor = '+ '
                menu += cursor
                power = ''
                if hasattr(chip, 'power'):
                    power = ' %s' % (chip.power)
                equipable = self.equipable(index)
                if equipable:
                    equipable = ' '
                else:
                    equipable = 'X'
                if not index in self.selected:
                    menu += '%s%s %s %s %s' % (
                        chip.name,
                        power,
                        elements[chip.element],
                        chip.code,
                        equipable
                    )
                else:
                    menu += '%s%s %s %s %s' % (
                        ' ' * len(chip.name),
                        ' ' * len(str(power)),
                        ' ' * len(elements[chip.element]),
                        ' ' * len(chip.code),
                        ' ' * len(equipable)
                    )
            if self.chips:
                menu += '|'
            print menu
        print 'Players: %s' % (len(self.players))
        # Display the custom bar.
        custom = ''
        # If the bar is full, display a message.
        if self.custombar >= 10:
            custom = ' Custom'
        print '%s%s' % (('*' * self.custombar), custom)
        grid = ''
        cols = len(self.field[0])
        top = []
        for col in range(0, cols):
            top.append('-----')
        top = ' '.join(top)
        for row in range(len(self.field) - 1, -1, -1):
            grid += '\n %s' % (top)
            grid += '\n|'
            for col in range(0, cols):
                panel = self.field[row][col]
                label = ' '
                blue = ' '
                coming = '>'
                going = '<'
                if self.flip:
                    coming = '<'
                    going = '>'
                status = {
                    'blank': 'X',
                    'broken': 'B',
                    'coming': coming,
                    'cracked': 'C',
                    'down': 'V',
                    'frozen': 'F',
                    'going': going,
                    'grass': 'G',
                    'holy': 'H',
                    'normal': ' ',
                    'poison': 'P',
                    'up': '^'
                }
                # Place all living characters.
                character = panel['character']
                if character:
                    player = self.players[character - 1]
                    if player and player['health']:
                        label = 'x'
                        # If the player is this character, change the symbol.
                        if character == self.player:
                            label = 'o'
                # Label a blue panels.
                if (col > (cols / 2.0) - 1) ^ panel['stolen']:
                    blue = 'B'
                grid += ' %s%s%s |' % (status[panel['status']], label, blue)
            grid += '\n %s' % (top)
        print grid
        for player in self.players:
            if player:
                print '\n%s' % (player['name'])
                print '-HP: %s' % (player['health'])
                print '-Status: %s' % (', '.join(player['status']))
                print '-Element: %s' % (player['element'])
        chips = []
        # Display the usable chips.
        for chip in self.character.chips:
            power = ''
            if hasattr(chip, 'power'):
                power = ' %s' % (chip.power)
            chips.append('%s%s %s' % (chip.name, power, elements[chip.element]))
        print '-Chips: %s' % (', '.join(chips))
        print '-Active Chip:'
        # Display the active chips.
        for type, chips in self.character.activechips.items():
            if chips:
                names = []
                if isinstance(chips, dict):
                    chips = list(
                        dict([(v, k) for (k, v) in chips.iteritems()])
                    )
                for chip in chips:
                    names.append(chip.name)
                print '--%s: %s' % (type, ', '.join(names))
        # If the game is over, display the winner prompt restarting.
        winners = self.winners()
        if not self.select and len(winners) == 1:
            print '\n%s wins! Press "r" to restart.' % (winners[0])
        print '\nControls:'
        print 'Directional Keys - Move Player / Chip Selection'
        print 'A: Use / Select Chip'
        print 'S: Use Buster / Remove Chip'
        print 'D: Prompt Chip Selection'
        print 'C: Charge Shot'
        print 'F: Go forward in time'
        print 'Enter: End Chip Selection'
        print 'Escape - End Game'
        player = self.players[self.player - 1]
        if not self.window.images:
            return
        self.window.batch = Batch()
        rows = len(self.field)
        cols = len(self.field[0])
        xcenter = (self.window.width / 2.0) - ((40 * cols) / 2.0)
        ycenter = (self.window.height / 2.0) - (((25 * rows) + 80) / 2.0)
        if self.select:
            if not 'menu' in self.window.sprites:
                self.window.sprites['menu'] = Sprite(
                    self.window.images['battle']['select']['menu'],
                    0,
                    0
                )
            menu = ((rows - 3) * 25)
            self.window.sprites['menu'].x = xcenter
            self.window.sprites['menu'].y = ycenter + menu
            self.window.sprites['menu'].group = self.group(rows + 1)
            self.window.sprites['menu'].batch = self.window.batch
            selection = self.highlighted()
            image = self.window.images['battle']['select']['standard']
            if isinstance(selection, int):
                image = self.window.images['battle']['select'][
                    self.chips[selection].classification
                ]
            if not 'classification' in self.window.sprites:
                self.window.sprites['classification'] = Sprite(image, 0, 0)
            self.window.sprites['classification'].image = image
            self.window.sprites['classification'].x = xcenter
            self.window.sprites['classification'].y = ycenter + 55 + menu
            self.window.sprites['classification'].group = self.group(rows + 1)
            self.window.sprites['classification'].batch = self.window.batch
            if isinstance(selection, int):
                image = self.window.images['chips']['big']
                classification = self.window.images['chips'][
                    self.chips[selection].classification
                ]
                chip = self.chips[selection].chip
                if chip in classification:
                    image = classification[chip]
            else:
                info = 'nodata'
                if self.selected:
                    info = 'sendchip'
                if self.selection['row'] and self.selection['col'] == 3:
                    info = 'shuffle'
                image = self.window.images['battle']['select']['info'][info]
            if not 'chip' in self.window.sprites:
                self.window.sprites['chip'] = Sprite(image, 0, 0)
            self.window.sprites['chip'].image = image
            self.window.sprites['chip'].x = xcenter + 15
            self.window.sprites['chip'].y = ycenter + 88 + menu
            self.window.sprites['chip'].group = self.group(rows + 2)
            self.window.sprites['chip'].batch = self.window.batch
            if isinstance(selection, int):
                image = self.window.images['chips']['elements'][
                    self.chips[selection].element
                ]
                if not 'element' in self.window.sprites:
                    self.window.sprites['element'] = Sprite(image, 0, 0)
                self.window.sprites['element'].image = image
                self.window.sprites['element'].x = xcenter + 25
                self.window.sprites['element'].y = ycenter + 73 + menu
                self.window.sprites['element'].group = self.group(rows + 2)
                self.window.sprites['element'].batch = self.window.batch
                if hasattr(self.chips[selection], 'power'):
                    if not 'power' in self.window.sprites:
                        self.window.sprites['power'] = []
                    string = str(self.chips[selection].power)
                    self.window.sprites['power'] = text(
                        string,
                        self.window.sprites['power'],
                        8,
                        self.window.images['fonts']['power'],
                        xcenter + 73 - (8 * len(string)),
                        ycenter + 74,
                        self.group(rows + 2),
                        self.window.batch
                    )
            cursor = 'chip'
            if not self.selection['row'] and self.selection['col'] == 5:
                cursor = 'ok'
            if self.selection['row'] and self.selection['col'] == 3:
                cursor = 'shuffle'
            image = self.window.images['battle']['select']['cursors'][cursor]
            if not 'frames' in image:
                image['frames'] = extract(image)
                image['index'] = 0
                clock.schedule_interval(animate, .13, image=image)
            image = image['frames'][image['index']]
            if not 'cursor' in self.window.sprites:
                self.window.sprites['cursor'] = Sprite(image, 0, 0)
            xoffset = self.selection['col']
            yoffset = 0
            if self.selection['row']:
                yoffset = -24
            self.window.sprites['cursor'].x = xcenter + 5 + (16 * xoffset)
            self.window.sprites['cursor'].y = ycenter + 37 + yoffset + menu
            if not self.selection['row'] and self.selection['col'] == 5:
                self.window.sprites['cursor'].x = xcenter + 89
                self.window.sprites['cursor'].y = ycenter + 25 + menu
            if self.selection['row'] and self.selection['col'] == 3:
                self.window.sprites['cursor'].x = xcenter + 55
                self.window.sprites['cursor'].y = ycenter + 7 + menu
            self.window.sprites['cursor'].image = image
            self.window.sprites['cursor'].group = self.group(rows + 3)
            self.window.sprites['cursor'].batch = self.window.batch
            if config['shuffle']:
                image = self.window.images[
                    'battle'
                ]['select']['shuffle']['on']
                if self.shuffled:
                    image = self.window.images[
                        'battle'
                    ]['select']['shuffle']['off']
                if not 'shuffle' in self.window.sprites:
                    self.window.sprites['shuffle'] = Sprite(image, 0, 0)
                self.window.sprites['shuffle'].image = image
                self.window.sprites['shuffle'].x = xcenter + 58
                self.window.sprites['shuffle'].y = ycenter + 10 + menu
                self.window.sprites['shuffle'].group = self.group(rows + 2)
                self.window.sprites['shuffle'].batch = self.window.batch
            for index, chip in enumerate(self.chips):
                if (index == 5 and not config['extra']) or index == 8:
                    break
                if not index in self.selected:
                    image = self.window.images['chips']['icon']
                    classification = self.window.images['chips'][
                        chip.classification
                    ]['icons']
                    if chip.chip in classification:
                        image = classification[chip.chip]
                    if len(self.window.sprites['icons']) < index + 1:
                        self.window.sprites['icons'].append(
                            Sprite(image, 0, 0)
                        )
                    xoffset = index
                    yoffset = 0
                    if xoffset > 4:
                        xoffset -= 5
                        yoffset = -24
                    thissprite = self.window.sprites['icons'][index]
                    thissprite.image = image
                    thissprite.color = (255, 255, 255)
                    if not self.equipable(index):
                        thissprite.color = (184, 184, 176)
                    thissprite.x = xcenter + 9 + (16 * xoffset)
                    thissprite.y = ycenter + 41 + (yoffset) + menu
                    thissprite.group = self.group(rows + 2)
                    thissprite.batch = self.window.batch
            for index, chip in enumerate(self.selected):
                icon = self.window.images['chips']['icon']
                selected = self.window.images['battle']['select']['selected']
                chip = self.chips[chip]
                classification = self.window.images['chips'][
                    chip.classification
                ]['icons']
                if chip.chip in classification:
                    icon = classification[chip.chip]
                if len(self.window.sprites['selected']) < index + 1:
                    self.window.sprites['selected'].append({
                        'icon': Sprite(icon, 0, 0),
                        'selected': Sprite(selected, 0, 0),
                    })
                thissprite = self.window.sprites['selected'][index]
                thissprite['icon'].image = icon
                thissprite['icon'].x = xcenter + 97
                thissprite['icon'].y = ycenter + 121 - (16 * index) + menu
                thissprite['icon'].group = self.group(rows + 3)
                thissprite['icon'].batch = self.window.batch
                thissprite['selected'].image = selected
                thissprite['selected'].x = xcenter + 93
                thissprite['selected'].y = ycenter + 120 - (16 * index)
                thissprite['selected'].group = self.group(rows + 2)
                thissprite['selected'].batch = self.window.batch
        elif len(winners) != 1:
            image = self.window.images['battle']['custom']['bar']
            if not 'bar' in self.window.sprites:
                self.window.sprites['bar'] = Sprite(image, 0, 0)
            self.window.sprites['bar'].image = image
            self.window.sprites['bar'].x = xcenter - 72 + (40 * (cols / 2.0))
            self.window.sprites['bar'].y = ycenter + 69 + (25 * rows)
            self.window.sprites['bar'].group = self.group(0)
            self.window.sprites['bar'].batch = self.window.batch
            if self.custombar >= 10:
                image = self.window.images['battle']['custom']['full']
                if not 'frames' in image:
                    image['frames'] = extract(image)
                    image['index'] = 0
                    clock.schedule_interval(animate, .09, image=image)
                image = image['frames'][image['index']]
                if not 'full' in self.window.sprites:
                    self.window.sprites['full'] = Sprite(image, 0, 0)
                self.window.sprites['full'].image = image
                self.window.sprites['full'].x = xcenter - 64 + (
                    40 * (cols / 2.0)
                )
                self.window.sprites['full'].y = ycenter + 70 + (25 * rows)
                self.window.sprites['full'].group = self.group(1)
                self.window.sprites['full'].batch = self.window.batch
            chips = self.character.chips[:]
            chips.reverse()
            for index, chip in enumerate(chips):
                x = xcenter + (40 * self.character.col) - (2 * index)
                y = ycenter + (25 * self.character.row) + (2 * index)
                border = self.window.images['battle']['misc']['iconborder']
                icon = self.window.images['chips']['icon']
                classification = self.window.images['chips'][
                    chip.classification
                ]['icons']

                if chip.chip in classification:
                    icon = classification[chip.chip]
                if len(self.window.sprites['stack']) < index + 1:
                    self.window.sprites['stack'].append({
                        'border': Sprite(border, 0, 0),
                        'icon': Sprite(icon, 0, 0)
                    })
                stack = self.window.sprites['stack'][index]
                group = rows + 1 + (
                    range(
                        len(self.character.chips) - 1,
                        -1,
                        -1
                    )[index]
                )
                stack['border'].image = border
                stack['border'].x = x + 19
                stack['border'].y = y + 66
                stack['border'].group = self.group(group)
                stack['border'].batch = self.window.batch
                stack['icon'].image = icon
                stack['icon'].x = x + 20
                stack['icon'].y = y + 67
                stack['icon'].group = stack['border'].group
                stack['icon'].batch = self.window.batch
        image = self.window.images['battle']['misc']['health']
        if not 'healthbox' in self.window.sprites:
            self.window.sprites['healthbox'] = Sprite(image, 0, 0)
        xoffset = -118
        if self.select:
            xoffset = 2
        self.window.sprites['healthbox'].image = image
        self.window.sprites['healthbox'].x = xcenter + xoffset + (
            40 * (cols / 2.0)
        )
        self.window.sprites['healthbox'].y = ycenter + 69 + (25 * rows)
        self.window.sprites['healthbox'].group = self.group(0)
        self.window.sprites['healthbox'].batch = self.window.batch
        if not 'health' in self.window.sprites:
            self.window.sprites['health'] = []
        string = str(self.character.health)
        self.window.sprites['health'] = text(
            string,
            self.window.sprites['health'],
            8,
            self.window.images['fonts']['health']['self'],
            self.window.sprites['healthbox'].x + 39 - (8 * len(string)),
            self.window.sprites['healthbox'].y + 3,
            self.group(1),
            self.window.batch
        )
        for row in range(0, rows):
            for col in range(0, cols):
                panel = self.field[row][col]
                x = xcenter + (40 * col)
                y = ycenter + (25 * row)
                if not self.select:
                    y += 13
                color = 'red'
                if (col > (cols / 2.0) - 1) ^ panel['stolen']:
                    color = 'blue'
                shading = 'middle'
                yoffset = 0
                if row == rows - 1 and rows > 1:
                    shading = 'top'
                if not row:
                    shading = 'bottom'
                    yoffset = -5
                image = self.window.images[
                    'panels'
                ][color][panel['status']][shading]
                if not 'sprite' in panel:
                    panel['sprite'] = Sprite(image, 0, 0, group=self.group(0))
                panel['sprite'].image = image
                panel['sprite'].x = x
                panel['sprite'].y = y + yoffset
                panel['sprite'].batch = self.window.batch
                character = panel['character']
                if character:
                    player = self.players[character - 1]
                    if player and player['health']:
                        if not 'sprites' in player:
                            player['sprites'] = {
                                'health': []
                            }
                        image = self.window.images['characters']['mega'][
                            player['image']
                        ]['0']
                        if not 'self' in player['sprites']:
                            player['sprites']['self'] = Sprite(image, 0, 0)
                        xoffset = 24
                        if (col > (cols / 2.0) - 1) ^ panel['stolen']:
                            image = image.get_transform()
                            image.anchor_x = image.width
                            image = image.get_transform(flip_x=True)
                            xoffset = 36
                        x = x - xoffset
                        y = y - 23
                        group = range(rows - 1, -1, -1)[row] + 1
                        player['sprites']['self'].image = image
                        player['sprites']['self'].x = x
                        player['sprites']['self'].y = y
                        player['sprites']['self'].group = self.group(group)
                        player['sprites']['self'].batch = self.window.batch
                        if character != self.player:
                            player['sprites']['health'] = text(
                                str(player['health']),
                                player['sprites']['health'],
                                8,
                                self.window.images['fonts']['health'][
                                    'opponent'
                                ],
                                x,
                                y,
                                self.group(group + 3),
                                self.window.batch
                            )

    def equipable(self, chip):
        """Check if a chip can be equipped."""
        # If the chip has already been selected, you have already selected
        # five, or the chip is out of range, then it is not equipable.
        selected = self.selected
        chips = len(self.chips)
        if chip in selected or len(selected) > 4 or chip > chips - 1:
            return
        # Add the chip in question to see if the new set fits the conditions.
        self.selected.append(chip)
        codes = set([])
        names = set([])
        success = True
        for chip in self.selected:
            thischip = self.chips[chip]
            if thischip.code != '*':
                codes.add(thischip.code)
            names.add(thischip.name)
            # If you have two different names and two different codes, fail.
            if len(names) > 1 and len(codes) > 1:
                success = False
                break
        # Remove the chip.
        self.selected.pop()
        return success

    def fx(self, fx):
        if not config['fx']:
            return
        self.window.fx[fx].play()

    def group(self, group):
        if not group in self.window.groups:
            self.window.groups[group] = OrderedGroup(group)
        return self.window.groups[group]

    def highlighted(self):
        """Get the highlighted chip from the position on the selection screen.
        """
        selection = self.selection['col']
        if (selection == 5 or (self.selection['row'] and selection == 3)):
            return
        if self.selection['row']:
            selection += 5
        return selection

    def hit(self, row, col, power, element='none', flinch=True):
        """Handle damage."""
        self.send({
            'function': 'hit',
            'kwargs': {
                'row': row,
                'col': col,
                'flip': self.flip,
                'power': power,
                'element': element,
                'flinch': flinch
            }
        })

    def images(self, iterable):
        for value in iterable:
            if isinstance(iterable[value], dict):
                self.images(iterable[value])
            else:
                data = iterable[value].get_image_data()
                self.send(
                    {
                        'function': 'images',
                        'kwargs': {
                            'player': self.player,
                            'images': {
                                'data': data.get_data(data.format, data.pitch),
                                'format': data.format,
                                'height': data.height,
                                'pitch': data.pitch,
                                'width': data.width
                            }
                        }
                    },
                    encoding='ISO-8859-1'
                )

    def lineReceived(self, line):
        """When a JSON encoded message is received, run the specified
        callback function with its kwargs (if any) on the callable object.
        """
        line = json.loads(line)
        callable = self
        if line['object'] == 'character':
            callable = self.character
        for index, value in line['kwargs'].items():
            del line['kwargs'][index]
            line['kwargs'][str(index)] = value
        getattr(callable, line['function'])(**line['kwargs'])
        self.draw()

    def loadcharacter(self, row, col):
        self.chips = json.loads(
            open(
                os.path.join(
                    'chips',
                    'folders',
                    '%s.json' % (config['chipfolder'])
                )
            ).read()
        )
        if len(self.chips) != 30:
            raise Exception('Your chip folder must have exactly 30 chips.')
        name = 'characters.%s' % (config['character'],)
        module = __import__(name, globals(), locals(), ('Character',), -1)
        self.character = module.Character(self)
        # Convert the list of chip names and codes to a list of chip instances.
        for index, chip in enumerate(self.chips):
            name = 'chips.%s' % (chip['chip'])
            module = __import__(name, globals(), locals(), ('Chip',), -1)
            self.chips[index] = module.Chip(self.character)
            if not chip['code'] in self.chips[index].codes:
                raise InvalidChipcodeError(
                    'Invalid chip code %(code)s for chip (%chip)s' % chip
                )
            self.chips[index].chip = chip['chip']
            self.chips[index].code = chip['code']
        self.character.row = row
        self.character.col = col
        if self.flip:
            self.character.col = range(len(self.field[0]) - 1, -1, -1)[col]

    def move(self, row, col, rows=0, cols=0, force=False):
        """Move the player if possible."""
        self.send({
            'function': 'move',
            'kwargs': {
                'sender': self.player,
                'row': row,
                'col': col,
                'flip': self.flip,
                'rows': rows,
                'cols': cols,
                'force': force
            }
        })

    def panel(self, row, col, status=None, stolen=None):
        """Change a panel."""
        self.send({
            'function': 'panel',
            'kwargs': {
                'row': row,
                'col': col,
                'flip': self.flip,
                'status': status,
                'stolen': stolen
            }
        })

    def send(self, line, **kwargs):
        """Messages are always to be sent as a JSON string.  In the case that
        a dictionary is being passed to this function, it should be formatted
        like so:

        {
            'function': 'panel',
            'kwargs': {}
        }

        Where 'function' is the name of the callback function, and 'kwargs'
        being the keyword arguments.  
        """
        self.sendLine(json.dumps(line, **kwargs))

    def shuffle(self):
        """Shuffle the chips."""
        chips = []
        for index in self.selected:
            chips.append((index, self.chips[index]))
        self.selected.sort()
        for offset, index in enumerate(self.selected):
            del self.chips[index - offset]
        shuffle(self.chips)
        for chip in chips:
            self.chips = self.chips[0:chip[0]] + [chip[1]] + (
                self.chips[chip[0]:len(self.chips)]
            )

    def start(self, field, row, col, flip, player):
        """Set up the data for the beginning of the game."""
        self.flip = flip
        self.player = player
        players = [{} for index in range(0, player)]
        self.update(field, players)
        self.loadcharacter(row, col)
        self.custom()
        self.shuffle()
        self.characters()
        self.ready = True

    def time(self):
        """Handle a unit of time."""
        # Fill the custom bar if not full.
        if self.custombar != 10:
            self.custombar += 1
        self.send({'function': 'time', 'kwargs': {}})
        # Have the player and opponent run handle a unit of time.
        self.character.time()

    def update(self, field, players):
        """Update the game data."""
        # If you are on the other side, then reverse the panels.
        if self.flip:
            for row in field:
                row.reverse()

        # If we already have a field, then update it.  In the case that there
        # is no field, such as when a player has connected, then create it.
        if self.field:
            for row in range(0, len(field)):
                for col in range(0, len(field[0])):
                    for index, value in field[row][col].items():
                        # Update the value for this row's columns.
                        self.field[row][col][index] = value
        else:
            self.field = field

        for player in range(0, len(players)):
            if len(self.players) > player:
                for index, value in players[player].items():
                    self.players[player][index] = value
            else:
                self.players.append(players[player])

        # Update the player numbers.
        while len(self.players) > len(players):
            self.players.pop()
            if len(self.players) < self.player:
                self.player -= 1

    def winners(self):
        winners = []
        for player in self.players:
            if player and player['health']:
                winners.append(player['name'])
        return winners

def animate(dt, image):
    if image['index'] == len(image['frames']) - 1:
        image['index'] = -1
    image['index'] += 1
    reactor.protocol.draw()

def extract(image):
    images = image.copy()
    delete = []
    for index, frame in images.items():
        images[int(index)] = frame
        delete.append(index)
    for index in delete:
        del images[index]
    frames = []
    for frame in images.items():
        frames.append(frame[1])
    return frames

def loader(path, function):
    """Load resources from a directory recursively."""
    items = {}
    for item in os.listdir(path):
        name, ext = os.path.splitext(item)
        if name:
            if ext:
                items[name] = function(
                    os.path.join(
                        path,
                        '%s%s' % (name, ext)
                    ).replace('\\', '/')
                )
            elif not name.startswith('.'):
                items[name] = loader(os.path.join(path, name), function)
    return items

def loadmedia(path):
    return media.load(path, streaming=False)

def text(characters, sprites, spacing, font, x, y, group, batch):
    for index, character in enumerate(characters):
        image = font[character]
        if index > len(sprites) - 1:
            sprites.append(Sprite(image, 0, 0))
        sprites[index].image = image
        sprites[index].x = x + (index * spacing)
        sprites[index].y = y
        sprites[index].group = group
        sprites[index].batch = batch
    return sprites

factory = protocol.ClientFactory()
factory.protocol = GameProtocol
if __name__ == '__main__':
    from reactor import reactor
    reactor.connectTCP(config['ip'], config['port'], factory)
    reactor.run()