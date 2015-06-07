'use strict';

var GrabType = require(__dirname + '/types/grab'),
    extend = require(__dirname + '/extend');

function AreaGrabConstructor(io, config, game, character) {
    var self = this;

    this.properties.codes = ['B', 'F', 'S'];
    this.properties.description = 'Steals left edge from enemy';
    this.properties.name = 'Area Grab';
    this.properties.short = 'AreaGrab';
    this.properties.stars = 2;

    this.use = function use() {
        var col,
            stole = false;

        if (character.getPlayerNum() === 1) {
            for (col = 0; col < config.cols; col++) {
                if (self.stealRows(col)) {
                    stole = true;
                    break;
                }
            }
        } else {
            for (col = config.cols - 1; col >= 0; col--) {
                if (self.stealRows(col)) {
                    stole = true;
                    break;
                }
            }
        }

        if (stole) {
            game.getField().startStolenPanelTimeout();
        }
    }

    this.stealRows = function stealRows(col) {
        var grid = game.getField().getGrid(),
            row,
            panel,
            stole = false;

        for (row = 0; row < config.rows; row++) {
            panel = grid[row][col];

            if (self.stealPanel(panel)) {
                stole = true;
            }
        }

        return stole;
    }
}

module.exports = function AreaGrab(io, config, game, character) {
    return extend(AreaGrabConstructor, GrabType, io, config, game, character);
};
