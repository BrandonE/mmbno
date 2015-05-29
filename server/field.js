var EOL = require('os').EOL;

module.exports = function Field(config, players) {
    var self = this,
        row,
        col,
        cols,
        panel;

    this.config = config;
    this.grid = [];
    this.players = players;

    this.getGrid = function getGrid() {
        return self.grid;
    };

    this.checkCanStand = function checkCanStand(player, newPanel) {
        return (
            ['blank', 'broken'].indexOf(newPanel.status) === -1 ||
                player.status.indexOf('airshoes') > -1
        );
    };

    this.checkPanelInBounds = function checkPanelInBounds(player, newRow, newCol) {
        var newPanel = self.grid[newRow][newCol],
            isInBounds,
            // Check if the player is on the left side of the field.
            isNormalSide = (newCol < (config.cols / 2));

        // Player 2 should be on the right side.
        if (player.getPlayerNum() === 2) {
            isNormalSide = !isNormalSide;
        }

        isInBounds = isNormalSide;

        // Flip the result if this panel is stolen.
        if (newPanel.stolen) {
            isInBounds = !isInBounds;
        }

        return isInBounds;
    };

    this.draw = function draw() {
        var response = EOL,
            grid = self.getGrid(),
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
            playerNum,
            row,
            col,
            r,
            c;

        for (r in grid) {
            row = grid[r];

            response += ' ----- ----- ----- ----- ----- -----' + EOL +
                '|';

            for (c in row) {
                col = row[c];

                response += ' ' + panelStatus[col.status];

                if (col.character && col.character.getHealth()) {
                    playerNum = col.character.getPlayerNum();

                    if (playerNum === 1) {
                        response += 'x';
                    } else if (playerNum === 2) {
                        response += 'o';
                    } else {
                        response += '?';
                    }
                } else {
                    response += ' ';
                }

                // Label the red-side of the field from Player 1's perspective.
                if (self.checkPanelInBounds(self.players[0], r, c)) {
                    response += ' ';
                } else {
                    response += 'R';
                }

                response += ' |';
            }

            response += EOL +
                ' ----- ----- ----- ----- ----- -----' + EOL;
        }

        console.log('\033[2J');
        console.log(response);
    };

    this.placeCharacter = function place(character, row, col) {
        self.grid[row][col].character = character;
    };

    if (config.rows < 1 || config.cols < 1 || config.cols % 2) {
        throw new Error('Field dimensions invalid.');
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

        this.grid.push(cols);
    }
};
