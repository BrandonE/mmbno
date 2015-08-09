'use strict';

var Chip = require(__dirname + '/..'),
    extend = require(__dirname + '/../extend');

function RecoveryConstructor(io, config, game, character, code) {
    var self = this;

    this.use = function use() {
        character.heal(self.properties.health);
    };
}

module.exports = function Recovery(io, config, game, character, code) {
    return extend(RecoveryConstructor, Chip, io, config, game, character, code);
};
