var Character = require(__dirname + '/character'),
    EOL = require('os').EOL;

module.exports = function(config) {
    var IO = null,
        field,
        players = [null, null];

    function connect(socket) {
        var player,
            playerNum = -1;

        if (!players[0]) {
            playerNum = 1;
        } else if (!players[1]) {
            playerNum = 2;
        }

        if (playerNum !== -1) {
            player = new Character(socket.id, playerNum);
            players[playerNum - 1] = player;

            if (playerNum === 1) {
                placeCharacter(player, 1, 1);
            } else if (playerNum === 2) {
                placeCharacter(player, 1, 4);
            }

            IO.emit('user connected', playerNum);

            drawField();
            console.log('user `' + socket.id + '` connected');
        }
    }

    function disconnect(id) {
        var player = getPlayerById(id),
            playerNum;

        if (player) {
            playerNum = player.getPlayerNum();

            IO.emit('user disconnected', playerNum);

            field[player.getRow()][player.getCol()].character = null;
            delete players[playerNum - 1];

            drawField();
            console.log('user `' + id + '` disconnected');
        }
    }

    function move(playerId, direction, rows, cols) {
        var player = getPlayerById(playerId),
            playerNum = player.getPlayerNum(),
            currentRow,
            currentCol,
            currentPanel,
            newRow,
            newCol,
            newPanel;

        if (rows === undefined) {
            rows = 1;
        }

        if (cols === undefined) {
            cols = 1;
        }

        if (playerNum === 2) {
            cols = -cols;
        }

        if (player) {
            currentRow = player.getRow();
            currentCol = player.getCol();
            currentPanel = field[currentRow][currentCol];
            newRow = currentRow;
            newCol = currentCol;

            // If the panel doesn't contain the character, something went horribly wrong.
            if (currentPanel.character != player) {
                throw new Error('Field desync.');
            }

            switch (direction) {
                case 'up':
                    newRow -= rows;
                    break;

                case 'down':
                    newRow += rows;
                    break;

                case 'left':
                    newCol -= cols;
                    break;

                case 'right':
                    newCol += cols;
                    break;
            }

            // Destination must be a real panel.
            if (
                newRow >= 0 && newRow < config.rows &&
                   newCol >= 0 && newCol < config.cols
            ) {
                newPanel = field[newRow][newCol];

                if (
                    checkPanelInBounds(playerNum, newRow, newCol) &&
                        !newPanel.character
                ) {
                    currentPanel.character = null;
                    newPanel.character = player;
                    player.setRow(newRow);
                    player.setCol(newCol);
                    drawField();
                }
            }
        }
    }

    function attach(io) {
        IO = io;

        io.on('connection', function (socket) {
            if (!field) {
                createField();
            }

            connect(socket);

            socket.on('disconnect', function() {
                disconnect(socket.id);
            });

            socket.on('move', function(direction) {
                move(socket.id, direction);
            });
        });
    };

    return {
        attach : attach
    };

    function checkPanelInBounds(playerNum, newRow, newCol) {
        var newPanel = field[newRow][newCol],
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
    }

    function createField() {
        var row,
            col,
            cols,
            panel;

        if (config.rows < 1 || config.cols < 1 || config.cols % 2) {
            throw new Error('Field dimensions invalid.');
        }

        field = [];

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

            field.push(cols);
        }
    }

    function drawField() {
        var grid = EOL,
            panelStatus = {
                broken: 'B',
                cracked: 'C',
                grass: 'G',
                holy: 'H',
                ice: 'I',
                lava: 'L',
                normal: ' ',
                metal: 'M',
                poison: 'P',
                sand: 'S',
                water: 'W'
            },
            playerNum,
            row,
            col,
            r,
            c;

        for (r in field) {
            row = field[r];

            grid += ' ----- ----- ----- ----- ----- -----' + EOL +
                '|';

            for (c in row) {
                col = row[c];

                grid += ' ' + panelStatus[col.status];

                if (col.character && col.character.getHealth()) {
                    playerNum = col.character.getPlayerNum();

                    if (playerNum === 1) {
                        grid += 'x';
                    } else if (playerNum === 2) {
                        grid += 'o';
                    } else {
                        grid += '?';
                    }
                } else {
                    grid += ' ';
                }

                // Label the red-side of the field from Player 1's perspective.
                if (checkPanelInBounds(1, r, c)) {
                    grid += ' ';
                } else {
                    grid += 'R';
                }

                grid += ' |';
            }

            grid += EOL +
                ' ----- ----- ----- ----- ----- -----' + EOL
        }

        console.log('\033[2J');
        console.log(grid);
    }

    function getPlayerById(id) {
        var player,
            p;

        for (p in players) {
            player = players[p];

            if (player.getId() === id) {
                return player;
            }
        }

        return null;
    }

    function placeCharacter(character, row, col) {
        character.setRow(row);
        character.setCol(col);

        field[row][col].character = character;
    }
};
