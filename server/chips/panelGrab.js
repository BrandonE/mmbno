'use strict';

var GrabType = require(__dirname + '/types/grab'),
    extend = require(__dirname + '/extend');

function AreaGrabConstructor(io, config, game, character) {
    var self = this;

    this.properties.codes = ['*'];
    this.properties.description = 'Steals 1 enemy square';
    this.properties.name = 'Panel Grab';
    this.properties.short = 'PanlGrab';

    this.use = function use() {
        var grid = game.getField().getGrid(),
            row = character.getRow(),
            col,
            stole = false;

        if (character.getPlayerNum() === 1) {
            for (col = character.getCol(); col < config.cols; col++) {
                if (self.stealPanel(grid[row][col])) {
                    stole = true;
                    break;
                }
            }
        } else {
            for (col = character.getCol(); col >= 0; col--) {
                if (self.stealPanel(grid[row][col])) {
                    stole = true;
                    break;
                }
            }
        }

        if (stole) {
            game.getField().startStolenPanelTimeout();
        }
    }
}

module.exports = function AreaGrab(io, config, game, character) {
    return extend(AreaGrabConstructor, GrabType, io, config, game, character);
};
