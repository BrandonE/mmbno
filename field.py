def makefield():
    field = []
    for row in range(0, 3):
        cols = []
        for col in range(0, 6):
            box = {
                'character': None,
                'inverted': False,
                'status': 'normal',
                'col': col
            }
            cols.append(box)
        field.append(cols)
    return field

def flipfield(field):
    field = field[:]
    for key in enumerate(field):
        field[key[0]] = field[key[0]][:]
        field[key[0]].reverse()
    return field