'use strict';

var exports = (typeof module !== 'undefined' && typeof module.exports !== 'undefined') ? module.exports : window,
    panelStatusLabels = {
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
        water   : 'W',
        up      : '^',
        down    : 'V',
        left    : '<',
        right   : '>'
    },
    EOL = '\n';

function checkPanelInBounds(config, grid, playerNum, newRow, newCol) {
    var newPanel = grid[newRow][newCol],
        isInBounds,
    // Check if the player is on the left side of the field.
        isNormalSide = (newCol < (config.cols / 2));

    // Player 2 should be on the right side.
    if (playerNum === 2) {
        isNormalSide = !isNormalSide;
    }

    isInBounds = isNormalSide;

    // Flip the result if this panel is stolen.
    if (newPanel.stolen) {
        isInBounds = !isInBounds;
    }

    return isInBounds;
};

function gameToString(config, game, playerNumPerspective) {
    var response = EOL,
        row,
        panel,
        panelStatus,
        player,
        r,
        c,
        p;

    for (r in game.field) {
        row = game.field[r];

        response += ' ----- ----- ----- ----- ----- -----' + EOL +
            '|';

        for (c in row) {
            if (playerNumPerspective === 2) {
                c = config.cols - c - 1;
            }

            panel = row[c];
            panelStatus = panel.status;

            if (playerNumPerspective === 2) {
                if (panelStatus === 'left') {
                    panelStatus = 'right';
                } else if (panelStatus === 'right') {
                    panelStatus = 'left';
                }
            }

            response += ' ' + panelStatusLabels[panelStatus];

            if (panel.character && panel.character.health) {
                if (playerNumPerspective === panel.character.playerNum) {
                    response += 'x';
                } else {
                    response += 'o';
                }
            } else {
                response += ' ';
            }

            if (checkPanelInBounds(config, game.field, playerNumPerspective, r, c)) {
                response += ' ';
            } else {
                response += 'R';
            }

            response += ' |';
        }

        response += EOL +
            ' ----- ----- ----- ----- ----- -----' + EOL;
    }

    for (p in game.players) {
        player = game.players[p];

        if (player && player.health) {
            response += 'Player ' + player.playerNum + ': ' + player.health + 'HP' + EOL;
        }
    }

    response += 'Observers: ' + game.observers;

    return response;
};

exports.checkPanelInBounds = checkPanelInBounds;
exports.gameToString = gameToString;
