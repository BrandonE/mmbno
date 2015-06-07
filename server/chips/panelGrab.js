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
        var panelsStolen = false,
            grid = game.getField().getGrid(),
            row = character.getRow(),
            col,
            stealPanelAttempt;

        if (character.getPlayerNum() === 1) {
            for (col = character.getCol(); col < config.cols; col++) {
                stealPanelAttempt = self.stealPanel(grid[row][col]);

                if (stealPanelAttempt.panelGrabbed) {
                    if (!stealPanelAttempt.panelReturned) {
                        panelsStolen = true;
                    }

                    break;
                }
            }
        } else {
            for (col = character.getCol(); col >= 0; col--) {
                stealPanelAttempt = self.stealPanel(grid[row][col]);

                if (stealPanelAttempt.panelGrabbed) {
                    if (!stealPanelAttempt.panelReturned) {
                        panelsStolen = true;
                    }

                    break;
                }
            }
        }

        if (stealPanelAttempt) {
            game.getField().startStolenPanelTimeout();
        }
    }
}

module.exports = function AreaGrab(io, config, game, character) {
    return extend(AreaGrabConstructor, GrabType, io, config, game, character);
};
