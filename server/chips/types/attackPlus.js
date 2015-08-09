'use strict';

var Chip = require(__dirname + '/..'),
    extend = require(__dirname + '/../extend');

function AttackPlusConstructor(io, config, game, character, code) {
    var self = this;

    this.chain = function chain(chip) {
        // Add to the power to the previous chip if it has one.
        if (chip.getPower() !== null) {
            chip.addPower(self.properties.powerPlus);
            return true;
        }
    };
}

module.exports = function AttackPlus(io, config, game, character, code) {
    return extend(AttackPlusConstructor, Chip, io, config, game, character, code);
};
