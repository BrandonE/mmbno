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
import shutil
from random import randint, shuffle
from ConfigParser import ConfigParser
try:
    import simplejson as json
except ImportError:
    import json

from pyglet import media, resource
from pyglet.window import key, Window as Parent
from pyglet.graphics import Batch, OrderedGroup
from pyglet.sprite import Sprite
from reactor import reactor
from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver

__all__ = [
    'config', 'factory', 'GameProtocol', 'get_absolute', 'get_relative',
    'Window'
]

config = json.loads(open('config.json').read())


class Window(Parent):
    def __init__(self, owner, **kwargs):
        """Creates the Pyglet Window."""
        self.owner = owner
        self.batch = Batch()
        super(Window, self).__init__(**kwargs)
        self.images = loader(os.path.join('res', 'images'))
        self.sprites = {
            'icons': []
        }
        player = media.Player()
        player.eos_action = player.EOS_LOOP
        source = resource.media(
            os.path.join(
                'res',
                'sound',
                'music',
                'battle_%i.ogg' % randint(1, 11)
            ).replace('\\', '/')
        )
        player.queue(source)
        #player.play()

    def on_close(self):
        """Return true to ensure that no other handlers on the stack receive
        the on_close event"""
        reactor.callFromThread(reactor.stop)
        return True

    def on_draw(self):
        """Draw the screen."""
        self.clear()
        self.batch.draw()

class GameProtocol(LineReceiver):
    """Client for Twisted Server."""
    def characters(self):
        """Send this characters data."""
        self.send({
            'function': 'characters',
            'kwargs': {
                'player': self.player,
                'health': self.character.health,
                'image': self.character.image,
                'maxhealth': self.character.maxhealth,
                'name': self.character.name,
                'status': list(self.character.status),
                'type': self.character.type
            }
        })

    def connectionMade(self):
        self.field = []
        self.players = []
        self.window = Window(
            self,
            caption='MMBN Online',
            resizable=True
        )
        self.window.maximize()
        #self.images(self.window.images['characters'])
        @self.window.event
        def on_key_press(symbol, modifiers):
            """Handle key presses for Pyglet."""
            # If the player is prompted to select a chip
            if self.select:
                if symbol == key.RETURN:
                    # Finish the selection.
                    self.select = False
                    # Add the chips to the player.
                    for value in self.selected:
                        self.character.chips.append(
                            self.chips[self.picked[value]]
                        )
                    # Make the first selected the first used.
                    self.character.chips.reverse()
                    # Remove the chips from the library.
                    self.selected.sort()
                    offset = 0
                    for value in self.selected:
                        del self.chips[
                            self.picked[value] - offset
                        ]
                        offset += 1
                if symbol == key.RIGHT:
                    self.cursor(1)
                if symbol == key.LEFT:
                    self.cursor(-1)
                if symbol == key.A and self.equipable(
                    self.selection
                ):
                    # Prepare to add the chip.
                    self.selected.append(self.selection)
                if symbol == key.S and self.selected:
                    # Undo the selection.
                    self.selected.pop()
            else:
                # If the game is not over
                winner = []
                for value in self.players:
                    if value and value['health']:
                        winner.append(value['name'])
                if len(winner) != 1:
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
                        # Start the selection if the custom bar is full.
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

    def cursor(self, cols):
        """Move the cursor for chip selection."""
        newcol = self.selection + cols
        if newcol >= 0 and newcol < len(self.picked):
            self.selection = newcol

    def custom(self):
        """Redefine all the necessary values when prompting the custom bar."""
        self.custombar = 0
        self.character.chips = []
        self.pickchips()
        self.select = True
        self.selection = 0
        self.selected = []

    def draw(self):
        """Draw the screen"""
        # Start by clearing the screen.
        os.system('cls')
        # Graphically display a character or chip's type.
        types = {
            'wind': 'A',
            'none': 'N',
            'plus': 'P'
        }
        # If the player is prompted to select a chip
        if self.select:
            # Display the chip selection.
            menu = 'Custom: '
            for index, chip in enumerate(self.picked):
                menu += '|'
                cursor = '  '
                if index == self.selection:
                    cursor = '+ '
                menu += cursor
                power = ''
                if hasattr(self.chips[chip], 'power'):
                    power = ' %s' % (self.chips[chip].power)
                equipable = self.equipable(index)
                if equipable:
                    equipable = ' '
                else:
                    equipable = 'X'
                if not index in self.selected:
                    menu += '%s%s %s %s %s' % (
                        self.chips[chip].name,
                        power,
                        types[self.chips[chip].type],
                        self.chips[chip].code,
                        equipable
                    )
                else:
                    menu += '%s%s %s %s %s' % (
                        ' ' * len(self.chips[chip].name),
                        ' ' * len(str(power)),
                        ' ' * len(types[self.chips[chip].type]),
                        ' ' * len(self.chips[chip].code),
                        ' ' * len(equipable)
                    )
            if self.picked:
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
        for value in range(0, cols):
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
                if (col > (cols / 2) - 1) ^ panel['stolen']:
                    blue = 'B'
                grid += ' %s%s%s |' % (status[panel['status']], label, blue)
            grid += '\n %s' % (top)
        print grid
        for value in self.players:
            if value:
                print '\n%s' % (value['name'])
                print '-HP: %s' % (value['health'])
                print '-Status: %s' % (', '.join(value['status']))
                print '-Type: %s' % (value['type'])
        chips = []
        # Display the usable chips.
        for value in self.character.chips:
            power = ''
            if hasattr(value, 'power'):
                power = ' %s' % (value.power)
            chips.append('%s%s %s' % (value.name, power, types[value.type]))
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
        winner = []
        for value in self.players:
            if value and value['health']:
                winner.append(value['name'])
        if not self.select and len(winner) == 1:
            print '\n%s wins! Press "r" to restart.' % (winner[0])
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
        xcenter = (self.window.width / 2) - (40 * (cols / 2))
        ycenter = (self.window.height / 2) - (25 * (rows / 2))
        if rows > 1:
            ycenter -= 5
        if self.select:
            if not 'menu' in self.window.sprites:
                self.window.sprites['menu'] = Sprite(
                    self.window.images['battle']['select']['menu'],
                    0,
                    0
                )
            self.window.sprites['menu'].x = xcenter
            self.window.sprites['menu'].y = ycenter
            self.window.sprites['menu'].group = OrderedGroup(rows + 1)
            self.window.sprites['menu'].batch = self.window.batch
            image = self.window.images['battle']['select'][
                self.chips[self.picked[self.selection]].classification
            ]
            if not 'classification' in self.window.sprites:
                self.window.sprites['classification'] = Sprite(
                    image,
                    0,
                    0
                )
            self.window.sprites['classification'].image = image
            self.window.sprites['classification'].x = xcenter
            self.window.sprites['classification'].y = ycenter + 54
            self.window.sprites['classification'].group = OrderedGroup(rows)
            self.window.sprites['classification'].batch = self.window.batch
            image = self.window.images['chips']['big']
            classification = self.window.images['chips'][
                self.chips[self.picked[self.selection]].classification
            ]
            chip = self.chips[self.picked[self.selection]].chip
            if chip in classification:
                image = classification[chip]
            if not 'chip' in self.window.sprites:
                self.window.sprites['chip'] = Sprite(
                    image,
                    0,
                    0
                )
            self.window.sprites['chip'].image = image
            self.window.sprites['chip'].x = xcenter + 15
            self.window.sprites['chip'].y = ycenter + 87
            self.window.sprites['chip'].group = OrderedGroup(rows + 1)
            self.window.sprites['chip'].batch = self.window.batch
            image = self.window.images[
                'battle'
            ]['select']['cursors']['chip']['0']
            if not 'cursor' in self.window.sprites:
                self.window.sprites['cursor'] = Sprite(
                    image,
                    0,
                    0
                )
            self.window.sprites['cursor'].image = image
            self.window.sprites['cursor'].x = xcenter + 4 + (
                16 * self.selection
            )
            self.window.sprites['cursor'].y = ycenter + 39
            self.window.sprites['cursor'].group = OrderedGroup(rows + 1)
            self.window.sprites['cursor'].batch = self.window.batch
            for key, value in enumerate(self.picked):
                if key:
                    break
                image = self.window.images['chips']['icon']
                classification = self.window.images['chips'][
                    self.chips[value].classification
                ]['icons']
                chip = self.chips[value].chip
                if chip in classification:
                    image = classification[chip]
                if len(self.window.sprites['icons']) < key + 1:
                    self.window.sprites['icons'].append(Sprite(
                        image,
                        0,
                        0
                    ))
                self.window.sprites['icons'][key].image = image
                self.window.sprites['icons'][key].x = xcenter + 8
                self.window.sprites['icons'][key].y = ycenter + 39
                self.window.sprites['icons'][key].group = OrderedGroup(
                    rows + 1
                )
                self.window.sprites['icons'][key].batch = self.window.batch
            image = self.window.images['chips']['types'][
                self.chips[self.picked[self.selection]].type
            ]
            if not 'type' in self.window.sprites:
                self.window.sprites['type'] = Sprite(
                    image,
                    0,
                    0
                )
            self.window.sprites['type'].image = image
            self.window.sprites['type'].x = xcenter + 25
            self.window.sprites['type'].y = ycenter + 72
            self.window.sprites['type'].group = OrderedGroup(rows + 1)
            self.window.sprites['type'].batch = self.window.batch
        for row in range(0, rows):
            for col in range(0, cols):
                panel = self.field[row][col]
                x = 40 * col + xcenter
                y = 25 * row + ycenter
                color = 'red'
                if (col > (cols / 2) - 1) ^ panel['stolen']:
                    color = 'blue'
                shading = 'middle'
                if row == rows - 1 and rows > 2:
                    shading = 'top'
                if not row and rows > 1:
                    shading = 'bottom'
                    y -= 5
                image = self.window.images[
                    'panels'
                ][color][panel['status']][shading]
                if not 'sprite' in panel:
                    panel['sprite'] = Sprite(
                        image,
                        0,
                        0,
                        group=OrderedGroup(0)
                    )
                panel['sprite'].image = image
                panel['sprite'].x = x
                panel['sprite'].y = y
                panel['sprite'].batch = self.window.batch
                character = panel['character']
                if character:
                    player = self.players[character - 1]
                    if player and player['health']:
                        image = self.window.images[
                            'characters'
                        ]['mega'][player['image']]['0']
                        xoffset = 24
                        if (col > (cols / 2) - 1) ^ panel['stolen']:
                            image = image.get_transform()
                            image.anchor_x = image.width
                            image = image.get_transform(flip_x=True)
                            xoffset = 36
                        x = x - xoffset
                        y = y - 23
                        if not 'sprite' in player:
                            player['sprite'] = Sprite(image, x, y)
                        player['sprite'].image = image
                        player['sprite'].x = x
                        player['sprite'].y = y
                        player['sprite'].group = OrderedGroup(
                            range(rows - 1, -1, -1)[row] + 1
                        )
                        player['sprite'].batch = self.window.batch

    def equipable(self, chip):
        """Check if a chip can be equipped."""
        # If the chip has already been selected, you have already selected
        # five, or the chip is out of range.
        if (
            chip in self.selected or
            len(self.selected) > 4 or
            chip > len(self.chips) - 1
        ):
            return
        # Add the chip in question to see if the new set fits the conditions.
        self.selected.append(chip)
        chip = self.chips[self.picked[chip]]
        codes = set([])
        names = set([])
        success = True
        for value in self.selected:
            thischip = self.chips[self.picked[value]]
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

    def hit(self, row, col, power, type = 'none', flinch = True):
        """Handle damage."""
        self.send({
            'function': 'hit',
            'kwargs': {
                'row': row,
                'col': col,
                'flip': self.flip,
                'power': power,
                'type': type,
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
        line = json.loads(line)
        callable = self
        if line['object'] == 'character':
            callable = self.character
        for index, value in line['kwargs'].items():
            del line['kwargs'][index]
            line['kwargs'][str(index)] = value
        getattr(callable, line['function'])(**line['kwargs'])
        self.draw()

    def move(self, row, col, rows = 0, cols = 0, force = False):
        """Move the player if possible."""
        self.send({
            'function': 'move',
            'kwargs': {
                'row': row,
                'col': col,
                'flip': self.flip,
                'info': {
                    'status': list(self.character.status),
                    'type': self.character.type
                },
                'rows': rows,
                'cols': cols,
                'force': force
            }
        })

    def panel(self, row, col, status = None, stolen = None):
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

    def pickchips(self):
        """Pick a certain amount of random chips for selection."""
        picked = set([])
        # While there are chips to pick and the list is under 8, pick.
        while len(self.chips) != len(picked) and len(picked) < 8:
            picked.add(randint(0, len(self.chips) - 1))
        self.picked = list(picked)
        shuffle(self.picked)

    def send(self, line, **kwargs):
        """Messages are always to be sent as a JSON string."""
        self.sendLine(json.dumps(line, **kwargs))

    def start(self, field, row, col, flip, player):
        """Set up the data for the beginning of the game."""
        self.flip = flip
        self.player = player
        players = []
        for value in range(0, player):
            players.append({})
        self.update(field, players)
        self.chips = json.loads(
            open(
                os.path.join(
                    'chips',
                    'folders',
                    '%s.json' % (config['chipfolder'])
                )
            ).read()
        )
        if len(self.chips) > 30:
            raise Exception('Your folder cannot have more than 30 chips.')
        if len(self.chips) < 30:
            raise Exception('Your folder must have 30 chips.')
        module = __import__(
            'characters.%s' % (config['character']),
            globals(),
            locals(),
            ('Character',),
            -1
        )
        self.character = module.Character(self)
        # Convert the list of chip names and codes to a list of chip instances.
        for index, chip in enumerate(self.chips):
            module = __import__(
                'chips.%s' % (chip['chip']),
                globals(),
                locals(),
                ('Chip',),
                -1
            )
            self.chips[index] = module.Chip(self.character)
            if not chip['code'] in self.chips[index].codes:
                raise Exception('Improper chip code')
            self.chips[index].chip = chip['chip']
            self.chips[index].code = chip['code']
        self.character.row = row
        self.character.col = col
        if self.flip:
            self.character.col = range(len(self.field[0]) - 1, -1, -1)[col]
        self.custom()
        self.characters()
        length = len(self.field)
        height = length * 25
        if length > 1:
            height += 5

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
        if self.flip:
            for value in field:
                value.reverse()
        if self.field:
            for row in range(0, len(field)):
                for col in range(0, len(field[0])):
                    for index, value in field[row][col].items():
                        self.field[row][col][index] = value
        else:
            self.field = field
        for player in range(0, len(players)):
            if len(self.players) > player:
                for index, value in players[player].items():
                    self.players[player][index] = value
            else:
                self.players.append(players[player])
        while len(self.players) > len(players):
            self.players.pop()
            if len(self.players) < self.player:
                self.player -= 1

def loader(path):
    images = {}
    for panel in os.listdir(path):
        panel = panel.split('.')
        name = panel[0]
        if name:
            if len(panel) > 1:
                images[name] = resource.image(
                    os.path.join(
                        path,
                        '%s.%s' % (name, panel[1])
                    ).replace('\\', '/')
                )
            else:
                images[name] = loader(
                    os.path.join(
                        path,
                        '%s' % (name)
                    )
                )
    return images

factory = protocol.ClientFactory()
factory.protocol = GameProtocol
reactor.connectTCP(config['ip'], config['port'], factory)
reactor.run()