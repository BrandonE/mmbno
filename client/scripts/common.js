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

function isPanelInBounds(config, col, stolen, playerNum) {
    var isInBounds,
        // Check if the player is on the left side of the field.
        isNormalSide = (col < (config.cols / 2));

    // Player 2 should be on the right side.
    if (playerNum === 2) {
        isNormalSide = !isNormalSide;
    }

    isInBounds = isNormalSide;

    // Flip the result if this panel is stolen.
    if (stolen) {
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
        activeDamageHandlers,
        damageHandler,
        r,
        c,
        p,
        d;

    for (r = 0; r < game.field.length; r++) {
        row = game.field[r];

        response += ' ----- ----- ----- ----- ----- -----' + EOL +
            '|';

        for (c = 0; c < row.length; c++) {
            if (playerNumPerspective === 1) {
                panel = row[c];
            } else {
                panel = row[config.cols - c - 1];
            }

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

            if (isPanelInBounds(config, c, game.field[r][c].stolen, playerNumPerspective)) {
                response += ' ';
            } else {
                response += 'B';
            }

            response += ' |';
        }

        response += EOL +
            ' ----- ----- ----- ----- ----- -----' + EOL;
    }

    for (p = 0; p < game.players.length; p++) {
        activeDamageHandlers = [];

        player = game.players[p];

        if (player && player.health) {
            for (d = 0; d < player.damageHandlers.length; d++) {
                damageHandler = player.damageHandlers[d];

                if (damageHandler) {
                    activeDamageHandlers.push(damageHandler);
                }
            }

            response += 'Player ' + player.playerNum + ':' + EOL +
                '    ' + player.health + 'HP' + EOL +
                '    Statuses: ' + player.statuses.join(', ') + EOL +
                '    Damage Handlers: ' + activeDamageHandlers.join(', ') + EOL;
        }
    }

    response += 'Observers: ' + game.observers;

    return response;
}

exports.isPanelInBounds = isPanelInBounds;
exports.gameToString = gameToString;
