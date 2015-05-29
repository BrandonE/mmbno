var socket = io(),
    clientPlayerNum = -1,
    grid = [],
    players = [null, null],
    config = {
        rows : 3,
        cols : 6
    },
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
    EOL = '\n',
    row,
    col,
    cols,
    panel;

function checkPanelInBounds(playerNum, newRow, newCol) {
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

function draw() {
    var response = EOL,
        playerNum,
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
            col = row[c];

            response += '  '/* + panelStatus[col.status]*/;

            if (col.character/* && col.character.getHealth()*/) {
                /*
                playerNum = col.character.getPlayerNum();

                if (playerNum === 1) {
                    response += 'x';
                } else if (playerNum === 2) {
                    response += 'o';
                } else {
                    response += '?';
                }
                */
                response += 'x';
            } else {
                response += ' ';
            }

            // Label the red-side of the field from Player 1's perspective.
            if (checkPanelInBounds(clientPlayerNum, r, c)) {
                response += ' ';
            } else {
                response += 'R';
            }

            response += ' |';
        }

        response += EOL +
            ' ----- ----- ----- ----- ----- -----' + EOL;
    }

    /*
    for (p in players) {
        player = players[p];

        if (player) {
            response += 'Player ' + player.getPlayerNum() + ': ' + player.getHealth() + 'HP' + EOL;
        }
    }
    */

    $('#grid').text(response);
}

for (row = 0; row < config.rows; row++) {
    cols = [];

    for (col = 0; col < config.cols; col++) {
        panel = {
            character : null,
            stolen    : false,
            status    : 'normal',
            time      : 0
        };

        cols.push(panel);
    }

    grid.push(cols);
}

$(document).ready
(
    function ()
    {
        socket.on('user connected', function(playerNum, playersToSend) {
            var player,
                p;

            if (clientPlayerNum === -1) {
                clientPlayerNum = playerNum;
                $('#playerNum').text(clientPlayerNum);
            }

            for (p in playersToSend) {
                player = playersToSend[p];

                if (player) {
                    players[p] = player;
                    grid[player.row][player.col].character = player;
                }
            }

            draw();
        });

        socket.on('user disconnected', function(playerNum) {
            draw();
        });

        socket.on('moved', function(playerNum, row, col) {
            var player = players[playerNum - 1];
            grid[player.row][player.col].character = null;
            player.row = row;
            player.col = col;
            grid[row][col].character = player;
            draw();
        });

        $(document).keydown(function(e) {
            switch(e.which) {
                case 37:
                    socket.emit('move', 'left');
                    break;

                case 38:
                    socket.emit('move', 'up');
                    break;

                case 39:
                    socket.emit('move', 'right');
                    break;

                case 40:
                    socket.emit('move', 'down');
                    break;

                case 65:
                    socket.emit('buster');
                    break;

                default:
                    return;
            }

            e.preventDefault();
        });
    }
);
