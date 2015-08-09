'use strict';

var Chip = require(__dirname + '/..'),
    extend = require(__dirname + '/../extend');

function SpreaderConstructor(io, config, game, character, code) {
    var self = this;

    this.use = function use() {
        character.shoot(self.properties.power, self.properties.element, true, null, function onHit(panel) {
            var grid = game.getField().getGrid(),
                row,
                rowOffset,
                panelRow = panel.getRow(),
                col,
                colOffset,
                panelCol = panel.getCol(),
                newPanel,
                newPanelCharacter;

            for (rowOffset = -1; rowOffset <= 1; rowOffset++) {
                row = panelRow + rowOffset;

                if (row < 0 || row >= config.rows) {
                    break;
                }

                for (colOffset = -1; colOffset <= 1; colOffset++) {
                    col = panelCol + colOffset;

                    if (col >= 0 && col < config.cols && (rowOffset !== 0 || colOffset !== 0)) {
                        newPanel = grid[row][col];
                        newPanelCharacter = newPanel.getCharacter();

                        if (newPanelCharacter) {
                            newPanelCharacter.takeDamage(self.power, self.element);
                        }
                    }
                }
            }
        });
    };
}

module.exports = function Spreader(io, config, game, character, code) {
    return extend(SpreaderConstructor, Chip, io, config, game, character, code);
};
