'use strict';

var Chip = require(__dirname + '/..'),
    extend = require(__dirname + '/../extend');

function VulcanConstructor(io, config, game, character) {
    var self = this;

    this.shoot = function shoot() {
        character.shoot(self.properties.power, self.properties.element, function onHit(panel) {
            var grid = game.getField().getGrid(),
                newCol = panel.getCol(),
                newPanel,
                newPanelCharacter;

            if (character.getPlayerNum() === 1) {
                newCol++;
            } else {
                newCol--;
            }

            if (newCol >= 0 && newCol < config.cols) {
                newPanel = grid[panel.getRow()][newCol];
                newPanelCharacter = newPanel.getCharacter();

                if (newPanelCharacter) {
                    newPanelCharacter.takeDamage(self.power, self.element);
                }
            }
        });

        character.addStatus('attacking');

        self.properties.bullets--;

        if (self.properties.bullets) {
            setTimeout(function() {
                character.removeStatus('attacking');
                self.shoot();
            }, 150);
        } else {
            character.removeStatus('attacking');
        }
    };

    this.use = function use() {
        self.shoot();
    };
}

module.exports = function Vulcan(io, config, game, character) {
    return extend(VulcanConstructor, Chip, io, config, game, character);
};
