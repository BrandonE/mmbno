var EOL = require('os').EOL;

module.exports = function(config) {
    var IO = null,
        field;

    function connect(socket) {
        IO.emit('user connected');
        drawField();
        console.log('user connected');
    }

    function disconnect() {
        IO.emit('user disconnected');
        drawField();
        console.log('user disconnected');
    }

    function attach(io) {
        IO = io;

        io.on('connection', function (socket) {
            if (!field) {
                createField();
            }

            connect(socket);
            socket.on('disconnect', disconnect);
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

                if (col.character && col.character.health) {
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
};
