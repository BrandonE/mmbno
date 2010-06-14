import os
import Tkinter as tk
from game import game
from controls import handle

status = {
    'normal': 'N',
    'number': '/'
}

def chardraw(character):
    print '\n%s' % (character.name)
    print '-HP: %s' % (str(character.health))
    print '-Status: %s' % (', '.join(character.status))
    print '-Type %s' % (character.type)
    chips = []
    for value in character.chips:
        power = ' '
        if hasattr(value, 'power'):
            power = value.power
        chips.append('%s %s %s' % (value.name, power, status[value.type]))
    print '-Chips: %s' % (', '.join(chips))
    print '-Active Chip:'
    for key, value in character.activechips.items():
        if value:
            print '--%s: %s' % (key, character.getactivechip(key).name)

def draw():
    os.system('cls')
    if game.select:
        menu = ''
        for key, chip in enumerate(game.picked):
            menu += '|'
            cursor = '  '
            if key == game.selection:
                cursor = '+ '
            menu += cursor
            power = ' '
            if hasattr(game.chips[chip], 'power'):
                power = game.chips[chip].power
            if not key in game.selected:
                menu += '%s %s %s %s' % (
                    game.chips[chip].name,
                    power,
                    status[game.chips[chip].type],
                    game.chips[chip].code
                )
            else:
                menu += '%s %s %s %s' % (
                    ' ' * len(game.chips[chip].name),
                    ' ' * len(str(power)),
                    ' ' * len(status[game.chips[chip].type]),
                    ' ' * len(game.chips[chip].code)
                )
        print '%s|' % (menu)
    custom = ''
    if game.time >= 10:
        custom = ' Custom'
    print '%s%s' % (('*' * game.time), custom)
    fielddraw(game.player)
    fielddraw(game.opponent)
    chardraw(game.player)
    chardraw(game.opponent)
    if not game.player.health or not game.opponent.health:
        winner = game.player
        loser = game.opponent
        if not game.player.health:
            winner = game.opponent
            loser = game.player
        print '\n%s defeated! %s wins! Press "r" to restart.' % (
            loser.name,
            winner.name
        )
    print '\nControls:'
    print 'Directional Keys - Move Player / Chip Selection'
    print 'A: Use / Select Chip'
    print 'S: Use Buster / Remove Chip'
    print 'D: Prompt Chip Selection'
    print 'C: Charge Shot'
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
            if col['character'] and col['character'].health:
                label = 'x'
                if character == col['character']:
                    label = 'o'
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
    handle(key)
    draw()

draw()
root = tk.Tk()
root.bind_all('<Key>', keypress)
root.withdraw()
root.mainloop()