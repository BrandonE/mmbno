import os
try:
    import simplejson as json
except ImportError:
    import json
import Tkinter as tk
from random import randint
from field import flipfield, makefield

def chardraw(character):
    print '\n:%s' % (character.name)
    print '-HP: %s' % (str(character.health))
    print '-Status: %s' % (', '.join(character.status))
    chips = []
    for value in character.chips:
        chips.append(value.name)
    print '-Chips: %s' % (', '.join(chips))
    print '-Active Chip:'
    for key, value in character.activechips.items():
        if value:
            print '--%s: %s' % (key, character.getactivechip(key).name)

def draw():
    os.system('cls')
    if select:
        menu = ''
        for key, chip in enumerate(picked):
            menu += '|'
            cursor = '  '
            if key == selection:
                cursor = '+ '
            menu += cursor
            power = ' '
            if hasattr(chips[chip], 'power'):
                power = chips[chip].power
            if not key in selected:
                menu += '%s %s %s' % (chips[chip].name, power, chips[chip].code)
            else:
                menu += '%s %s %s' % (
                    ' ' * len(chips[chip].name),
                    ' ' * len(str(power)),
                    ' ' * len(chips[chip].code)
                )
        print menu + '|'
    fielddraw(player)
    fielddraw(opponent)
    chardraw(player)
    chardraw(opponent)
    if not player.health or not opponent.health:
        winner = player
        loser = opponent
        if not player.health:
            winner = opponent
            loser = player
        print '\n%s defeated! %s wins! Press "r" to restart.' % (loser.name, winner.name)
    print '\nControls:'
    print 'Directional Keys - Move Player / Chip Selection'
    print 'A: Use / Select Chip'
    print 'S: Use Buster / Remove Chip'
    print 'D: Prompt Chip Selection'
    print 'F: Deal 25 damage to player (Test)'
    print 'G: Deal 100 damage to player (Test)'
    print 'Enter: End Chip Selection'
    print 'Escape - End Game'

def fielddraw(character):
    grid = ''
    for row in character.field:
        grid += '\n ----- ----- ----- ----- ----- -----'
        grid += '\n|'
        for key, col in enumerate(row):
            label = ' '
            red = ' '
            status = {
                'broken': 'B',
                'cracked': 'C',
                'normal': ' '
            }
            if col['character']:
                label = 'x'
            if (
                (
                    (key < 0 or key > 2) and
                    col['inverted'] == False
                ) or
                (
                    (key >= 0 or key <= 2) and
                    col['inverted'] == True
                )
            ):
                red = 'R'
            grid += ' %s%s%s |' % (status[col['status']], label, red)
        grid += '\n ----- ----- ----- ----- ----- -----'
    print grid

def keypress(event):
    key = event.keysym
    global chips
    global picked
    global select
    global selected
    global selection
    if key == 'Escape':
        root.destroy()
    if player.health and opponent.health:
        if select:
            if key == 'Return':
                select = False
                for value in selected:
                    player.chips.append(chips[picked[value]])
                player.chips.reverse()
                selected.sort()
                offset = 0
                for value in selected:
                    del chips[picked[value] - offset]
                    offset += 1
            if key == 'Right':
                movecursor(1)
            if key == 'Left':
                movecursor(-1)
            if key == 'a' and not selection in selected and len(selected) < 5:
                if selection < len(chips):
                    selected.append(selection)
            if key == 's' and selected:
                selected.pop()
        else:
            if key == 'Up':
                player.move(rows=1)
            if key == 'Down':
                player.move(rows=-1)
            if key == 'Right':
                player.move(cols=1)
            if key == 'Left':
                player.move(cols=-1)
            if key == 'a' and player.chips:
                player.usechip()
            if key == 's':
                player.buster()
            if key == 'd':
                select = True
                picked = pickchips()
                selection = 0
                selected = []
                player.chips = []
            if key == 'c':
                player.charge()
            if key == 'f':
                player.hit(25)
            if key == 'g':
                player.hit(100)
    elif key == 'r':
        field = makefield()
        player.__init__(field, 1, 1)
        opponentfield = flipfield(field)
        player.move(0, 0, True)
        opponent.__init__(opponentfield, 1, 1)
        opponent.move(0, 0, True)
        chips = json.loads(
            open(
                os.path.join('chips', 'folders', config['chipfolder'])
            ).read()
        )
        chips = chips[0:30]
        for key, value in enumerate(chips):
            module = __import__(
                'chips.%s' % (value['chip']),
                globals(),
                locals(),
                ('Chip',),
                -1
            )
            chips[key] = module.Chip(player, value)
            chips[key].code = value['code']
        select = True
        picked = pickchips()
        selection = 0
        selected = []
    draw()

def movecursor(cols):
    global selection
    newcol = selection + cols
    if newcol >= 0 and newcol < len(picked):
        selection = newcol

def pickchips():
    picked = set([])
    while len(chips) != len(picked) and len(picked) < 10:
        picked.add(randint(0, len(chips) - 1))
    return list(picked)

config = json.loads(open('config.json').read())
field = makefield()
opponentfield = flipfield(field)
from characters.mega import Character
player = Character(field)
player.move(0, 0, True)
from characters.bass import Character
opponent = Character(opponentfield)
opponent.move(0, 0, True)
field[0][0]['status'] = 'broken'
field[2][0]['status'] = 'cracked'
field[0][5]['status'] = 'broken'
chips = json.loads(
    open(
        os.path.join('chips', 'folders', config['chipfolder'])
    ).read()
)
chips = chips[0:30]
for key, value in enumerate(chips):
    module = __import__(
        'chips.%s' % (value['chip']),
        globals(),
        locals(),
        ('Chip',),
        -1
    )
    chips[key] = module.Chip(player, value)
    chips[key].code = value['code']
select = True
picked = pickchips()
selection = 0
selected = []
draw()
root = tk.Tk()
root.bind_all('<Key>', keypress)
root.withdraw()
root.mainloop()