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
        var col;

        if (character.getPlayerNum() === 1) {
            for (col = character.getCol(); col < config.cols; col++) {
                console.log(col);
                if (self.stealRows(col)) {
                    break;
                }
            }
        } else {
            for (col = character.getCol(); col >= 0; col--) {
                if (self.stealRows(col)) {
                    break;
                }
            }
        }
    }

    this.stealRows = function stealRows(col) {
        var grid = game.getField().getGrid(),
            row,
            panel,
            panelCharacter,
            stole = false;

        for (row = 0; row < config.rows; row++) {
            panel = grid[row][col];

            if (!panel.isInBounds(character)) {
                panelCharacter = panel.getCharacter();

                if (panelCharacter) {
                    panelCharacter.takeDamage(self.damage);
                } else {
                    panel.flipStolen();
                }

                stole = true;
            }
        }

        return stole;
    }
}

module.exports = function AreaGrab(io, config, game, character) {
    return extend(AreaGrabConstructor, GrabType, io, config, game, character);
};
