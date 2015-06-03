var common = require(__dirname + '/common'),
    Panel = require(__dirname + '/panel');

module.exports = function Field(io, config, game) {
    var self = this;

    this.grid = [];

    this.getGrid = function getGrid() {
        return self.grid;
    };

    this.draw = function draw() {
        if (game.num === 1) {
            // Clear the console.
            console.log('\033[2J');

            // Draw the game from Player 1's perspective.
            console.log(common.gameToString(config, game.toSendable(), 1));
        }
    };

    this.initialize = function initialize() {
        var cols,
            row,
            col;

        if (config.rows < 1 || config.cols < 1 || config.cols % 2) {
            throw new Error('Field dimensions invalid.');
        }

        for (row = 0; row < config.rows; row++) {
            cols = [];

            for (col = 0; col < config.cols; col++) {
                cols.push(new Panel(io, config, game, self, row, col));
            }

            self.grid.push(cols);
        }

    }

    this.placeCharacter = function place(character, row, col) {
        self.grid[row][col].character = character;
    };

    this.toSendable = function toSendable() {
        var sendable = [],
            cols,
            row,
            col;

        for (row = 0; row < config.rows; row++) {
            cols = [];

            for (col = 0; col < config.cols; col++) {
                cols.push(self.grid[row][col].toSendable());
            }

            sendable.push(cols);
        }

        return sendable;
    }

    this.initialize();
};
