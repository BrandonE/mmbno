var common = require(__dirname + '/common'),
    Panel = require(__dirname + '/panel');

module.exports = function Field(io, config, game) {
    var self = this;

    this.grid = [];
    this.shouldReturnStolenPanels = false;

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

    this.handleAdjacentRoadPanels = function handleAdjacentRoadPanels(row, col) {
        var adjacentRow,
            adjacentCol;

        // Check the panel above this one.
        adjacentRow = row - 1;

        if (adjacentRow > 0) {
            self.grid[adjacentRow][col].handleRoad();
        }

        // Check the panel below this one.
        adjacentRow = row + 1;

        if (adjacentRow < config.rows) {
            self.grid[adjacentRow][col].handleRoad();
        }

        // Check the panel to the left of this one.
        adjacentCol = col - 1;

        if (adjacentCol > 0) {
            self.grid[row][adjacentCol].handleRoad();
        }

        // Check the panel to the right of this one.
        adjacentCol = col + 1;

        if (adjacentCol < config.cols) {
            self.grid[row][adjacentCol].handleRoad();
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

    this.returnCol = function returnCol(col) {
        var panelsStolen = false,
            panelsReturned = false,
            canReturnCol = true,
            row,
            panel;

        for (row = 0; row < config.rows; row++) {
            panel = self.grid[row][col];

            if (panel.isStolen()) {
                panelsStolen = true;

                // A column should not returned if any of its panels cannot be returned due to a present character.
                if (panel.getCharacter()) {
                    canReturnCol = false;
                    break;
                }
            }
        }

        if (panelsStolen && canReturnCol) {
            // Return the column.
            for (row = 0; row < config.rows; row++) {
                panel = self.grid[row][col];

                if (panel.isStolen()) {
                    panel.flipStolen();
                    self.handleAdjacentRoadPanels(row, col);
                }
            }

            panelsReturned = true;
        }

        return {
            panelsStolen   : panelsStolen,
            panelsReturned : panelsReturned
        };
    };

    this.startStolenPanelTimeout = function startStolenPanelTimeout() {
        self.shouldReturnStolenPanels = false;
        clearTimeout(self.stolenPanelTimeout);

        self.stolenPanelTimeout = setTimeout(
            function () {
                self.shouldReturnStolenPanels = true;

                self.updateStolenPanels();
            },
            10000
        );
    };

    this.updateStolenPanels = function updateStolenPanels() {
        var panelsReturned = false,
            canReturnPanels = true,
            numHalfCols = config.cols / 2,
            col,
            returnColAttempt;

        if (self.shouldReturnStolenPanels) {
            // Attempt to return all of the stolen panels on the left side of the field from left to right.
            for (col = 0; col < numHalfCols; col++) {
                returnColAttempt = self.returnCol(col);

                if (returnColAttempt.panelsStolen) {
                    if (returnColAttempt.panelsReturned) {
                        panelsReturned = true;
                    } else {
                        canReturnPanels = false;
                        break;
                    }
                }
            }

            // Panels can only be stolen from one side of the field or the other.
            if (!panelsReturned && canReturnPanels) {
                // Attempt to return all of the stolen panels on the right side of the field from right to left.
                for (col = config.cols - 1; col >= numHalfCols; col--) {
                    returnColAttempt = self.returnCol(col);

                    if (returnColAttempt.panelsStolen) {
                        if (returnColAttempt.panelsReturned) {
                            panelsReturned = true;
                        } else {
                            canReturnPanels = false;
                            break;
                        }
                    }
                }
            }

            // The process is complete if no character has stopped it along the way and panels have been returned.
            if (canReturnPanels && panelsReturned) {
                self.shouldReturnStolenPanels = false;
            }
        }
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
    };

    this.initialize();
};
