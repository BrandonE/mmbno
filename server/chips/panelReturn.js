'use strict';

var Chip = require(__dirname + '/'),
    extend = require(__dirname + '/extend');

function PanelReturnConstructor(io, config, game, character, code) {
    var self = this;

    this.properties.codes = ['*'];
    this.properties.description = 'Fix your area\'s panels';
    this.properties.name = 'Panel Return';
    this.properties.short = 'PnlRetrn';
    this.properties.stars = 2;

    this.use = function use() {
        var field = game.getField(),
            grid = field.getGrid(),
            row,
            col,
            panel;

        for (row = 0; row < config.rows; row++) {
            for (col = 0; col < config.cols; col++) {
                panel = grid[row][col];

                if (panel.isStolen()) {
                    /*
                     Check if this panel is in the bounds of the player using this chip. If not, the player using this
                     chip is the one who lost panels. Otherwise, this chip has no effect.
                     */
                    if (!panel.isInBounds(character)) {
                        field.setShouldReturnStolenPanels(true);
                        field.updateStolenPanels();
                    }

                    return;
                }
            }
        }
    };
}

module.exports = function PanelReturn(io, config, game, character, code) {
    return extend(PanelReturnConstructor, Chip, io, config, game, character, code);
};
