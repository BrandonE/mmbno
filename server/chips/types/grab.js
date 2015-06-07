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
}

module.exports = function Grab(io, config, game, character) {
    return extend(GrabConstructor, Chip, io, config, game, character);
};
