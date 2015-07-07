'use strict';

var Chip = require(__dirname + '/..'),
    extend = require(__dirname + '/../extend');

function TankCannonConstructor(io, config, game, character) {
    var self = this;

    this.use = function use() {
        character.shoot(
            self.properties.power, self.properties.element,
            function onHit(panel) {
                // Knocking "back" relative to the character's perspective means moving left.
                panel.getCharacter().move('left', 1);
            },
            function onMiss() {
                var grid = game.getField().getGrid(),
                    characterRow = character.getRow(),
                    row,
                    rowOffset,
                    col,
                    panel,
                    panelCharacter;

                // Hit the back column.
                if (character.getPlayerNum() === 1) {
                    col = config.cols - 1;
                } else {
                    col = 0;
                }

                // Hit the row the character is on, the one above it, and the one below it.
                for (rowOffset = -1; rowOffset <= 1; rowOffset++) {
                    row = characterRow + rowOffset;

                    if (row >= 0 && row < config.rows) {
                        panel = grid[row][col];
                        panelCharacter = panel.getCharacter();

                        if (panelCharacter) {
                            panelCharacter.takeDamage(self.properties.power, self.properties.element);
                        }

                        panel.crackOrBreak();
                    }
                }
            }
        );
    };
}

module.exports = function TankCannon(io, config, game, character) {
    return extend(TankCannonConstructor, Chip, io, config, game, character);
};
