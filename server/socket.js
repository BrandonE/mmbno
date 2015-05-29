var Character = require(__dirname + '/character'),
    EOL = require('os').EOL;

module.exports = function(config) {
    var IO = null,
        field,
        players = [];

    function connect(socket) {
        var player = new Character(socket.id),
            playerNum;

        players.push(player);
        playerNum = players.length;

        IO.emit('user connected', playerNum);

        if (playerNum === 1) {
            placeCharacter(player, 1, 1);
        } else if (playerNum === 2) {
            placeCharacter(player, 1, 4);
        }

        drawField();
        console.log('user `' + socket.id + '` connected');
    }

    function disconnect() {
        IO.emit('user disconnected');
        // TODO: Remove player.
        drawField();
        console.log('user disconnected');
    }

    function move(playerId, direction) {
        var player = getPlayerById(playerId),
            currentRow,
            currentCol,
            newRow,
            newCol;

        if (player) {
            currentRow = player.getRow();
            currentCol = player.getCol();
            newRow = currentRow;
            newCol = currentCol;

            switch (direction) {
                case 'up':
                    newRow--;
                    break;

                case 'down':
                    newRow++;
                    break;

                case 'left':
                    newCol--;
                    break;

                case 'right':
                    newCol++;
                    break;
            }

            field[currentRow][currentCol].character = null;
            field[newRow][newCol].character = player;
            player.setRow(newRow);
            player.setCol(newCol);
            drawField();
        }
    }

    function attach(io) {
        IO = io;

        io.on('connection', function (socket) {
            if (!field) {
                createField();
            }

            connect(socket);
            socket.on('disconnect', disconnect);

            socket.on('move', function(direction) {
                move(socket.id, direction);
            });
        });
    };

    return {
        attach : attach
    };

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
                    grid += 'x';
                } else {
                    grid += ' ';
                }

                grid += '  |';
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
