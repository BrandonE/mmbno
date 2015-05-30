'use strict';

var exports = (typeof module !== 'undefined' && typeof module.exports !== 'undefined') ? module.exports : window;

exports.checkPanelInBounds = function checkPanelInBounds(config, grid, playerNum, newRow, newCol) {
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

exports.createGrid = function createGrid(config) {
    var grid = [],
        cols,
        row,
        col,
        panel;

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

        grid.push(cols);
    }

    return grid;
};
