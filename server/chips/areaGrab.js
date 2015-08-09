'use strict';

var GrabType = require(__dirname + '/types/grab'),
    extend = require(__dirname + '/extend');

function AreaGrabConstructor(io, config, game, character, code) {
    var self = this;

    this.properties.codes = ['B', 'F', 'S'];
    this.properties.description = 'Steals left edge from enemy';
    this.properties.name = 'Area Grab';
    this.properties.short = 'AreaGrab';
    this.properties.stars = 2;

    this.use = function use() {
        var panelsStolen = false,
            col,
            stealColAttempt;

        if (character.getPlayerNum() === 1) {
            for (col = 0; col < config.cols; col++) {
                stealColAttempt = self.stealCol(col);

                if (stealColAttempt.panelsGrabbed) {
                    if (!stealColAttempt.panelsReturned) {
                        panelsStolen = true;
                    }

                    break;
                }
            }
        } else {
            for (col = config.cols - 1; col >= 0; col--) {
                stealColAttempt = self.stealCol(col);

                if (stealColAttempt.panelsGrabbed) {
                    if (!stealColAttempt.panelsReturned) {
                        panelsStolen = true;
                    }

                    break;
                }
            }
        }

        if (panelsStolen) {
            game.getField().startStolenPanelTimeout();
        }
    };

    this.stealCol = function stealCol(col) {
        var panelsGrabbed = false,
            panelsReturned = false,
            grid = game.getField().getGrid(),
            row,
            stealPanelAttempt;

        for (row = 0; row < config.rows; row++) {
            stealPanelAttempt = self.stealPanel(grid[row][col]);

            if (stealPanelAttempt.panelGrabbed) {
                panelsGrabbed = true;

                if (stealPanelAttempt.panelReturned) {
                    panelsReturned = true;
                }
            }
        }

        return {
            panelsGrabbed  : panelsGrabbed,
            panelsReturned : panelsReturned
        };
    };
}

module.exports = function AreaGrab(io, config, game, character, code) {
    return extend(AreaGrabConstructor, GrabType, io, config, game, character, code);
};
