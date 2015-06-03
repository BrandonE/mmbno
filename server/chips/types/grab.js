'use strict';

var Chip = require(__dirname + '/..'),
    extend = require(__dirname + '/../extend');

function GrabConstructor(io, config, game, character) {
    var self = this;

    this.damage = 10;

    this.stealPanel = function stealPanel(panel) {
        var panelCharacter;

        if (!panel.isInBounds(character)) {
            panelCharacter = panel.getCharacter();

            if (panelCharacter) {
                panelCharacter.takeDamage(self.damage);
            } else {
                panel.flipStolen();
            }

            return true;
        } else {
            return false;
        }
    }

    this.timeout = function timeout() {
        clearTimeout(game.yieldStolenPanelsTimeout);
        game.setYieldStolenPanels(false);
        game.yieldStolenPanelsTimeout = setTimeout(
            function () {
                var grid = game.getField().getGrid(),
                    row,
                    col,
                    panel,
                    panelCharacter;

                for (row = 0; row < config.rows; row++) {
                    for (col = 0; col < config.cols; col++) {
                        panel = grid[row][col];

                        if (panel.isStolen()) {
                            panelCharacter = panel.getCharacter();
                            if (panelCharacter && panel.isInBounds(panelCharacter)) {
                                game.setYieldStolenPanels(true);
                            } else {
                                panel.flipStolen();
                            }
                        }
                    }
                }
            },
            10000
        );
    };
}

module.exports = function Grab(io, config, game, character) {
    return extend(GrabConstructor, Chip, io, config, game, character);
};
