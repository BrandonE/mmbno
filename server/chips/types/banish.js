'use strict';

var Chip = require(__dirname + '/..'),
    extend = require(__dirname + '/../extend');

function BanishConstructor(io, config, game, character, code) {
    var self = this;

    this.use = function use() {
        var thieves = [],
            thief,
            t,
            stolenPanels = 0,
            grid = game.getField().getGrid(),
            row,
            col,
            panel,
            panelCharacter,
            panelInBounds;

        for (row = 0; row < config.rows; row++) {
            for (col = 0; col < config.cols; col++) {
                panel = grid[row][col];
                panelCharacter = panel.getCharacter();
                panelInBounds = panel.isInBounds(character);

                if (panel.isStolen()) {
                    /*
                     Check if this panel is in the bounds of the player using this chip. If so, the player using this
                     chip is on the thieving side. This chip has no effect.
                     */
                    if (panelInBounds) {
                        return;
                    } else {
                        stolenPanels++;
                    }
                }

                if (!panelInBounds && panelCharacter) {
                    thieves.push(panelCharacter);
                }
            }
        }

        // Deal the chip's damage to each thief for each stolen panel.
        for (t = 0; t < thieves.length; t++) {
            thief = thieves[t];

            thief.takeDamage(stolenPanels * self.properties.damage);
        }
    };
}

module.exports = function Banish(io, config, game, character, code) {
    return extend(BanishConstructor, Chip, io, config, game, character, code);
};
