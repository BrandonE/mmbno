from game import game

def handle(key):
    if key == 'Escape':
        root.destroy()
    if game.player.health and game.opponent.health:
        if game.select:
            if key == 'Return':
                game.select = False
                for value in game.selected:
                    game.player.chips.append(game.chips[game.picked[value]])
                game.player.chips.reverse()
                game.selected.sort()
                offset = 0
                for value in game.selected:
                    del game.chips[game.picked[value] - offset]
                    offset += 1
            if key == 'Right':
                game.cursor(1)
            if key == 'Left':
                game.cursor(-1)
            if (
                key == 'a' and
                not game.selection in game.selected and
                len(game.selected) < 5 and
                game.selection < len(game.chips)
            ):
                chip = game.chips[game.picked[game.selection]]
                success = True
                for value in game.selected:
                    if (
                        game.chips[value].code != '*' and
                        chip.code != '*' and
                        game.chips[value].code != chip.code and
                        game.chips[value].name != chip.name
                    ):
                        success = False
                        break
                if success:
                    game.selected.append(game.selection)
            if key == 's' and game.selected:
                game.selected.pop()
        else:
            if key == 'Up':
                game.player.move(rows=1)
                game.player.time()
                if game.time < 10:
                    game.time += 1
            if key == 'Down':
                game.player.move(rows=-1)
                game.player.time()
                if game.time < 10:
                    game.time += 1
            if key == 'Right':
                game.player.move(cols=1)
                game.player.time()
                if game.time < 10:
                    game.time += 1
            if key == 'Left':
                game.player.move(cols=-1)
                game.player.time()
                if game.time < 10:
                    game.time += 1
            if key == 'a' and game.player.chips:
                game.player.usechip()
            if key == 's':
                game.player.buster()
            if key == 'd':
                if game.time >= 10:
                    game.custom()
            if key == 'c':
                game.player.charge()
            if key == 'f':
                game.player.hit(25)
            if key == 'g':
                game.player.hit(100)
    elif key == 'r':
        game.__init__()