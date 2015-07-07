'use strict';

var exports = (typeof module !== 'undefined' && typeof module.exports !== 'undefined') ? module.exports : window,
    panelTypeLabels = {
        blank   : '_',
        broken  : 'B',
        cracked : 'C',
        frozen  : 'F',
        grass   : 'G',
        holy    : 'H',
        lava    : 'L',
        normal  : ' ',
        metal   : 'M',
        poison  : 'P',
        sand    : 'S',
        volcano : 'V',
        water   : 'W',
        up      : '^',
        down    : 'v',
        left    : '<',
        right   : '>'
    },
    EOL = '\n';

function isPanelInBounds(config, grid, playerNum, row, col) {
    var panel = grid[row][col],
        isInBounds,
        // Check if the player is on the left side of the field.
        isNormalSide = (col < (config.cols / 2));

    // Player 2 should be on the right side.
    if (playerNum === 2) {
        isNormalSide = !isNormalSide;
    }

    isInBounds = isNormalSide;

    // Flip the result if this panel is stolen.
    if (panel.stolen) {
        isInBounds = !isInBounds;
    }

    return isInBounds;
}

function gameToString(config, game, playerNumPerspective) {
    var response = EOL,
        row,
        panel,
        panelType,
        player,
        damageHandler,
        r,
        c,
        p,
        d;

    for (r in game.field) {
        if (game.field.hasOwnProperty(r)) {
            row = game.field[r];

            response += ' ----- ----- ----- ----- ----- -----' + EOL +
                '|';

            for (c in row) {
                if (row.hasOwnProperty(c)) {
                    if (playerNumPerspective === 2) {
                        c = config.cols - c - 1;
                    }

                    panel = row[c];
                    panelType = panel.type;

                    if (playerNumPerspective === 2) {
                        if (panelType === 'left') {
                            panelType = 'right';
                        } else if (panelType === 'right') {
                            panelType = 'left';
                        }
                    }

                    response += ' ' + panelTypeLabels[panelType];

                    if (panel.character && panel.character.health) {
                        if (playerNumPerspective === panel.character.playerNum) {
                            response += 'x';
                        } else {
                            response += 'o';
                        }
                    } else {
                        response += ' ';
                    }

                    if (isPanelInBounds(config, game.field, playerNumPerspective, r, c)) {
                        response += ' ';
                    } else {
                        response += 'R';
                    }

                    response += ' |';
                }
            }

            response += EOL +
                ' ----- ----- ----- ----- ----- -----' + EOL;
        }
    }

    for (p in game.players) {
        if (game.players.hasOwnProperty(p)) {
            player = game.players[p];

            if (player && player.health) {
                response += 'Player ' + player.playerNum + ': ' + player.health + 'HP';

                if (player.statuses.length) {
                    response += ', ' + player.statuses.join(', ');
                }

                for (d in player.damageHandlers) {
                    damageHandler = player.damageHandlers[d];

                    if (damageHandler) {
                        response += ', ' + damageHandler;
                    }
                }

                response += EOL;
            }
        }
    }

    response += 'Observers: ' + game.observers;

    return response;
}

exports.isPanelInBounds = isPanelInBounds;
exports.gameToString = gameToString;
