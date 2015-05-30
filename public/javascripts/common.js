'use strict';

var exports = (typeof module !== 'undefined' && typeof module.exports !== 'undefined') ? module.exports : window,
    panelStatus = {
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

function gridToString(config, grid, players, playerNumPerspective) {
    var response = EOL,
        row,
        col,
        player,
        r,
        c,
        p;

    for (r in grid) {
        row = grid[r];

        response += ' ----- ----- ----- ----- ----- -----' + EOL +
            '|';

        for (c in row) {
            if (playerNumPerspective === 2) {
                c = config.cols - c - 1;
            }

            col = row[c];

            response += ' ' + panelStatus[col.status];

            if (col.character && col.character.health) {
                if (playerNumPerspective === col.character.playerNum) {
                    response += 'x';
                } else {
                    response += 'o';
                }
            } else {
                response += ' ';
            }

            if (checkPanelInBounds(config, grid, playerNumPerspective, r, c)) {
                response += ' ';
            } else {
                response += 'R';
            }

            response += ' |';
        }

        response += EOL +
            ' ----- ----- ----- ----- ----- -----' + EOL;
    }

    for (p in players) {
        player = players[p];

        if (player) {
            response += 'Player ' + player.playerNum + ': ' + player.health + 'HP' + EOL;
        }
    }

    return response;
};

exports.checkPanelInBounds = checkPanelInBounds;
exports.gridToString = gridToString;
