'use strict';

var Chip = require(__dirname + '/..'),
    extend = require(__dirname + '/../extend');

function GrabConstructor(io, config, game, character) {
    var self = this;

    this.damage = 10;

    this.stealPanel = function stealPanel(panel) {
        var panelGrabbed = false,
            panelReturned = false,
            panelCharacter;

        if (!panel.isInBounds(character)) {
            panelCharacter = panel.getCharacter();

            // If this panel was already stolen, this is actually a return.
            if (panel.isStolen()) {
                panelReturned = true;
            }

            if (panelCharacter) {
                panelCharacter.takeDamage(self.damage);
            } else {
                panel.flipStolen();
            }

            panelGrabbed = true;
        }

        return {
            panelGrabbed  : panelGrabbed,
            panelReturned : panelReturned
        };
    };
}

module.exports = function Grab(io, config, game, character) {
    return extend(GrabConstructor, Chip, io, config, game, character);
};
